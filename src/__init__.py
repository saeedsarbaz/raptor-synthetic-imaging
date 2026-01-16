"""
RAPTORplus Synthetic Image Generation Package

Proof-of-concept implementation for Task 1 of the RAPTORplus PhD project.
"""

__version__ = "0.1.0"
__author__ = "Saeed Sarbazzadeh Khosroshahi"

from .data_loader import load_nifti_image, normalize_image, load_dataset_slices
from .registration import register_images_demons, apply_deformation_field
from .deformation_generator import SyntheticImageGenerator
from .quality_metrics import (compute_ssim, compute_psnr, compute_mae, 
                              evaluate_synthetic_images, summarize_metrics)
from .visualization import create_comparison_grid, plot_metrics_comparison

__all__ = [
    'load_nifti_image',
    'normalize_image',
    'load_dataset_slices',
    'register_images_demons',
    'apply_deformation_field',
    'SyntheticImageGenerator',
    'compute_ssim',
    'compute_psnr',
    'compute_mae',
    'evaluate_synthetic_images',
    'summarize_metrics',
    'create_comparison_grid',
    'plot_metrics_comparison',
]
