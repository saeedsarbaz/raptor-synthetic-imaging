#!/usr/bin/env python3
"""
Phase 2 Step 1 CORRECTED FINAL: Generate Synthetic Images
Fix: Warp in DVF grid (use scalar component for resampling, pass DVF path to apply_transforms)
"""
import ants
from pathlib import Path
import json
import sys

def generate_in_fixed_grid(moving_img_path, fixed_img_path, dvf_path, out_path):
    """
    Generate synthetic by warping in DVF grid
    
    Key fixes:
    1. Extract scalar component from DVF for resampling target
    2. Resample fixed image to DVF grid
    3. Pass DVF PATH (not object) to apply_transforms
    """
    print(f"  Loading fixed: {fixed_img_path.name}")
    fixed_native = ants.image_read(str(fixed_img_path))
    
    print(f"  Loading DVF: {dvf_path.name}")
    dvf = ants.image_read(str(dvf_path))
    print(f"    DVF grid: {dvf.shape}, spacing={dvf.spacing}")

    # Extract scalar component as resampling reference
    print(f"  Extracting scalar reference from DVF...")
    dvf_scalar = dvf.split_channels()[0]

    # Resample fixed image to DVF grid
    print(f"  Resampling fixed to DVF grid...")
    fixed_in_dvf_grid = ants.resample_image_to_target(fixed_native, dvf_scalar, interp_type=1)
    print(f"    Resampled: {fixed_in_dvf_grid.shape}, spacing={fixed_in_dvf_grid.spacing}")

    print(f"  Loading moving: {moving_img_path.name}")
    moving = ants.image_read(str(moving_img_path))
    
    # Apply forward DVF using DVF PATH (not object)
    print(f"  Applying transformation...")
    warped = ants.apply_transforms(
        fixed=fixed_in_dvf_grid,
        moving=moving,
        transformlist=[str(dvf_path)],  # CRITICAL: pass path string, not object
        interpolator='linear'
    )
    
    print(f"  Saving: {out_path.name}")
    ants.image_write(warped, str(out_path))
    print(f"  [DONE]")
    return fixed_in_dvf_grid

def main():
    print("="*70)
    print("Phase 2 Step 1 CORRECTED: Generate Synthetic Images")
    print("Fix: Warp in DVF grid for metric accuracy")
    print("="*70)
    
    data_dir = Path("data/preprocessed/popi_ants")
    dvf_dir  = Path("results/popi_ants_roi")
    out_dir  = Path("results/synthetic")
    out_dir.mkdir(parents=True, exist_ok=True)

    fixed50 = data_dir / "phase50.nii.gz"
    phase70 = data_dir / "phase70.nii.gz"
    phase30 = data_dir / "phase30.nii.gz"
    phase00 = data_dir / "phase00.nii.gz"

    dvf_70_50 = dvf_dir / "dvf_70_to_50_FINAL.nii.gz"
    dvf_30_50 = dvf_dir / "dvf_30_to_50_FINAL.nii.gz"
    dvf_00_50 = dvf_dir / "dvf_00_to_50_FINAL.nii.gz"

    # Verify all files
    print("\nVerifying inputs...")
    for p in [fixed50, phase70, phase30, phase00, dvf_70_50, dvf_30_50, dvf_00_50]:
        if not p.exists():
            print(f"ERROR missing: {p}", file=sys.stderr)
            sys.exit(1)
        print(f"  [OK] {p.name}")

    # Generate synthetics aligned to DVF grid (iso)
    print("\n[1/3] Phase 70 to 50 (in DVF grid)")
    print("-"*70)
    fixed_iso = generate_in_fixed_grid(phase70, fixed50, dvf_70_50, out_dir/"phase70_in_50.nii.gz")
    
    print("\n[2/3] Phase 30 to 50 (in DVF grid)")
    print("-"*70)
    _ = generate_in_fixed_grid(phase30, fixed50, dvf_30_50, out_dir/"phase30_in_50.nii.gz")
    
    print("\n[3/3] Phase 00 to 50 (in DVF grid)")
    print("-"*70)
    _ = generate_in_fixed_grid(phase00, fixed50, dvf_00_50, out_dir/"phase00_in_50.nii.gz")

    # Save the fixed image resampled to iso grid for fair comparison
    print("\nSaving phase50 in DVF grid for validation...")
    ants.image_write(fixed_iso, str(out_dir/"phase50_iso_like_dvf.nii.gz"))

    # Save manifest
    with open(out_dir/"synthetic_outputs.json","w") as f:
        json.dump({
            "phase50_iso_like_dvf": str(out_dir/"phase50_iso_like_dvf.nii.gz"),
            "phase70_in_50": str(out_dir/"phase70_in_50.nii.gz"),
            "phase30_in_50": str(out_dir/"phase30_in_50.nii.gz"),
            "phase00_in_50": str(out_dir/"phase00_in_50.nii.gz")
        }, f, indent=2)

    print("\n" + "="*70)
    print("Synthetic generation COMPLETE")
    print("="*70)
    print("Files generated:")
    print("  - phase50_iso_like_dvf.nii.gz (reference in DVF grid)")
    print("  - phase70_in_50.nii.gz")
    print("  - phase30_in_50.nii.gz")
    print("  - phase00_in_50.nii.gz")

if __name__ == "__main__":
    main()
