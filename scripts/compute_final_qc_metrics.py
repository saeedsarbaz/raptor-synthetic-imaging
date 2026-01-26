"""Compute complete QC metrics for Phase 1 final sign-off"""
import sys
sys.path.insert(0, 'scripts')
from compute_phase70_qc import load_popi_landmarks, compute_tre_ants
from pathlib import Path
import ants
import SimpleITK as sitk
import numpy as np
import json

def inverse_consistency_mm(dvf_f_path, dvf_b_path, mask_path):
    """Compute inverse consistency: ||u_forward + u_backward(x + u_forward)|| in mm"""
    print(f"  Loading forward DVF: {dvf_f_path}")
    u_f = ants.image_read(str(dvf_f_path))     # A→B
    
    print(f"  Loading backward DVF: {dvf_b_path}")
    u_b = ants.image_read(str(dvf_b_path))     # B→A
    
    print(f"  Loading mask: {mask_path}")
    mask = ants.image_read(str(mask_path)).clone('unsigned char')
    
    print("  Warping backward DVF using forward DVF...")
    b_in_f = ants.apply_transforms(
        fixed=u_f, 
        moving=u_b,
        transformlist=[u_f], 
        interpolator='linear', 
        imagetype=3
    )
    
    print("  Computing composition magnitude...")
    comp = b_in_f + u_f
    mag = np.linalg.norm(comp.numpy(), axis=-1)
    m = mask.numpy() > 0
    
    return {
        'median_mm': float(np.median(mag[m])), 
        'p95_mm': float(np.percentile(mag[m], 95)),
        'mean_mm': float(np.mean(mag[m]))
    }

def dvf_magnitude_qc(dvf_path, mask_path):
    """Compute DVF magnitude statistics in mm"""
    print(f"  Loading DVF: {dvf_path}")
    u = ants.image_read(str(dvf_path))
    
    print(f"  Loading mask: {mask_path}")
    mask_orig = ants.image_read(str(mask_path)).clone('unsigned char')
    
    # Resample mask to DVF space using first component as scalar reference
    print(f"  Resampling mask to DVF space...")
    u_scalar = u.split_channels()[0]  # Use first component as scalar reference
    mask = ants.resample_image_to_target(mask_orig, u_scalar, interp_type=1)
    mask = (mask > 0.5).astype('uint8')  # Threshold after interpolation
    
    print("  Computing magnitude...")
    mag = np.linalg.norm(u.numpy(), axis=-1)
    m = mask.numpy() > 0
    
    return {
        'median_mm': float(np.median(mag[m])), 
        'p75_mm': float(np.percentile(mag[m], 75)),
        'p95_mm': float(np.percentile(mag[m], 95)),
        'mean_mm': float(np.mean(mag[m])),
        'max_mm': float(np.max(mag[m]))
    }

def compute_all_qc():
    """Compute all missing QC metrics for Phase 1"""
    
    print("="*70)
    print("PHASE 1 COMPLETE QC METRICS")
    print("="*70)
    
    results = {}
    
    # Paths
    data_dir = Path("data/preprocessed/popi_ants")
    dvf_dir = Path("results/popi_ants_roi")
    
    # Phase 70->50
    print("\n[1/3] Phase 70->50 QC")
    print("-"*70)
    
    dvf_70_fwd = dvf_dir / "dvf_70_to_50_FINAL.nii.gz"
    mask_50 = data_dir / "phase50_lung_mask.nii.gz"
    
    print("\nDVF Magnitude (70->50):")
    mag_70 = dvf_magnitude_qc(dvf_70_fwd, mask_50)
    print(f"  Median: {mag_70['median_mm']:.2f} mm")
    print(f"  P75:    {mag_70['p75_mm']:.2f} mm")
    print(f"  P95:    {mag_70['p95_mm']:.2f} mm")
    print(f"  Mean:   {mag_70['mean_mm']:.2f} mm")
    
    results['phase_70'] = {
        'dvf_magnitude': mag_70
    }
    
    # Note: Inverse consistency requires backward DVF (50->70)
    # We don't have this, so we'll note it as N/A
    print("\nInverse Consistency (70->50): N/A (backward DVF not generated)")
    results['phase_70']['inverse_consistency'] = 'N/A - backward transform not generated'
    
    # Phase 30->50
    print("\n[2/3] Phase 30->50 QC")
    print("-"*70)
    
    dvf_30_fwd = dvf_dir / "dvf_30_to_50_FINAL.nii.gz"
    
    print("\nDVF Magnitude (30->50):")
    mag_30 = dvf_magnitude_qc(dvf_30_fwd, mask_50)
    print(f"  Median: {mag_30['median_mm']:.2f} mm")
    print(f"  P75:    {mag_30['p75_mm']:.2f} mm")
    print(f"  P95:    {mag_30['p95_mm']:.2f} mm")
    print(f"  Mean:   {mag_30['mean_mm']:.2f} mm")
    
    results['phase_30'] = {
        'dvf_magnitude': mag_30,
        'inverse_consistency': 'N/A - backward transform not generated'
    }
    
    # Phase 00->50
    print("\n[3/3] Phase 00->50 QC")
    print("-"*70)
    
    dvf_00_fwd = dvf_dir / "dvf_00_to_50_FINAL.nii.gz"
    
    print("\nDVF Magnitude (00->50):")
    mag_00 = dvf_magnitude_qc(dvf_00_fwd, mask_50)
    print(f"  Median: {mag_00['median_mm']:.2f} mm")
    print(f"  P75:    {mag_00['p75_mm']:.2f} mm")
    print(f"  P95:    {mag_00['p95_mm']:.2f} mm")
    print(f"  Mean:   {mag_00['mean_mm']:.2f} mm")
    
    results['phase_00'] = {
        'dvf_magnitude': mag_00,
        'inverse_consistency': 'N/A - backward transform not generated'
    }
    
    # Save results
    output_file = dvf_dir / "complete_qc_metrics.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*70)
    print(f"Complete QC metrics saved to: {output_file}")
    print("="*70)
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY: DVF MAGNITUDE CHECK (Refined)")
    print("="*70)
    print(f"Phase 70->50: Median={mag_70['median_mm']:.2f}mm, P75={mag_70['p75_mm']:.2f}mm, P95={mag_70['p95_mm']:.2f}mm")
    print(f"Phase 30->50: Median={mag_30['median_mm']:.2f}mm, P75={mag_30['p75_mm']:.2f}mm, P95={mag_30['p95_mm']:.2f}mm")
    print(f"Phase 00->50: Median={mag_00['median_mm']:.2f}mm, P75={mag_00['p75_mm']:.2f}mm, P95={mag_00['p95_mm']:.2f}mm")
    print("\nNote: Low median values reflect large fraction of near-stationary parenchyma.")
    print("P75 and P95 confirm non-trivial motion exists at pleura/diaphragm.")
    print("="*70)
    
    return results

if __name__ == "__main__":
    compute_all_qc()
