"""
Quality metrics for evaluating synthetic medical images.
Implements SSIM, PSNR, and other image quality assessment metrics.
"""

import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
import pandas as pd
from typing import List, Dict


def compute_ssim(img1: np.ndarray, img2: np.ndarray) -> float:
    """
    Compute Structural Similarity Index between two images.
    
    Args:
        img1, img2: Images to compare (same shape)
        
    Returns:
        SSIM value in range [-1, 1], where 1 = identical
    """
    return ssim(img1, img2, data_range=img1.max() - img1.min())


def compute_psnr(img1: np.ndarray, img2: np.ndarray) -> float:
    """
    Compute Peak Signal-to-Noise Ratio between two images.
    
    Args:
        img1, img2: Images to compare (same shape)
        
    Returns:
        PSNR value in dB (higher is better)
    """
    return psnr(img1, img2, data_range=img1.max() - img1.min())


def compute_mae(img1: np.ndarray, img2: np.ndarray) -> float:
    """
    Compute Mean Absolute Error between two images.
    
    Args:
        img1, img2: Images to compare (same shape)
        
    Returns:
        MAE value (lower is better)
    """
    return np.mean(np.abs(img1 - img2))


def compute_rmse(img1: np.ndarray, img2: np.ndarray) -> float:
    """
    Compute Root Mean Squared Error between two images.
    
    Args:
        img1, img2: Images to compare (same shape)
        
    Returns:
        RMSE value (lower is better)
    """
    return np.sqrt(np.mean((img1 - img2) ** 2))


def evaluate_synthetic_images(reference: np.ndarray, 
                               synthetic_list: List[np.ndarray],
                               real_list: List[np.ndarray] = None) -> pd.DataFrame:
    """
    Comprehensive evaluation of synthetic images against reference.
    
    Computes multiple quality metrics for synthetic images and optionally
    compares to real anatomical variations.
    
    Args:
        reference: Reference image
        synthetic_list: List of synthetic images to evaluate
        real_list: Optional list of real images for baseline comparison
        
    Returns:
        DataFrame with metrics for each image
    """
    results = []
    
    # Evaluate synthetic images
    for i, synth in enumerate(synthetic_list):
        results.append({
            'image_id': f'synthetic_{i:03d}',
            'type': 'synthetic',
            'ssim': compute_ssim(reference, synth),
            'psnr': compute_psnr(reference, synth),
            'mae': compute_mae(reference, synth),
            'rmse': compute_rmse(reference, synth)
        })
    
    # Evaluate real images if provided (for baseline comparison)
    if real_list is not None:
        for i, real in enumerate(real_list):
            results.append({
                'image_id': f'real_{i:03d}',
                'type': 'real',
                'ssim': compute_ssim(reference, real),
                'psnr': compute_psnr(reference, real),
                'mae': compute_mae(reference, real),
                'rmse': compute_rmse(reference, real)
            })
    
    return pd.DataFrame(results)


def summarize_metrics(metrics_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute summary statistics grouped by image type.
    
    Args:
        metrics_df: DataFrame from evaluate_synthetic_images()
        
    Returns:
        Summary DataFrame with mean and std for each metric
    """
    summary = metrics_df.groupby('type')[['ssim', 'psnr', 'mae', 'rmse']].agg(['mean', 'std'])
    return summary


def print_metrics_summary(metrics_df: pd.DataFrame):
    """
    Print formatted summary of metrics.
    
    Args:
        metrics_df: DataFrame from evaluate_synthetic_images()
    """
    summary = summarize_metrics(metrics_df)
    
    print("\n" + "="*60)
    print("QUALITY METRICS SUMMARY")
    print("="*60)
    
    for img_type in summary.index:
        print(f"\n{img_type.upper()}:")
        print(f"  SSIM:  {summary.loc[img_type, ('ssim', 'mean')]:.3f} ± {summary.loc[img_type, ('ssim', 'std')]:.3f}")
        print(f"  PSNR:  {summary.loc[img_type, ('psnr', 'mean')]:.2f} ± {summary.loc[img_type, ('psnr', 'std')]:.2f} dB")
        print(f"  MAE:   {summary.loc[img_type, ('mae', 'mean')]:.4f} ± {summary.loc[img_type, ('mae', 'std')]:.4f}")
        print(f"  RMSE:  {summary.loc[img_type, ('rmse', 'mean')]:.4f} ± {summary.loc[img_type, ('rmse', 'std')]:.4f}")
    
    print("\n" + "="*60)
