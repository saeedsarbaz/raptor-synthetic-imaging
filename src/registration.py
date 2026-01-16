"""
Image registration utilities using SimpleITK.
Implements deformable registration for medical images.
"""

import SimpleITK as sitk
import numpy as np
from typing import Tuple


def register_images_demons(fixed_img: np.ndarray, 
                           moving_img: np.ndarray,
                           n_iterations: int = 50,
                           sigma: float = 1.0) -> np.ndarray:
    """
    Register moving image to fixed image using Demons deformable registration.
    
    Args:
        fixed_img: Reference image (2D or 3D numpy array)
        moving_img: Image to be registered (same shape as fixed)
        n_iterations: Number of Demons iterations
        sigma: Smoothing sigma for deformation field
        
    Returns:
        Deformation vector field as numpy array with shape (*img.shape, ndim)
    """
    # Convert to SimpleITK images
    fixed = sitk.GetImageFromArray(fixed_img.astype(np.float32))
    moving = sitk.GetImageFromArray(moving_img.astype(np.float32))
    
    # Demons registration filter
    demons = sitk.DemonsRegistrationFilter()
    demons.SetNumberOfIterations(n_iterations)
    demons.SetStandardDeviations(sigma)
    
    # Execute registration
    displacement_field = demons.Execute(fixed, moving)
    
    # Convert back to numpy
    dvf = sitk.GetArrayFromImage(displacement_field)
    
    return dvf


def apply_deformation_field(image: np.ndarray, 
                            deformation_field: np.ndarray,
                            scale: float = 1.0) -> np.ndarray:
    """
    Apply deformation field to an image.
    
    Args:
        image: Input image (2D or 3D)
        deformation_field: Deformation vector field with shape (*image.shape, ndim)
        scale: Multiplier for deformation magnitude (0.5 = half deformation, 2.0 = double)
        
    Returns:
        Warped image (same shape as input)
    """
    # Scale deformation
    scaled_dvf = deformation_field * scale
    
    # Convert to SimpleITK
    img_sitk = sitk.GetImageFromArray(image.astype(np.float32))
    
    # Convert DVF to SimpleITK displacement field
    # DVF from Demons has shape (H, W, 2) for 2D or (D, H, W, 3) for 3D
    dvf_sitk = sitk.GetImageFromArray(scaled_dvf.astype(np.float64), isVector=True)
    dvf_sitk.CopyInformation(img_sitk)
    
    # Create displacement field transform
    displacement_transform = sitk.DisplacementFieldTransform(dvf_sitk)
    
    # Resample image using the transform
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(img_sitk)
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetDefaultPixelValue(0.0)
    resampler.SetTransform(displacement_transform)
    
    warped = resampler.Execute(img_sitk)
    
    return sitk.GetArrayFromImage(warped)


def compute_deformation_magnitude(deformation_field: np.ndarray) -> np.ndarray:
    """
    Compute magnitude of deformation at each pixel/voxel.
    
    Args:
        deformation_field: Deformation vector field
        
    Returns:
        Magnitude map (same spatial shape as input image)
    """
    # Compute L2 norm along the last axis (vector dimension)
    magnitude = np.linalg.norm(deformation_field, axis=-1)
    return magnitude


def register_image_pair(reference: np.ndarray, target: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Register target to reference and return both the warped image and deformation field.
    
    Args:
        reference: Fixed reference image
        target: Moving target image
        
    Returns:
        Tuple of (warped_image, deformation_field)
    """
    dvf = register_images_demons(reference, target)
    warped = apply_deformation_field(target, dvf, scale=1.0)
    
    return warped, dvf
