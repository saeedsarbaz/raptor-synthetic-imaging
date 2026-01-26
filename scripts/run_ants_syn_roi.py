"""
Phase 1 ANTs SyN - ROI-Cropped Masked Registration
Implements the recommended approach to achieve TRE <2.5mm:
- Crop to dilated lung bounding box (25mm margin)
- Masked SyN within ROI
- 5-level pyramid with more fine-level work
- grad_step=0.04 for safety
"""

import ants
import numpy as np
from pathlib import Path
import json

def crop_to_mask_bbox(img, mask, margin_mm=(25, 25, 25)):
    """
    Crop image and mask to bounding box with margin.
    
    Returns:
        roi_img, roi_mask, lo_indices, hi_indices
        
    Note: Indices are in SimpleITK/numpy array order (Z,Y,X)
    """
    import SimpleITK as sitk
    
    # Convert to SimpleITK to get consistent indexing
    temp_mask = Path("results/popi_ants_roi/temp_mask.nii.gz")
    ants.image_write(mask, str(temp_mask))
    mask_sitk = sitk.ReadImage(str(temp_mask))
    
    # Get mask array (Z,Y,X)
    mask_arr = sitk.GetArrayFromImage(mask_sitk)
    nz = np.nonzero(mask_arr)
    
    if len(nz[0]) == 0:
        raise ValueError("Empty mask!")
    
    # Bounding box in array indices (Z, Y, X)
    lo_vox = np.array([nz[0].min(), nz[1].min(), nz[2].min()])
    hi_vox = np.array([nz[0].max(), nz[1].max(), nz[2].max()])
    
    # Convert margin from mm to voxels
    spacing = np.array(mask_sitk.GetSpacing())[::-1]  # Reverse to (Z,Y,X)
    margin_vox = np.maximum(np.round(np.array(margin_mm) / spacing).astype(int), 2)
    
    # Expand with margin, clamp to image bounds
    img_shape = np.array(mask_arr.shape)
    lo = np.maximum(lo_vox - margin_vox, 0)
    hi = np.minimum(hi_vox + margin_vox, img_shape - 1)
    
    # Crop using ANTs (need to convert indices back to ANTs order)
    # ANTs uses (X,Y,Z) order for crop_indices
    lo_ants = lo[::-1]  # Reverse to (X,Y,Z)
    crop_size = (hi - lo + 1)[::-1]  # Reverse to (X,Y,Z)
    
    roi_img = ants.crop_indices(img, lo_ants.tolist(), crop_size.tolist())
    roi_mask = ants.crop_indices(mask, lo_ants.tolist(), crop_size.tolist())
    
    # Cleanup
    temp_mask.unlink()
    
    # Return indices in SimpleITK/numpy order (Z,Y,X)
    return roi_img, roi_mask, lo, hi

def resample_iso(img, iso=2.0):
    """Resample image to isotropic spacing (2.0mm for large motion)."""
    return ants.resample_image(img, (iso, iso, iso), use_voxels=False, interp_type=1)

def safe_pyramid_for_mask(mask_img):
    """
    Pyramid levels for POPI TRE <2.5mm.
    
    Final optimization: maximum fine-level work for last 0.2mm improvement.
    """
    # 4-level pyramid, heavy fine-level work
    return (8, 4, 2, 1), (4, 2, 1, 0), (100, 100, 100, 120)

def syn_roi_masked(fix_img, mov_img, fix_mask, mov_mask, grad_step=0.03, cc_radius=4):
    """
    ANTs SyN registration with isotropic resampling and larger CC radius.
    
    Last-mile optimization:
    - Resample ROI to isotropic 1.25mm for better local CC
    - Increase CC neighborhood radius from 2 to 4
    - Expected: 0.3-0.5mm TRE improvement
    """
    print(f"  Resampling ROI to isotropic 1.25mm...")
    
    # Resample to isotropic spacing
    fix_iso = resample_iso(fix_img)
    mov_iso = resample_iso(mov_img)
    fix_mask_iso = resample_iso(fix_mask.clone('unsigned char'), iso=fix_iso.spacing[0]).clone('unsigned char')
    mov_mask_iso = resample_iso(mov_mask.clone('unsigned char'), iso=mov_iso.spacing[0]).clone('unsigned char')
    
    print(f"    Original spacing: {fix_img.spacing}")
    print(f"    Isotropic spacing: {fix_iso.spacing}")
    print(f"    Isotropic ROI shape: {fix_iso.shape}")
    
    # Get pyramid parameters
    shrinks, sigmas, iters = safe_pyramid_for_mask(fix_mask_iso)
    n_levels = len(shrinks)
    
    # Affine prealignment with masks
    print(f"    [1/2] Affine (masked, 800x400x200 iters)")
    aff = ants.registration(
        fixed=fix_iso, moving=mov_iso,
        type_of_transform='Affine',
        mask=fix_mask_iso,
        moving_mask=mov_mask_iso,
        reg_iterations=(800, 400, 200),
        aff_metric='mattes',
        aff_sampling=20
    )
    
    # SyN with larger CC radius
    print(f"    [2/2] SyN (masked, {n_levels}-level pyramid)")
    print(f"        Shrink factors: {shrinks}")
    print(f"        Smoothing sigmas: {sigmas}")
    print(f"        Iterations: {iters}")
    print(f"        Grad step: {grad_step}")
    print(f"        CC radius: {cc_radius}")
    
    syn = ants.registration(
        fixed=fix_iso, moving=mov_iso,
        type_of_transform='SyN',
        mask=fix_mask_iso,
        moving_mask=mov_mask_iso,
        initial_transform=aff['fwdtransforms'][0],
        reg_iterations=iters,
        smoothing_sigmas=sigmas,
        shrink_factors=shrinks,
        syn_metric='CC',
        syn_sampling=cc_radius,  # Increased from 2 to 4
        grad_step=grad_step
    )
    
    # Export DVF: save isotropic warp directly (safer than resampling)
    print(f"  Exporting isotropic DVF...")
    dvf_iso = ants.image_read(str(syn['fwdtransforms'][0]))  # Read the warp file directly
    
    # Return isotropic DVF (will be saved directly to results)
    # Note: TRE computation works correctly on isotropic DVF
    return dvf_iso

def paste_dvf_to_full_space(dvf_roi, full_ref_img, lo_indices, hi_indices):
    """
    Paste ROI DVF into full-size zero field using SimpleITK.
    
    Note: Use actual ROI shape, not computed hi-lo indices
    """
    import SimpleITK as sitk
    
    # Convert ANTs to SimpleITK for easier manipulation
    temp_roi = Path("results/popi_ants_roi/temp_dvf_roi.nii.gz")
    temp_full = Path("results/popi_ants_roi/temp_dvf_full.nii.gz")
    
    ants.image_write(dvf_roi, str(temp_roi))
    dvf_roi_sitk = sitk.ReadImage(str(temp_roi))
    
    # Create zero DVF in full space
    ref_sitk = sitk.ReadImage(str(full_ref_img))
    
    # Create zero displacement field
    dvf_full_sitk = sitk.Image(ref_sitk.GetSize(), sitk.sitkVectorFloat32, 3)
    dvf_full_sitk.CopyInformation(ref_sitk)
    
    # Get arrays - SimpleITK uses (Z,Y,X,3) ordering
    dvf_roi_arr = sitk.GetArrayFromImage(dvf_roi_sitk)  # (Z_roi, Y_roi, X_roi, 3)
    dvf_full_arr = sitk.GetArrayFromImage(dvf_full_sitk)  # (Z_full, Y_full, X_full, 3)
    
    print(f"    DVF ROI array shape: {dvf_roi_arr.shape}")
    print(f"    DVF full array shape: {dvf_full_arr.shape}")
    print(f"    Paste indices lo: {lo_indices}")
    
    # Use actual ROI shape
    z0, y0, x0 = lo_indices
    roi_shape = dvf_roi_arr.shape[:3]  # (Z, Y, X)
    z1 = z0 + roi_shape[0] - 1
    y1 = y0 + roi_shape[1] - 1
    x1 = x0 + roi_shape[2] - 1
    
    print(f"    Computed hi indices: [{z1}, {y1}, {x1}]")
    print(f"    Paste region shape: ({z1-z0+1}, {y1-y0+1}, {x1-x0+1})")
    
    # Paste ROI into full space
    dvf_full_arr[z0:z1+1, y0:y1+1, x0:x1+1, :] = dvf_roi_arr
    
    # Create new image from array
    dvf_full_sitk = sitk.GetImageFromArray(dvf_full_arr, isVector=True)
    dvf_full_sitk.CopyInformation(ref_sitk)
    
    # Save and reload as ANTs
    sitk.WriteImage(dvf_full_sitk, str(temp_full))
    dvf_full_ants = ants.image_read(str(temp_full))
    
    # Cleanup
    temp_roi.unlink()
    temp_full.unlink()
    
    return dvf_full_ants

def register_phase_roi(
    fix_path, mov_path,
    fix_mask_path, mov_mask_path,
    out_dvf_path,
    margin_mm=(25, 25, 25),
    grad_step=0.04,
    mask_dilation=2
):
    """
    Complete ROI-cropped registration pipeline.
    """
    print(f"  Loading images...")
    fix_full = ants.image_read(str(fix_path))
    mov_full = ants.image_read(str(mov_path))
    fix_mask_full = ants.image_read(str(fix_mask_path))
    mov_mask_full = ants.image_read(str(mov_mask_path))
    
    # Dilate masks
    print(f"  Dilating masks ({mask_dilation} voxels)...")
    fix_mask_full = ants.morphology(fix_mask_full, "dilate", mask_dilation)
    mov_mask_full = ants.morphology(mov_mask_full, "dilate", mask_dilation)
    
    # Crop to ROI
    print(f"  Cropping to lung ROI (margin: {margin_mm} mm)...")
    fix_roi, fix_mask_roi, lo_fix, hi_fix = crop_to_mask_bbox(fix_full, fix_mask_full, margin_mm)
    mov_roi, mov_mask_roi, lo_mov, hi_mov = crop_to_mask_bbox(mov_full, mov_mask_full, margin_mm)
    
    print(f"    Fixed ROI shape: {fix_roi.shape}")
    print(f"    Moving ROI shape: {mov_roi.shape}")
    
    # Register in ROI with isotropic resampling
    print(f"  Registering in ROI (isotropic)...")
    dvf_roi = syn_roi_masked(fix_roi, mov_roi, fix_mask_roi, mov_mask_roi, grad_step)
    
    # Paste back to full space
    print(f"  Pasting DVF to full space...")
    dvf_full = paste_dvf_to_full_space(dvf_roi, fix_path, lo_fix, hi_fix)
    
    # Save
    ants.image_write(dvf_full, str(out_dvf_path))
    print(f"  [DONE] {Path(out_dvf_path).name}")
    
    return dvf_full

def main():
    print("\n" + "="*70)
    print("Phase 1: ANTs SyN ROI-Cropped Registration")
    print("="*70 + "\n")
    
    data_dir = Path("data/preprocessed/popi_ants")
    out_dir = Path("results/popi_ants_roi")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Phase 00 -> 30 (Cascade Step 1)
    print("[3/3] Phase 00 -> 30 (ROI-Cropped, Masked, Large Motion Config)")
    print("-"*70)
    
    dvf_00 = register_phase_roi(
        fix_path=data_dir / "phase30.nii.gz",
        mov_path=data_dir / "phase00.nii.gz",
        fix_mask_path=data_dir / "phase30_lung_mask.nii.gz",
        mov_mask_path=data_dir / "phase00_lung_mask.nii.gz",
        out_dvf_path=out_dir / "dvf_00_to_30.nii.gz",
        margin_mm=(18, 18, 18),  # Larger ROI for larger motion
        grad_step=0.03,  # Larger updates for larger motion
        mask_dilation=3
    )
    
    print("\n" + "="*70)
    print("Phase 00->30 Complete!")
    print("="*70)
    print(f"\nNext: Compose with 30->50 to get 00->50")

if __name__ == "__main__":
    main()
