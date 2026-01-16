"""
Visualization utilities for medical images and results.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple
import seaborn as sns


def create_comparison_grid(reference: np.ndarray, 
                           synthetic_images: List[np.ndarray],
                           n_cols: int = 3,
                           figsize: Tuple[int, int] = (12, 10)) -> plt.Figure:
    """
    Create a grid showing reference image and synthetic variations.
    
    Args:
        reference: Reference image
        synthetic_images: List of synthetic images
        n_cols: Number of columns in grid
        figsize: Figure size
        
    Returns:
        Matplotlib figure
    """
    n_synth = len(synthetic_images)
    n_rows = int(np.ceil((n_synth + 1) / n_cols))
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten()
    
    # Plot reference
    axes[0].imshow(reference, cmap='gray')
    axes[0].set_title('Reference Image', fontsize=12, fontweight='bold', color='blue')
    axes[0].axis('off')
    
    # Plot synthetic images
    for i, synth_img in enumerate(synthetic_images):
        axes[i+1].imshow(synth_img, cmap='gray')
        axes[i+1].set_title(f'Synthetic #{i+1}', fontsize=10)
        axes[i+1].axis('off')
    
    # Hide unused subplots
    for i in range(n_synth + 1, len(axes)):
        axes[i].axis('off')
    
    plt.tight_layout()
    return fig


def plot_metrics_comparison(metrics_df, save_path: str = None):
    """
    Create box plots comparing metrics for synthetic vs real images.
    
    Args:
        metrics_df: DataFrame from evaluate_synthetic_images()
        save_path: Optional path to save figure
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    metrics = ['ssim', 'psnr', 'mae', 'rmse']
    titles = ['SSIM (higher is better)', 'PSNR (dB, higher is better)', 
              'MAE (lower is better)', 'RMSE (lower is better)']
    
    for ax, metric, title in zip(axes.flatten(), metrics, titles):
        sns.boxplot(data=metrics_df, x='type', y=metric, ax=ax)
        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.set_xlabel('')
        ax.set_ylabel(metric.upper(), fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def plot_deformation_magnitude(deformation_field: np.ndarray, 
                                original_image: np.ndarray = None,
                                figsize: Tuple[int, int] = (12, 5)) -> plt.Figure:
    """
    Visualize deformation field magnitude.
    
    Args:
        deformation_field: Deformation vector field
        original_image: Optional original image to overlay
        figsize: Figure size
        
    Returns:
        Matplotlib figure
    """
    magnitude = np.linalg.norm(deformation_field, axis=-1)
    
    if original_image is not None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        ax1.imshow(original_image, cmap='gray')
        ax1.set_title('Original Image')
        ax1.axis('off')
        
        im = ax2.imshow(magnitude, cmap='hot')
        ax2.set_title('Deformation Magnitude')
        ax2.axis('off')
        plt.colorbar(im, ax=ax2, label='Displacement (pixels)')
    else:
        fig, ax = plt.subplots(1, 1, figsize=(6, 5))
        im = ax.imshow(magnitude, cmap='hot')
        ax.set_title('Deformation Magnitude')
        ax.axis('off')
        plt.colorbar(im, ax=ax, label='Displacement (pixels)')
    
    plt.tight_layout()
    return fig


def save_figure(fig: plt.Figure, filepath: str, dpi: int = 300):
    """
    Save figure with high quality.
    
    Args:
        fig: Matplotlib figure
        filepath: Output file path
        dpi: Resolution in dots per inch
    """
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight', facecolor='white')
    print(f"Saved figure to: {filepath}")
