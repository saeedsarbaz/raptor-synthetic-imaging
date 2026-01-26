"""Recover correct Forward Warps and compose cascade using SimpleITK"""
import sys
sys.path.insert(0, 'scripts')
from compute_phase70_qc import load_popi_landmarks, compute_tre_ants
from pathlib import Path
import os
import glob
import time
import SimpleITK as sitk
import numpy as np

def find_forward_warp(timewindow_start, timewindow_end):
    """Find *InverseWarp.nii.gz in TEMP within time window (Empirically correct)"""
    temp_dir = os.environ['TEMP']
    all_warps = glob.glob(os.path.join(temp_dir, '*InverseWarp.nii.gz'))
    candidates = []
    
    print(f"Searching InverseWarps between {time.ctime(timewindow_start)} and {time.ctime(timewindow_end)}")
    
    for f in all_warps:
        mtime = os.path.getmtime(f)
        if timewindow_start <= mtime <= timewindow_end:
            candidates.append(f)
            
    if not candidates:
        return None
        
    # Return latest in window
    return max(candidates, key=os.path.getmtime)

def run():
    print("="*60)
    print("RECOVER AND COMPOSE CASCADE (SimpleITK)")
    print("="*60)
    
    now = time.time()
    # 00->30 run finished recently
    warp_00_30 = find_forward_warp(now - 1800, now) # Actually InverseWarp
    
    if not warp_00_30:
        print("Error: Could not find 00->30 Inverse Warp!")
        return
        
    print(f"Found 00->30 Warp (v): {warp_00_30}")
    
    # Load 30->50 from saved file (which we know gave 2.62mm)
    path_u = "results/popi_ants_roi/dvf_30_to_50_FINAL.nii.gz"
    print(f"Loading existing 30->50 DVF (u): {path_u}")
    
    # Load with SITK
    print("\nLoading transforms...")
    # These are Displacement Fields.
    u_img = sitk.ReadImage(path_u) # 50->30
    v_img = sitk.ReadImage(warp_00_30) # 30->00
    
    # Create Transforms
    # Note: SITK DisplacementFieldTransform expects Double vectors.
    tx_u = sitk.DisplacementFieldTransform(sitk.Cast(u_img, sitk.sitkVectorFloat64))
    tx_v = sitk.DisplacementFieldTransform(sitk.Cast(v_img, sitk.sitkVectorFloat64))
    
    # Compose: T_total(x) = T_v( T_u(x) )
    # Input x (in 50) -> T_u(x) maps to 30 -> T_v(...) maps to 00.
    # Result is 50->00.
    print("Composing transforms...")
    composite_tx = sitk.CompositeTransform([tx_u, tx_v]) # Apply u then v? 
    # SITK internal order: T(x) = T0(T1(x))? Or T1(T0(x))?
    # Documentation says: "Points are transformed by the first transform in the list, then the next..."
    # So [tx_u, tx_v] -> tx_v(tx_u(x)). This is correct.
    
    # To get the Displacement Field of the composite:
    # We need to resample the composite transform onto the grid of 'u' (Phase 50).
    print("Resampling composite to DVF...")
    converter = sitk.TransformToDisplacementFieldFilter()
    converter.SetReferenceImage(u_img)
    dvf_total = converter.Execute(composite_tx)
    
    # Save 00->50
    final_path = "results/popi_ants_roi/dvf_00_to_50_FINAL.nii.gz"
    sitk.WriteImage(dvf_total, final_path)
    print(f"Saved composed DVF to: {final_path}")
    
    # Also save the Corrected 30->50 (if we found a better warp)
    fixed_30_path = "results/popi_ants_roi/dvf_30_to_50_CORRECTED.nii.gz"
    sitk.WriteImage(u_img, fixed_30_path)
    print(f"Saved Corrected 30->50 DVF: {fixed_30_path}")
    
    # Compute QC
    print("\nComputing QC (Phase 00->50)...")
    lm_50 = load_popi_landmarks('50')
    lm_00 = load_popi_landmarks('00')
    tre = compute_tre_ants(final_path, lm_50, lm_00)
    print(f"  TRE Median: {tre['median_mm']:.2f} mm")
    print(f"  TRE P95:    {tre['p95_mm']:.2f} mm")

if __name__ == "__main__":
    run()
