#!/usr/bin/env python3
"""
FDK Reconstruction with One-Step Scatter Correction
Implements projection-domain scatter removal before log transform
"""
import json, numpy as np, ants, astra
from pathlib import Path
from scipy.ndimage import gaussian_filter

print("="*70)
print("FDK + ONE-STEP SCATTER CORRECTION")
print("="*70)

def shading_correct_mu(mu_xyz, body_mask, sigma=25):
    """Shading correction with recommended sigma=25mm"""
    med = float(np.median(mu_xyz[body_mask]))
    tmp = mu_xyz.copy()
    tmp[~body_mask] = med
    bias = gaussian_filter(tmp, sigma=sigma)
    res = mu_xyz / np.maximum(bias, 1e-6)
    scale = float(np.mean(mu_xyz[body_mask]) / (np.mean(res[body_mask]) + 1e-6))
    return res * scale

# Load configs
cfg = json.load(open("configs/cbct_geom.json"))
M = json.load(open("results/cbct/manifest.json"))
G = cfg["geometry"]
R = cfg["reconstruction"]

# Physics parameters
I0 = cfg["noise_model"]["I0"]
alpha = cfg["noise_model"]["scatter_alpha"]
sigma_px = cfg["noise_model"]["scatter_lpf_sigma_px"]
mu_w = 0.0185  # Water attenuation coefficient

print(f"\nPhysics: I0={I0}, scatter_alpha={alpha}, blur_sigma={sigma_px}px")
print(f"Scatter correction: ONE-STEP projection-domain\n")

# ASTRA geometries
angles = np.deg2rad(np.linspace(G["angles_deg_start"], G["angles_deg_end"], G["n_proj"]).astype(np.float32))
proj_geom = astra.create_proj_geom('cone', G["det_pixel_mm"], G["det_pixel_mm"],
                                   G["det_rows"], G["det_cols"], angles,
                                   G["SAD_mm"], G["SDD_mm"] - G["SAD_mm"])
nx, ny, nz = M["grid"]["shape"]
sx, sy, sz = np.array([nx, ny, nz]) * np.array(M["grid"]["spacing_mm"])
vol_geom = astra.create_vol_geom(nx, ny, nz, -sx/2, sx/2, -sy/2, sy/2, -sz/2, sz/2)

# Check for beam hardening coefficients
bh_path = Path("results/cbct/beam_hardening_coeff.json")
if bh_path.exists():
    bh = json.load(open(bh_path))
    a1, a2 = bh["a1"], bh["a2"]
    USE_BH = True
    print(f"Beam hardening: p' = {a1:.6f}*p + {a2:.8f}*p^2")
else:
    USE_BH = False
    print("Beam hardening: Not available")

Path("results/cbct/recon").mkdir(parents=True, exist_ok=True)

# Process all cases
for lab in M["cases"]:
    print(f"\n{'='*70}")
    print(f"Case: {lab.upper()}")
    print('='*70)
    
    # Load data
    gt = ants.image_read(M["cases"][lab]["gt_hu"])
    gt_hu = gt.numpy().astype(np.float32)
    body_mask = gt_hu > -950.0
    
    # Load projections
    p_meas = np.load(f"results/cbct/projections/{lab}_proj.npz")["p"]
    
    # Reconstruct measured counts (I = I0 * exp(-p))
    I_meas = I0 * np.exp(-np.clip(p_meas, 0, 100)).astype(np.float32)
    
    # === STEP 1: Initial FDK (baseline) ===
    print("  [1/5] Initial FDK reconstruction...")
    pid0 = astra.data3d.create('-sino', proj_geom, p_meas)
    rid0 = astra.data3d.create('-vol', vol_geom)
    
    cfg_fdk = astra.astra_dict('FDK_CUDA')
    cfg_fdk['ProjectionDataId'] = pid0
    cfg_fdk['ReconstructionDataId'] = rid0
    cfg_fdk['option'] = {
        'ShortScan': True,
        'FilterType': 'hann',
        'FilterD': 0.8,
        'VoxelSuperSampling': 2
    }
    
    alg0 = astra.algorithm.create(cfg_fdk)
    astra.algorithm.run(alg0)
    rec0_zyx = astra.data3d.get(rid0)
    rec0_mu = np.transpose(rec0_zyx, (2, 1, 0))
    
    astra.algorithm.delete(alg0)
    astra.data3d.delete(rid0)
    astra.data3d.delete(pid0)
    
    # === STEP 2: Forward project to estimate primary ===
    print("  [2/5] Estimating scatter...")
    mu0_zyx = np.transpose(rec0_mu, (2, 1, 0)).astype(np.float32)
    vid0 = astra.data3d.create('-vol', vol_geom, mu0_zyx)
    pid_fp, L_hat = astra.create_sino3d_gpu(vid0, proj_geom, vol_geom, returnData=True)
    
    # Primary estimate
    I_hat = I0 * np.exp(-np.clip(L_hat, 0, 100))
    
    # Scatter estimate (Gaussian blur)
    S_hat = np.zeros_like(I_hat, dtype=np.float32)
    for k in range(I_hat.shape[0]):
        S_hat[k] = alpha * gaussian_filter(I_hat[k], sigma_px, mode='nearest')
    
    astra.data3d.delete(vid0)
    astra.data3d.delete(pid_fp)
    
    # === STEP 3: Subtract scatter and re-log ===
    print("  [3/5] Scatter correction + re-log...")
    I_corr = np.clip(I_meas - S_hat, 1.0, None)
    p1 = -np.log(I_corr / I0).astype(np.float32)
    
    # Optional: Apply beam hardening
    if USE_BH:
        p1 = (a1 * p1 + a2 * (p1 ** 2)).astype(np.float32)
        print(f"    Applied beam hardening quadratic")
    
    # === STEP 4: Final FDK with corrected projections ===
    print("  [4/5] Final FDK reconstruction...")
    pid1 = astra.data3d.create('-sino', proj_geom, p1)
    rid1 = astra.data3d.create('-vol', vol_geom)
    
    cfg_fdk['ProjectionDataId'] = pid1
    cfg_fdk['ReconstructionDataId'] = rid1
    
    alg1 = astra.algorithm.create(cfg_fdk)
    astra.algorithm.run(alg1)
    rec1_zyx = astra.data3d.get(rid1)
    rec1_mu = np.transpose(rec1_zyx, (2, 1, 0))
    
    astra.algorithm.delete(alg1)
    astra.data3d.delete(rid1)
    astra.data3d.delete(pid1)
    
    # === STEP 5: Shading correction + HU conversion ===
    print("  [5/5] Shading correction...")
    rec1_mu = shading_correct_mu(rec1_mu, body_mask, sigma=25)
    rec1_hu = 1000.0 * (rec1_mu / mu_w - 1.0)
    
    # Save (NO HU-domain calibration for real cases!)
    rec_img = ants.from_numpy(rec1_hu.astype(np.float32), 
                              origin=gt.origin, spacing=gt.spacing, direction=gt.direction)
    ants.image_write(rec_img, f"results/cbct/recon/{lab}_reconHU_scatter_corrected.nii.gz")
    
    # Quick metrics
    lung_mask = (gt_hu > -900) & (gt_hu < -400) & body_mask
    if lung_mask.sum() > 1000:
        lung_bias = float((rec1_hu[lung_mask] - gt_hu[lung_mask]).mean())
        print(f"    Lung bias: {lung_bias:+.1f} HU")
    
    body_bias = float((rec1_hu[body_mask] - gt_hu[body_mask]).mean())
    print(f"    Body bias: {body_bias:+.1f} HU")
    print(f"    HU range:  [{rec1_hu.min():.0f}, {rec1_hu.max():.0f}]")
    
    # Scatter stats
    scatter_frac = float(S_hat.mean() / I_meas.mean())
    print(f"    Scatter fraction: {scatter_frac:.2%}")

print("\n" + "="*70)
print("[OK] All cases reconstructed with scatter correction")
print("="*70)
print("\nNext: Run metrics to assess improvement")
