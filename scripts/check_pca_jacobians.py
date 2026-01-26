#!/usr/bin/env python3
"""
Phase 3 QC: Jacobian safety check for synthesized DVFs
"""
import ants
import numpy as np
import json
from pathlib import Path
import SimpleITK as sitk

def jacobian_qc(warp_path, ref_iso_path, mask_path):
    """Compute Jacobian determinant QC metrics for a DVF"""
    # Load reference and mask
    ref = ants.image_read(str(ref_iso_path))
    mask = ants.image_read(str(mask_path)).clone('unsigned char')
    mask = ants.apply_transforms(
        fixed=ref,
        moving=mask,
        transformlist=[],
        interpolator='nearestNeighbor'
    ).clone('unsigned char')
    
    # Compute Jacobian using SimpleITK (more reliable)
    dvf_sitk = sitk.ReadImage(str(warp_path))
    jac = sitk.DisplacementFieldJacobianDeterminant(dvf_sitk)
    
    # Extract masked values
    jac_arr = sitk.GetArrayFromImage(jac).flatten()
    mask_arr = mask.numpy().flatten() > 0
    vals = jac_arr[mask_arr].astype(np.float32)
    
    # Compute stats
    neg = float((vals < 0).mean() * 100.0)
    
    return {
        'p01': float(np.percentile(vals, 1)),
        'p50': float(np.median(vals)),
        'p99': float(np.percentile(vals, 99)),
        'neg_percent': neg,
        'min': float(vals.min()),
        'max': float(vals.max())
    }

def main():
    print("="*70)
    print("Phase 3 QC: Jacobian Safety Check")
    print("="*70)
    
    ref_iso = "results/synthetic/phase50_iso_like_dvf.nii.gz"
    mask50 = "data/preprocessed/popi_ants/phase50_lung_mask.nii.gz"
    pca_dir = Path("results/pca")
    
    # Check all synthesized DVFs
    print("\nChecking synthesized DVFs at ±1 SD and ±2 SD...")
    print("-"*70)
    
    results = {}
    sd_files = sorted(pca_dir.glob("pc*_*sd.nii.gz"))
    
    for dvf_path in sd_files:
        print(f"\n{dvf_path.name}:")
        try:
            qc = jacobian_qc(dvf_path, ref_iso, mask50)
            results[dvf_path.name] = qc
            
            # Print results
            print(f"  Jacobian P01: {qc['p01']:.3f}")
            print(f"  Jacobian P50: {qc['p50']:.3f}")
            print(f"  Jacobian P99: {qc['p99']:.3f}")
            print(f"  Negative %:   {qc['neg_percent']:.2f}%")
            print(f"  Range: [{qc['min']:.3f}, {qc['max']:.3f}]")
            
            # Check safety
            passed = (qc['neg_percent'] < 0.5 and 
                     qc['p01'] > 0.80 and 
                     qc['p99'] < 1.25)
            print(f"  Safety: {'[PASS]' if passed else '[FAIL]'}")
            
        except Exception as e:
            print(f"  ERROR: {e}")
            results[dvf_path.name] = {"error": str(e)}
    
    # Save results
    out_json = pca_dir / "jacobian_qc.json"
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*70)
    print(f"Results saved to: {out_json}")
    print("="*70)

if __name__ == "__main__":
    main()
