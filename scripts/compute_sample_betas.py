"""
Phase 3 Enhancement: Compute Per-Sample Beta Coefficients
Shows how original DVFs project onto principal components in SD units
"""

import numpy as np
import ants
import json
from pathlib import Path

def sample_betas_sd(X, mu, U, S):
    """
    Compute beta coefficients for samples in SD units.
    
    Args:
        X: (P, N) stacked samples (masked DVFs)
        mu: (P,) mean vector
        U: (P, K) principal components
        S: (K,) singular values
        
    Returns:
        betas: (K, N) coefficients in SD units
        scale: (K,) per-mode SD
    """
    N = X.shape[1]
    
    # Center data
    Xc = X - mu[:, None]
    
    # Per-mode SD scale
    scale = S / np.sqrt(max(1, N - 1))  # For N=3, scale = S/sqrt(2)
    
    # Project onto PCs: alphas = U^T @ Xc
    alphas = U.T @ Xc  # (K, N)
    
    # Convert to SD units: betas = alphas / scale
    betas = (alphas.T / (scale + 1e-8)).T  # (K, N) in SD units
    
    return betas, scale

def main():
    """Compute and save beta coefficients for original DVFs"""
    
    print("="*70)
    print("Computing Per-Sample Beta Coefficients")
    print("="*70)
    
    # Load PCA metadata
    pca_meta_path = Path("results/pca/pca_meta.json")
    with open(pca_meta_path, 'r') as f:
        pca_meta = json.load(f)
    
    singular_values = np.array(pca_meta['singular_values'])
    variance_explained = np.array(pca_meta['variance_explained'])
    
    print(f"\n1. PCA Metadata:")
    print(f"   Singular values: {singular_values}")
    print(f"   Variance explained: {variance_explained}%")
    
    # Load DVFs and mask
    dvf_dir = Path("results/popi_ants_roi")
    mask_path = Path("data/preprocessed/popi_ants/phase50_lung_mask.nii.gz")
    
    dvfs = []
    for dvf_name in ["dvf_70_to_50_FINAL.nii.gz", 
                      "dvf_30_to_50_FINAL.nii.gz", 
                      "dvf_00_to_50_FINAL.nii.gz"]:
        dvf = ants.image_read(str(dvf_dir / dvf_name))
        dvfs.append(dvf)
    
    # Resample mask to DVF grid
    mask_orig = ants.image_read(str(mask_path))
    mask = ants.apply_transforms(
        fixed=dvfs[0].split_channels()[0],
        moving=mask_orig,
        transformlist=[],
        interpolator='nearestNeighbor'
    ).numpy() > 0
    
    print(f"\n2. Loading DVFs:")
    print(f"   Mask voxels: {mask.sum()}")
    
    # Pack DVFs into matrix
    X_list = []
    for i, dvf in enumerate(dvfs):
        arr = dvf.numpy().astype(np.float32)  # (Z, Y, X, 3)
        vec = arr[mask, :]  # (N_mask, 3)
        vec_flat = vec.flatten()  # (N_mask * 3,)
        X_list.append(vec_flat)
        print(f"   DVF {i+1}: shape {arr.shape} -> {vec_flat.shape[0]} elements")
    
    X = np.column_stack(X_list)  # (P, 3) where P=N_mask*3
    
    # Load mean and PCs
    mu = ants.image_read("results/pca/pc_mean.nii.gz").numpy()[mask, :].flatten()
    
    U_list = []
    for k in range(2):  # PC1, PC2
        pc = ants.image_read(f"results/pca/pc_{k+1}.nii.gz").numpy()[mask, :].flatten()
        U_list.append(pc)
    U = np.column_stack(U_list)  # (P, 2)
    
    # Compute betas
    betas, scale = sample_betas_sd(X, mu, U, singular_values[:2])
    
    print(f"\n3. Beta Coefficients (SD units):")
    print(f"   Per-mode SD: {scale}")
    print(f"\n   Sample Betas (rows=PCs, cols=Samples):")
    print(f"   {'':12s} DVF70    DVF30    DVF00")
    for k in range(2):
        print(f"   PC{k+1} (SD):    {betas[k,0]:7.3f}  {betas[k,1]:7.3f}  {betas[k,2]:7.3f}")
    
    # Save to JSON
    meta = {
        "description": "Beta coefficients for original DVFs in SD units",
        "sample_names": ["dvf_70_to_50", "dvf_30_to_50", "dvf_00_to_50"],
        "betas_rows_PCs_cols_samples": betas.tolist(),
        "per_mode_SD_mm": scale.tolist(),
        "interpretation": {
            "pc1": "Primary breathing amplitude (82.2% variance)",
            "pc2": "Breathing pattern variation (17.8% variance)"
        },
        "notes": [
            "Betas are in standard deviation (SD) units",
            "Formula: beta_k = (U_k^T @ (x - mu)) / (sigma_k / sqrt(N-1))",
            "Negative beta: exhale direction",
            "Positive beta: inhale direction"
        ]
    }
    
    out_path = Path("results/pca/sample_betas.json")
    with open(out_path, 'w') as f:
        json.dump(meta, f, indent=2)
    
    print(f"\n[OK] Saved sample betas: {out_path}")
    print("="*70)

if __name__ == "__main__":
    main()
