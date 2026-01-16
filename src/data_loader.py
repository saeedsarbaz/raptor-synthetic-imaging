"""
Data loading utilities for medical imaging.
Handles NIfTI format medical images from Medical Segmentation Decathlon dataset.
"""

import nibabel as nib
import numpy as np
from pathlib import Path
from typing import Tuple, List
import glob


def load_nifti_image(filepath: str) -> np.ndarray:
    """
    Load a NIfTI medical image and return as numpy array.
    
    Args:
        filepath: Path to .nii or .nii.gz file
        
    Returns:
        3D numpy array containing the image data
    """
    img = nib.load(filepath)
    return img.get_fdata()


def normalize_image(img: np.ndarray, percentile_clip: bool = True) -> np.ndarray:
    """
    Normalize image to [0, 1] range.
    
    Args:
        img: Input image array
        percentile_clip: If True, clip to 1st and 99th percentiles before normalizing
        
    Returns:
        Normalized image in [0, 1] range
    """
    if percentile_clip:
        lower = np.percentile(img, 1)
        upper = np.percentile(img, 99)
        img = np.clip(img, lower, upper)
    
    img = img - img.min()
    img = img / (img.max() + 1e-8)
    return img


def select_middle_slice(volume: np.ndarray, axis: int = 2) -> np.ndarray:
    """
    Extract middle 2D slice from 3D volume for visualization.
    
    Args:
        volume: 3D image volume
        axis: Axis along which to slice (0, 1, or 2)
        
    Returns:
        2D slice from the middle of the volume
    """
    mid_idx = volume.shape[axis] // 2
    if axis == 0:
        return volume[mid_idx, :, :]
    elif axis == 1:
        return volume[:, mid_idx, :]
    else:
        return volume[:, :, mid_idx]


def load_dataset_slices(data_dir: str, n_images: int = 20, normalize: bool = True,
                        target_size: Tuple[int, int] = None) -> List[np.ndarray]:
    """
    Load multiple medical images and extract middle slices.
    
    Args:
        data_dir: Directory containing .nii.gz files
        n_images: Number of images to load
        normalize: Whether to normalize images
        target_size: Optional (height, width) to resize all images to same size
        
    Returns:
        List of 2D image slices
    """
    # Find all NIfTI files
    pattern = str(Path(data_dir) / "*.nii.gz")
    image_paths = sorted(glob.glob(pattern))[:n_images]
    
    if len(image_paths) == 0:
        raise ValueError(f"No .nii.gz files found in {data_dir}")
    
    print(f"Loading {len(image_paths)} images from {data_dir}")
    
    slices = []
    for path in image_paths:
        volume = load_nifti_image(path)
        slice_2d = select_middle_slice(volume)
        
        if normalize:
            slice_2d = normalize_image(slice_2d)
        
        slices.append(slice_2d)
    
    # Check if all slices have same size
    shapes = [s.shape for s in slices]
    if len(set(shapes)) > 1:
        print(f"WARNING: Images have different sizes: {set(shapes)}")
        if target_size is None:
            # Use median size as target
            all_heights = [s.shape[0] for s in slices]
            all_widths = [s.shape[1] for s in slices]
            target_size = (int(np.median(all_heights)), int(np.median(all_widths)))
        
        print(f"Resizing all images to {target_size}")
        slices = [resize_image(s, target_size) for s in slices]
    
    print(f"Loaded {len(slices)} slices with shape {slices[0].shape}")
    return slices


def resize_image(img: np.ndarray, target_shape: Tuple[int, int]) -> np.ndarray:
    """
    Resize image to target shape using bilinear interpolation.
    
    Args:
        img: Input 2D image
        target_shape: (height, width) tuple
        
    Returns:
        Resized image
    """
    from skimage.transform import resize
    return resize(img, target_shape, order=1, preserve_range=True, anti_aliasing=True)
