#!/usr/bin/env python3
"""
Phase 3: PCA on Deformation Vector Fields
Extract principal breathing motion modes from validated Phase 1 DVFs
"""
import ants
import numpy as np
import json
from pathlib import Path

def load_vector_field(path):
    """Load DVF and return ANTs image and numpy array"""
    v = ants.image_read(str(path))
    arr = v.numpy().astype(np.float32)  # (X,Y,Z,3)
    return v, arr

def mask_indices(mask_img):
    """Get flattened indices of mask voxels"""
    m = mask_img.numpy() > 0
    idx = np.where(m.ravel())[0]
    return idx, m.shape

def pack_fields_to_matrix(dvf_list, mask_img):
    """Stack masked vector voxels into matrix X in R^{P x N}
    
    P = 3 * |mask| (3 components per masked voxel)
    N = number of DVFs
    """
    idx, vol_shape = mask_indices(mask_img)
    N = len(dvf_list)
    X = []
    
    print(f"  Packing {N} DVFs into matrix...")
    for i, dvf_path in enumerate(dvf_list):
        _, arr = load_vector_field(dvf_path)
        # Flatten xyz to one vector per component inside mask
        v = arr.reshape(-1, 3)[idx, :]           # (|mask|, 3)
        X.append(v.reshape(-1))                  # (3*|mask|,)
        print(f"    DVF {i+1}/{N}: {len(v.reshape(-1))} elements")
    
    X = np.stack(X, axis=1).astype(np.float32)   # (P, N)
    print(f"  Design matrix X: {X.shape} (P={X.shape[0]}, N={X.shape[1]})")
    return X, idx, vol_shape

def pca_smallN(X):
    """PCA via eigen-decomposition of covariance in sample space
    
    For small N (<< P), compute eigendecomposition of X^T X (N x N) instead of X X^T (P x P)
    """
    N = X.shape[1]
    print(f"\n  Computing PCA (N={N})...")
    
    # Center across samples
    mu = X.mean(axis=1, keepdims=True)          # (P,1)
    Xc = X - mu
    print(f"    Centered data (mean field removed)")
    
    # Covariance in sample space: C = Xc^T Xc (N×N)
    C = Xc.T @ Xc
    print(f"    Computing eigendecomposition of {C.shape} covariance matrix...")
    evals, V = np.linalg.eigh(C)                # eigen-decomp (ascending)
    order = np.argsort(evals)[::-1]
    evals, V = evals[order], V[:, order]
    S = np.sqrt(np.maximum(evals, 0.0))         # singular values (length N)
    
    # PCs (eigenfields) in voxel space: U_k = (Xc @ v_k) / S_k
    U = []
    for k in range(len(S)):
        if S[k] > 1e-8:
            Uk = (Xc @ V[:, k]) / S[k]
            U.append(Uk)
            print(f"    PC {k+1}: singular value = {S[k]:.2f}")
    
    U = np.stack(U, axis=1) if len(U) else np.zeros_like(Xc)
    
    # Variance explained
    var = (S**2)
    var_ratio = (var / (var.sum() + 1e-8)).tolist()
    
    print(f"    Total PCs extracted: {U.shape[1]}")
    print(f"    Variance explained: {[f'{v:.1%}' for v in var_ratio[:U.shape[1]]]}")
    
    return mu.squeeze(), U, S, var_ratio  # mu: (P,), U: (P,K), S: (K,)

def unpack_to_vector_image(vec, idx, vol_shape, like_img):
    """Unpack masked vector back to (X,Y,Z,3) ANTs vector image"""
    out = np.zeros((np.prod(vol_shape), 3), dtype=np.float32)
    out[idx, :] = vec.reshape(-1, 3)
    out = out.reshape((*vol_shape, 3))
    
    # Create vector image by setting components
    # First create scalar reference from like_img
    scalar_ref = like_img if like_img.components == 1 else like_img.split_channels()[0]
    
    # Build vector image from 3 scalar components
    components = []
    for c in range(3):
        comp_img = ants.from_numpy(out[:,:,:,c], origin=scalar_ref.origin, 
                                   spacing=scalar_ref.spacing, direction=scalar_ref.direction)
        components.append(comp_img)
    
    # Merge components into vector image
    img = ants.merge_channels(components)
    return img

def main():
    print("="*70)
    print("Phase 3: PCA on Deformation Vector Fields")
    print("="*70)
    
    base = Path("results/popi_ants_roi")
    synth_base = Path("results/synthetic")
    out_dir = Path("results/pca")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Reference grid and mask (iso)
    print("\n1. Loading reference grid and mask...")
    ref_iso = ants.image_read(str(synth_base/"phase50_iso_like_dvf.nii.gz"))
    print(f"   Reference: {ref_iso.shape}, {ref_iso.spacing}")
    
    mask50 = ants.image_read("data/preprocessed/popi_ants/phase50_lung_mask.nii.gz").clone('unsigned char')
    mask50 = ants.apply_transforms(
        fixed=ref_iso,
        moving=mask50,
        transformlist=[],
        interpolator='nearestNeighbor'
    ).clone('unsigned char')
    print(f"   Mask voxels: {(mask50.numpy() > 0).sum()}")

    # DVFs to analyze
    print("\n2. Collecting DVFs...")
    dvfs = [
        base/"dvf_70_to_50_FINAL.nii.gz",
        base/"dvf_30_to_50_FINAL.nii.gz",
        base/"dvf_00_to_50_FINAL.nii.gz",
    ]
    
    for i, p in enumerate(dvfs):
        if not p.exists():
            raise FileNotFoundError(p)
        print(f"   DVF {i+1}: {p.name}")

    # Stack and PCA
    print("\n3. Packing DVFs and computing PCA...")
    X, idx, vol_shape = pack_fields_to_matrix(dvfs, mask50)
    mu, U, S, var_ratio = pca_smallN(X)   # mu: (P,), U: (P,K), S: (K,)
    K = U.shape[1]

    # Save mean and PCs as vector images
    print("\n4. Saving mean field and principal components...")
    mean_img = unpack_to_vector_image(mu, idx, vol_shape, ref_iso)
    ants.image_write(mean_img, str(out_dir/"pc_mean.nii.gz"))
    print(f"   Saved: pc_mean.nii.gz")
    
    pcs_meta = {
        "n_samples": len(dvfs),
        "n_components": K,
        "singular_values": S[:K].tolist(),
        "variance_explained": var_ratio[:K],
        "cumulative_variance": np.cumsum(var_ratio[:K]).tolist()
    }
    
    for k in range(K):
        pc_k_img = unpack_to_vector_image(U[:,k], idx, vol_shape, ref_iso)
        ants.image_write(pc_k_img, str(out_dir/f"pc_{k+1}.nii.gz"))
        print(f"   Saved: pc_{k+1}.nii.gz (variance explained: {var_ratio[k]:.1%})")
    
    with open(out_dir/"pca_meta.json","w") as f:
        json.dump(pcs_meta, f, indent=2)
    print(f"   Saved: pca_meta.json")

    # Synthesis: ±1 SD and ±2 SD for first two modes
    print("\n5. Synthesizing DVFs at ±1 SD and ±2 SD...")
    scale = (S / np.sqrt(max(1, X.shape[1]-1))).astype(np.float32)  # per-mode SD
    
    for k in range(min(2, K)):
        print(f"   PC {k+1} (SD = {scale[k]:.3f}):")
        for s in [-2.0, -1.0, 1.0, 2.0]:
            u_syn = mu + U[:,k] * (s * scale[k])
            u_img = unpack_to_vector_image(u_syn, idx, vol_shape, ref_iso)
            fname = f"pc{k+1}_{'m' if s<0 else 'p'}{int(abs(s))}sd.nii.gz"
            ants.image_write(u_img, str(out_dir/fname))
            print(f"      {fname}")

    print("\n" + "="*70)
    print("Phase 3 PCA COMPLETE")
    print("="*70)
    print(f"Output directory: {out_dir}")
    print(f"Principal components: {K}")
    print(f"Cumulative variance explained: {np.cumsum(var_ratio[:K]).tolist()}")
    print("="*70)

if __name__ == "__main__":
    main()
