#!/usr/bin/env python3
"""
Compute Metrics for Scatter-Corrected Reconstructions
Compare against ground truth: SSIM, PSNR, NCC, HU bias
"""
import json, numpy as np, ants
from pathlib import Path
from skimage.metrics import structural_similarity as ssim, peak_signal_noise_ratio as psnr

print("="*70)
print("SCATTER-CORRECTED RECONSTRUCTION METRICS")
print("="*70)

HU_MIN, HU_MAX = -1000.0, 400.0
RNG = HU_MAX - HU_MIN

def clip(a):
    return np.clip(a, HU_MIN, HU_MAX).astype(np.float32)

def ncc(a, b):
    a0, b0 = a - a.mean(), b - b.mean()
    return float((a0 @ b0) / (np.linalg.norm(a0) * np.linalg.norm(b0) + 1e-8))

M = json.load(open("results/cbct/manifest.json"))
results = {}

for lab in M["cases"]:
    print(f"\n{'='*70}")
    print(f"Case: {lab.upper()}")
    print('='*70)
    
    # Load ground truth
    gt = ants.image_read(M["cases"][lab]["gt_hu"])
    gt_hu = gt.numpy().astype(np.float32)
    
    # Load scatter-corrected reconstruction
    recon_path = f"results/cbct/recon/{lab}_reconHU_scatter_corrected.nii.gz"
    if not Path(recon_path).exists():
        print(f"  [SKIP] Reconstruction not found")
        continue
    
    rec = ants.image_read(recon_path)
    rec_hu = rec.numpy().astype(np.float32)
    
    # Create masks
    body_mask = gt_hu > -950.0
    lung_mask = (gt_hu > -900) & (gt_hu < -400) & body_mask
    
    if lung_mask.sum() < 100:
        print(f"  [WARN] Lung mask too small")
        continue
    
    print(f"  Body voxels: {body_mask.sum():,}")
    print(f"  Lung voxels: {lung_mask.sum():,}")
    
    # Compute metrics for lung and body
    def compute_metrics(mask, name):
        A = clip(gt_hu)[mask]
        B = clip(rec_hu)[mask]
        
        # PSNR
        ps = float(psnr(A, B, data_range=RNG))
        
        # SSIM (slice-wise)
        ssim_vals = []
        for z in range(gt_hu.shape[2]):
            if mask[:,:,z].sum() < 100:
                continue
            A_slice = (clip(gt_hu[:,:,z]) - HU_MIN) / RNG
            B_slice = (clip(rec_hu[:,:,z]) - HU_MIN) / RNG
            ssim_vals.append(ssim(A_slice, B_slice, data_range=1.0, gaussian_weights=True))
        
        ss = float(np.mean(ssim_vals)) if ssim_vals else 0.0
        
        # NCC
        nc = ncc(A, B)
        
        # HU bias
        bias = float(B.mean() - A.mean())
        
        return {
            "SSIM": ss,
            "PSNR_dB": ps,
            "NCC": nc,
            "HU_bias": bias,
            "voxels": int(mask.sum())
        }
    
    lung_metrics = compute_metrics(lung_mask, "LUNG")
    body_metrics = compute_metrics(body_mask, "BODY")
    
    results[lab] = {
        "lung": lung_metrics,
        "body": body_metrics
    }
    
    # Print results
    print(f"\n  LUNG METRICS:")
    print(f"    SSIM:     {lung_metrics['SSIM']:.4f}")
    print(f"    PSNR:     {lung_metrics['PSNR_dB']:.2f} dB")
    print(f"    NCC:      {lung_metrics['NCC']:.4f}")
    print(f"    HU bias:  {lung_metrics['HU_bias']:+.1f} HU")
    
    print(f"\n  BODY METRICS:")
    print(f"    SSIM:     {body_metrics['SSIM']:.4f}")
    print(f"    PSNR:     {body_metrics['PSNR_dB']:.2f} dB")
    print(f"    NCC:      {body_metrics['NCC']:.4f}")
    print(f"    HU bias:  {body_metrics['HU_bias']:+.1f} HU")

# Save results
json.dump(results, open("results/cbct/recon/scatter_corrected_metrics.json", "w"), indent=2)

print("\n" + "="*70)
print("SUMMARY TABLE")
print("="*70)
print(f"{'Case':<18} {'SSIM':>6} {'PSNR':>7} {'NCC':>7} {'Lung Bias':>11}")
print("-"*70)

for lab in ["exhale_strong", "exhale_moderate", "mean", "mixed_1", "mixed_2"]:
    if lab in results and "lung" in results[lab]:
        m = results[lab]["lung"]
        print(f"{lab:<18} {m['SSIM']:>6.3f} {m['PSNR_dB']:>7.2f} {m['NCC']:>7.3f} {m['HU_bias']:>+10.1f} HU")

print("="*70)
print("TARGETS:           >= 0.85  >= 20 dB  >= 0.85      +/- 60 HU")
print("="*70)

# Check if targets met
if results:
    mean_lung = results.get("mean", {}).get("lung", {})
    if mean_lung:
        ssim_val = mean_lung["SSIM"]
        psnr_val = mean_lung["PSNR_dB"]
        ncc_val = mean_lung["NCC"]
        bias_val = abs(mean_lung["HU_bias"])
        
        print("\nMEAN CASE STATUS:")
        print(f"  SSIM:      {ssim_val:.3f}  {'PASS' if ssim_val >= 0.85 else 'FAIL'}")
        print(f"  PSNR:      {psnr_val:.2f} dB  {'PASS' if psnr_val >= 20 else 'FAIL'}")
        print(f"  NCC:       {ncc_val:.3f}  {'PASS' if ncc_val >= 0.85 else 'FAIL'}")
        print(f"  Lung Bias: {mean_lung['HU_bias']:+.1f} HU  {'PASS' if bias_val <= 60 else 'CLOSE' if bias_val <= 70 else 'FAIL'}")

print(f"\n[OK] Metrics saved to: results/cbct/recon/scatter_corrected_metrics.json")
