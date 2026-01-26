"""
Phase 3 Enhancement: Inverse-Consistency Check for ±β Pairs
Verifies that u(+β) + u(−β) ≈ 0 inside the mask
"""

import ants
import numpy as np
import json
from pathlib import Path

def ic_pm_beta(pc_path, mean_path, beta, sd_scale, mask_path, ref_like):
    """
    Compute inverse-consistency for ±β synthesized DVFs along one PC.
    
    Args:
        pc_path: Path to principal component DVF
        mean_path: Path to mean field DVF
        beta: Coefficient value (will test ±beta)
        sd_scale: Per-mode SD (sigma_k / sqrt(N-1))
        mask_path: Path to lung mask
        ref_like: Reference image for mask resampling
        
    Returns:
        dict with median and P95 of residual magnitude
    """
    # Load PC and mean
    mu = ants.image_read(str(mean_path)).numpy()
    U = ants.image_read(str(pc_path)).numpy()
    
    # Load and resample mask
    ref = ants.image_read(str(ref_like))
    mask_orig = ants.image_read(str(mask_path))
    mask = ants.apply_transforms(
        fixed=ref.split_channels()[0] if ref.components > 1 else ref,
        moving=mask_orig,
        transformlist=[],
        interpolator='nearestNeighbor'
    ).numpy() > 0
    
    # Synthesize u(+β) and u(−β)
    u_plus = mu + (+beta) * U * sd_scale
    u_minus = mu + (-beta) * U * sd_scale
    
    # Compute residual: should be near zero
    residual = u_plus + u_minus
    
    # Magnitude inside mask
    mag = np.linalg.norm(residual, axis=-1)[mask]
    
    return {
        "median_mm": float(np.median(mag)),
        "p95_mm": float(np.percentile(mag, 95)),
        "max_mm": float(np.max(mag)),
        "mean_mm": float(np.mean(mag))
    }

def main():
    """Test inverse-consistency for PC1 and PC2"""
    
    print("="*70)
    print("Inverse-Consistency Check for +/- Beta Pairs")
    print("="*70)
    
    # Paths
    pca_dir = Path("results/pca")
    mask_path = Path("data/preprocessed/popi_ants/phase50_lung_mask.nii.gz")
    ref_like = Path("results/synthetic/phase50_iso_like_dvf.nii.gz")
    
    # SD scales (from PCA: sigma_k / sqrt(2))
    sd_scales = {
        "pc1": 1756.89 / np.sqrt(2),  # 1242.3
        "pc2": 817.54 / np.sqrt(2)    # 578.1
    }
    
    results = {}
    
    # Test PC1 at ±1.0 SD
    print("\n1. PC1 Inverse-Consistency (±1.0 SD):")
    ic_pc1 = ic_pm_beta(
        pc_path=pca_dir / "pc_1.nii.gz",
        mean_path=pca_dir / "pc_mean.nii.gz",
        beta=1.0,
        sd_scale=sd_scales["pc1"],
        mask_path=mask_path,
        ref_like=ref_like
    )
    print(f"   Residual |u(+1) + u(-1)|:")
    print(f"     Median: {ic_pc1['median_mm']:.4f} mm")
    print(f"     P95:    {ic_pc1['p95_mm']:.4f} mm")
    print(f"     Max:    {ic_pc1['max_mm']:.4f} mm")
    
    results["pc1_pm1sd"] = ic_pc1
    
    # Test PC2 at ±1.0 SD
    print("\n2. PC2 Inverse-Consistency (±1.0 SD):")
    ic_pc2 = ic_pm_beta(
        pc_path=pca_dir / "pc_2.nii.gz",
        mean_path=pca_dir / "pc_mean.nii.gz",
        beta=1.0,
        sd_scale=sd_scales["pc2"],
        mask_path=mask_path,
        ref_like=ref_like
    )
    print(f"   Residual |u(+1) + u(-1)|:")
    print(f"     Median: {ic_pc2['median_mm']:.4f} mm")
    print(f"     P95:    {ic_pc2['p95_mm']:.4f} mm")
    print(f"     Max:    {ic_pc2['max_mm']:.4f} mm")
    
    results["pc2_pm1sd"] = ic_pc2
    
    # Interpretation
    print("\n3. Interpretation:")
    threshold = 0.1  # mm
    
    if ic_pc1['median_mm'] < threshold and ic_pc2['median_mm'] < threshold:
        print(f"   [PASS] Excellent symmetry (medians < {threshold} mm)")
    elif ic_pc1['median_mm'] < 1.0 and ic_pc2['median_mm'] < 1.0:
        print(f"   [OK] Good symmetry (medians < 1.0 mm)")
    else:
        print(f"   [WARNING] Poor symmetry - check PCA implementation")
    
    # Save results
    out_path = pca_dir / "inverse_consistency_pm_beta.json"
    results["metadata"] = {
        "description": "Inverse-consistency check for ±β synthesized DVFs",
        "formula": "| u(+β) + u(−β) | should be ≈ 0",
        "interpretation": "Small residuals confirm PCA symmetry and correct synthesis",
        "threshold_excellent_mm": 0.1,
        "threshold_good_mm": 1.0
    }
    
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n[OK] Saved inverse-consistency results: {out_path}")
    print("="*70)

if __name__ == "__main__":
    main()
