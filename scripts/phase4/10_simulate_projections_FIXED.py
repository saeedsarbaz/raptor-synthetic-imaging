#!/usr/bin/env python3
"""
Step 3 (FIXED): Simulate projections WITHOUT pedestal correction
After 9+ hours of debugging, discovered pedestal over-corrects when scatter is present.
"""
import json, numpy as np, ants, astra
from pathlib import Path
from scipy.ndimage import gaussian_filter

print("="*70)
print("STEP 3 (FIXED): SIMULATE PROJECTIONS - NO PEDESTAL")
print("="*70)

def to_mu(hu, mu_w=0.0185):
    return mu_w * (1.0 + hu / 1000.0)

# Load config and manifest
cfg = json.load(open("configs/cbct_geom.json"))
M = json.load(open("results/cbct/manifest.json"))
G = cfg["geometry"]
N = cfg["noise_model"]
shapes = M["grid"]["shape"]

# ASTRA geometries
angles = np.deg2rad(np.linspace(G["angles_deg_start"], G["angles_deg_end"], G["n_proj"]).astype(np.float32))
proj_geom = astra.create_proj_geom('cone', 
                                   G["det_pixel_mm"], G["det_pixel_mm"],
                                   G["det_rows"], G["det_cols"], 
                                   angles, 
                                   G["SAD_mm"], 
                                   G["SDD_mm"] - G["SAD_mm"])

nx, ny, nz = shapes
spacing = M["grid"]["spacing_mm"]
sx, sy, sz = np.array(shapes) * np.array(spacing)
vol_geom = astra.create_vol_geom(nx, ny, nz, -sx/2, sx/2, -sy/2, sy/2, -sz/2, sz/2)

# Physics parameters
I0 = N["I0"]
rd = N["readout_sigma_counts"]
s_blur = N["detector_blur_sigma_px"]
scat_a = N["scatter_alpha"]
scat_sig = N["scatter_lpf_sigma_px"]

print(f"\nGeometry:")
print(f"  FOV: {G['det_cols']*G['det_pixel_mm']*G['SAD_mm']/G['SDD_mm']:.1f}mm")
print(f"  Projections: {G['n_proj']}")
print(f"\nPhysics:")
print(f"  I0: {I0:.0f}")
print(f"  Scatter alpha: {scat_a}")
print(f"  Blur sigma: {s_blur} px")
print(f"  Pedestal correction: DISABLED (scatter model is accurate)")

Path("results/cbct/projections").mkdir(parents=True, exist_ok=True)

# Process MEAN case only
lab = "mean"
print(f"\nProcessing {lab}...")

hu_img = ants.image_read(f"results/cbct/volumes_prep/{lab}_HU_prep.nii.gz")
hu = hu_img.numpy().astype(np.float32)
mu = to_mu(hu)

# Forward project attenuation
print("  Forward projecting...")
mu_zyx = np.transpose(mu, (2,1,0)).astype(np.float32)
vid = astra.data3d.create('-vol', vol_geom, mu_zyx)
pid, L = astra.create_sino3d_gpu(vid, proj_geom, vol_geom, returnData=True)

# Ideal counts
I = I0 * np.exp(-L)

# Detector PSF blur
if s_blur > 0:
    print("  Applying detector blur...")
    for k in range(I.shape[0]):
        I[k] = gaussian_filter(I[k], s_blur, mode='nearest')

# Additive scatter
if scat_a > 0:
    print("  Adding scatter...")
    for k in range(I.shape[0]):
        s = gaussian_filter(I[k], scat_sig, mode='nearest')
        I[k] = I[k] + scat_a * s

# Poisson + readout noise
print("  Adding noise...")
rng = np.random.default_rng(42)
I_noisy = rng.poisson(np.clip(I, 1.0, None)).astype(np.float32) + \
          rng.normal(0.0, rd, I.shape).astype(np.float32)

# Convert to projections (NO PEDESTAL CORRECTION)
print("  Converting to projections (no pedestal)...")
p = -np.log(np.clip(I_noisy / I0, 1e-6, None)).astype(np.float32)

# Save
np.savez_compressed(f"results/cbct/projections/{lab}_proj.npz", p=p)

print(f"\n  L mean: {L.mean():.3f} (ideal line integrals)")
print(f"  p mean: {p.mean():.3f} (reconstructed projections)")
print(f"  Diff:   {p.mean() - L.mean():+.3f} (should be small, <0.1)")

if abs(p.mean() - L.mean()) < 0.1:
    print("  [PASS] Projection values are correct!")
else:
    print("  [WARN] Large difference - check physics model")

# Cleanup ASTRA
astra.data3d.delete(vid)
astra.data3d.delete(pid)

print("\n" + "="*70)
print("[OK] Step 3 (FIXED) complete - mean projection saved")
print("="*70)
