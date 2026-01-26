"""
Compute QC metrics for Phase 70 -> 50 ANTs SyN registration.

Metrics:
1. TRE (Target Registration Error from landmarks)
2. Jacobian determinant (P01, P99, negative %)
3. DVF magnitude statistics
"""

import ants
import numpy as np
from pathlib import Path
import json

def load_popi_landmarks(phase):
    """
    Load POPI landmarks from .pts file.
    
    Returns:
        Nx3 array of landmarks in physical mm coordinates
    """
    lm_path = Path(f"data/raw/popi_4dct/{phase}-Landmarks.pts")
    
    if not lm_path.exists():
        raise FileNotFoundError(f"Landmarks not found: {lm_path}")
    
    # POPI .pts format: each line is "x y z"
    landmarks = []
    with open(lm_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                coords = line.split()
                if len(coords) >= 3:
                    landmarks.append([float(coords[0]), float(coords[1]), float(coords[2])])
    
    return np.array(landmarks)

def compute_tre_ants(dvf_path, fixed_landmarks, moving_landmarks):
    """
    Compute TRE using ANTs displacement field.
    
    Args:
        dvf_path: Path to DVF
        fixed_landmarks: Nx3 array (reference positions in mm)
        moving_landmarks: Nx3 array (original positions in mm)
    
    Returns:
        dict with median_mm, p95_mm, max_mm
    """
    dvf = ants.image_read(str(dvf_path))
    
    # Convert landmarks to voxel indices
    spacing = np.array(dvf.spacing)
    origin = np.array(dvf.origin)
    
    # Moving landmarks in voxel space
    mov_vox = (moving_landmarks - origin) / spacing
    
    # Sample DVF at moving landmark positions
    dvf_arr = dvf.numpy()  # Shape: (Z, Y, X, 3)
    
    # Interpolate DVF at each landmark
    warped_landmarks = []
    for i, lm_vox in enumerate(mov_vox):
        z, y, x = lm_vox
        
        # Trilinear interpolation
        z0, y0, x0 = int(np.floor(z)), int(np.floor(y)), int(np.floor(x))
        z1, y1, x1 = z0 + 1, y0 + 1, x0 + 1
        
        # Check bounds
        if (0 <= z0 < dvf_arr.shape[0]-1 and 
            0 <= y0 < dvf_arr.shape[1]-1 and 
            0 <= x0 < dvf_arr.shape[2]-1):
            
            # Trilinear weights
            dz, dy, dx = z - z0, y - y0, x - x0
            
            # Sample 8 corners
            c000 = dvf_arr[z0, y0, x0]
            c001 = dvf_arr[z0, y0, x1]
            c010 = dvf_arr[z0, y1, x0]
            c011 = dvf_arr[z0, y1, x1]
            c100 = dvf_arr[z1, y0, x0]
            c101 = dvf_arr[z1, y0, x1]
            c110 = dvf_arr[z1, y1, x0]
            c111 = dvf_arr[z1, y1, x1]
            
            # Interpolate
            c00 = c000 * (1-dx) + c001 * dx
            c01 = c010 * (1-dx) + c011 * dx
            c10 = c100 * (1-dx) + c101 * dx
            c11 = c110 * (1-dx) + c111 * dx
            
            c0 = c00 * (1-dy) + c01 * dy
            c1 = c10 * (1-dy) + c11 * dy
            
            displacement = c0 * (1-dz) + c1 * dz
            
            # Apply displacement
            warped_pos = moving_landmarks[i] + displacement
            warped_landmarks.append(warped_pos)
        else:
            # Out of bounds - use original position
            warped_landmarks.append(moving_landmarks[i])
    
    warped_landmarks = np.array(warped_landmarks)
    
    # Compute Euclidean errors
    errors = np.linalg.norm(warped_landmarks - fixed_landmarks, axis=1)
    
    return {
        'median_mm': float(np.median(errors)),
        'p95_mm': float(np.percentile(errors, 95)),
        'max_mm': float(errors.max()),
        'mean_mm': float(errors.mean()),
        'n_landmarks': len(errors)
    }

def compute_jacobian_stats_ants(dvf_path, mask_path=None):
    """
    Compute Jacobian determinant statistics.
    
    Uses SimpleITK for correct det(I + grad u) computation.
    
    Returns:
        dict with p01, p50, p99, pct_negative
    """
    import SimpleITK as sitk
    
    # Load DVF
    dvf_ants = ants.image_read(str(dvf_path))
    
    # Convert to SimpleITK for Jacobian computation
    # Write temp file and reload with SimpleITK
    temp_dvf = Path("results/popi_ants/temp_dvf_for_jac.nii.gz")
    ants.image_write(dvf_ants, str(temp_dvf))
    
    dvf_sitk = sitk.ReadImage(str(temp_dvf))
    
    # Compute Jacobian determinant (det(I + grad u))
    jac_sitk = sitk.DisplacementFieldJacobianDeterminant(dvf_sitk)
    
    # Get array
    jac_arr = sitk.GetArrayFromImage(jac_sitk)
    
    if mask_path and Path(mask_path).exists():
        # Load mask with SimpleITK to match Jacobian array shape
        mask_sitk = sitk.ReadImage(str(mask_path))
        mask_arr = sitk.GetArrayFromImage(mask_sitk)
        jac_masked = jac_arr[mask_arr > 0]
    else:
        jac_masked = jac_arr.flatten()
    
    neg_pct = float((jac_masked < 0).mean() * 100.0)
    
    # Clean up temp
    if temp_dvf.exists():
        temp_dvf.unlink()
    
    return {
        'min': float(jac_masked.min()),
        'p01': float(np.percentile(jac_masked, 1)),
        'p50': float(np.percentile(jac_masked, 50)),
        'p99': float(np.percentile(jac_masked, 99)),
        'max': float(jac_masked.max()),
        'pct_negative': neg_pct
    }

def compute_dvf_magnitude(dvf_path):
    """
    Compute DVF magnitude statistics.
    """
    dvf = ants.image_read(str(dvf_path))
    dvf_arr = dvf.numpy()
    
    mag = np.linalg.norm(dvf_arr, axis=-1)
    
    return {
        'median_mm': float(np.median(mag)),
        'p95_mm': float(np.percentile(mag, 95)),
        'max_mm': float(mag.max()),
        'mean_mm': float(mag.mean())
    }

def check_acceptance_criteria(metrics):
    """
    Check QC gates.
    
    Returns:
        (passed: bool, issues: list)
    """
    issues = []
    
    # TRE
    if metrics['tre']['median_mm'] > 2.5:
        issues.append(f"TRE median {metrics['tre']['median_mm']:.2f}mm > 2.5mm")
    if metrics['tre']['p95_mm'] > 5.0:
        issues.append(f"TRE P95 {metrics['tre']['p95_mm']:.2f}mm > 5.0mm")
    
    # Jacobian
    jac = metrics['jacobian']
    if jac['pct_negative'] > 0.5:
        issues.append(f"Negative Jac {jac['pct_negative']:.2f}% > 0.5%")
    if jac['p01'] < 0.8:
        issues.append(f"Jac P01 {jac['p01']:.3f} < 0.8")
    if jac['p99'] > 1.25:
        issues.append(f"Jac P99 {jac['p99']:.3f} > 1.25")
    
    # Motion check
    if metrics['dvf_magnitude']['median_mm'] < 0.5:
        issues.append(f"DVF magnitude {metrics['dvf_magnitude']['median_mm']:.2f}mm < 0.5mm (trivial)")
    
    return len(issues) == 0, issues

def main():
    print("\n" + "="*60)
    print("Phase 70 -> 50 QC Metrics")
    print("="*60 + "\n")
    
    # Paths
    dvf_path = "results/popi_ants/dvf_70_to_50.nii.gz"
    mask_path = "data/preprocessed/popi_ants/phase50_lung_mask.nii.gz"
    
    # 1. Load landmarks
    print("[1/4] Loading landmarks...")
    try:
        lm_50 = load_popi_landmarks("50")
        lm_70 = load_popi_landmarks("70")
        print(f"  Fixed (50): {len(lm_50)} landmarks")
        print(f"  Moving (70): {len(lm_70)} landmarks")
    except Exception as e:
        print(f"  ERROR: {e}")
        return
    
    # 2. Compute TRE
    print("\n[2/4] Computing TRE...")
    tre = compute_tre_ants(dvf_path, lm_50, lm_70)
    print(f"  Median: {tre['median_mm']:.2f} mm")
    print(f"  P95:    {tre['p95_mm']:.2f} mm")
    print(f"  Max:    {tre['max_mm']:.2f} mm")
    
    # 3. Compute Jacobian
    print("\n[3/4] Computing Jacobian...")
    jac = compute_jacobian_stats_ants(dvf_path, mask_path)
    print(f"  P01:      {jac['p01']:.3f}")
    print(f"  P50:      {jac['p50']:.3f}")
    print(f"  P99:      {jac['p99']:.3f}")
    print(f"  Negative: {jac['pct_negative']:.2f}%")
    
    # 4. DVF magnitude
    print("\n[4/4] Computing DVF magnitude...")
    dvf_mag = compute_dvf_magnitude(dvf_path)
    print(f"  Median: {dvf_mag['median_mm']:.2f} mm")
    print(f"  P95:    {dvf_mag['p95_mm']:.2f} mm")
    
    # Compile results
    metrics = {
        'phase': '70->50',
        'method': 'ANTs_SyN_whole_image',
        'tre': tre,
        'jacobian': jac,
        'dvf_magnitude': dvf_mag
    }
    
    # Check acceptance
    print("\n" + "="*60)
    print("QC Validation")
    print("="*60)
    
    passed, issues = check_acceptance_criteria(metrics)
    
    if passed:
        print("\n[PASS] ALL acceptance criteria met!")
    else:
        print("\n[FAIL] Issues found:")
        for issue in issues:
            print(f"  - {issue}")
    
    # Save results
    out_path = Path("results/popi_ants/metrics_70.json")
    with open(out_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\nMetrics saved: {out_path}")
    
    return metrics, passed

if __name__ == "__main__":
    main()
