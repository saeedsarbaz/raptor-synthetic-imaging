"""
Simulate biological response (tumor shrinkage) for proof-of-concept.
Addresses reviewer feedback: "PoC lacks biological response modeling"

This script demonstrates the capability to model biological changes
(tumor regression) in addition to anatomical deformations.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from data_loader import load_dataset_slices
except ImportError:
    import data_loader
    load_dataset_slices = data_loader.load_dataset_slices


def create_synthetic_tumor(image_shape, center, size, intensity=0.8):
    """
    Create a synthetic tumor region in an image.
    
    Args:
        image_shape: Shape of the image
        center: (y, x) coordinates of tumor center
        size: (height, width) of tumor region
        intensity: Relative intensity of tumor (0-1)
    
    Returns:
        tumor_mask: Binary mask of tumor region
    """
    mask = np.zeros(image_shape, dtype=float)
    
    y, x = center
    h, w = size
    
    # Create elliptical tumor region
    y_min = max(0, y - h//2)
    y_max = min(image_shape[0], y + h//2)
    x_min = max(0, x - w//2)
    x_max = min(image_shape[1], x + w//2)
    
    for i in range(y_min, y_max):
        for j in range(x_min, x_max):
            # Ellipse equation
            dy = (i - y) / (h/2)
            dx = (j - x) / (w/2)
            if dy**2 + dx**2 <= 1:
                mask[i, j] = intensity
    
    # Smooth edges
    mask = gaussian_filter(mask, sigma=1.0)
    
    return mask


def simulate_tumor_response(baseline_image, tumor_center, tumor_size, 
                            shrinkage_factor=0.5, intensity_change=-0.3):
    """
    Simulate tumor response to treatment (shrinkage and intensity change).
    
    Args:
        baseline_image: Original image with tumor
        tumor_center: (y, x) coordinates of tumor center
        tumor_size: (height, width) of initial tumor
        shrinkage_factor: Fraction to shrink (0.5 = 50% reduction)
        intensity_change: Change in tumor intensity (negative = darker)
    
    Returns:
        baseline_with_tumor: Image with synthetic tumor
        followup_image: Image after simulated response
        tumor_mask_before: Initial tumor mask
        tumor_mask_after: Residual tumor mask
    """
    # Create initial tumor
    tumor_mask_before = create_synthetic_tumor(
        baseline_image.shape, 
        tumor_center, 
        tumor_size, 
        intensity=0.8
    )
    
    # Add tumor to baseline
    baseline_with_tumor = baseline_image.copy()
    baseline_with_tumor = baseline_with_tumor + tumor_mask_before * 0.3
    baseline_with_tumor = np.clip(baseline_with_tumor, 0, 1)
    
    # Create shrunken tumor
    new_size = (int(tumor_size[0] * shrinkage_factor), 
                int(tumor_size[1] * shrinkage_factor))
    
    tumor_mask_after = create_synthetic_tumor(
        baseline_image.shape,
        tumor_center,
        new_size,
        intensity=0.8 + intensity_change
    )
    
    # Create follow-up image
    followup_image = baseline_image.copy()
    followup_image = followup_image + tumor_mask_after * 0.2
    followup_image = np.clip(followup_image, 0, 1)
    
    return baseline_with_tumor, followup_image, tumor_mask_before, tumor_mask_after


def create_comparison_figure(baseline, followup, mask_before, mask_after, 
                             output_path):
    """
    Create before/after comparison figure showing tumor response.
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Row 1: Before treatment
    axes[0, 0].imshow(baseline, cmap='gray')
    axes[0, 0].set_title('Baseline Image\n(With Synthetic Tumor)', fontsize=14, fontweight='bold')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(mask_before, cmap='hot', alpha=0.8)
    axes[0, 1].set_title('Tumor Region\n(Initial Volume)', fontsize=14, fontweight='bold')
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(baseline, cmap='gray')
    axes[0, 2].imshow(mask_before, cmap='hot', alpha=0.4)
    axes[0, 2].set_title('Overlay View\n(Baseline)', fontsize=14, fontweight='bold')
    axes[0, 2].axis('off')
    
    # Row 2: After treatment response
    axes[1, 0].imshow(followup, cmap='gray')
    axes[1, 0].set_title('Follow-up Image\n(After Treatment Response)', fontsize=14, fontweight='bold')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(mask_after, cmap='hot', alpha=0.8)
    axes[1, 1].set_title('Residual Tumor\n(50% Volume Reduction)', fontsize=14, fontweight='bold')
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(followup, cmap='gray')
    axes[1, 2].imshow(mask_after, cmap='hot', alpha=0.4)
    axes[1, 2].set_title('Overlay View\n(Follow-up)', fontsize=14, fontweight='bold')
    axes[1, 2].axis('off')
    
    # Overall title
    fig.suptitle('Simulated Biological Response: Tumor Regression During Treatment', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Add metrics annotation
    volume_before = np.sum(mask_before > 0.1)
    volume_after = np.sum(mask_after > 0.1)
    reduction_pct = (1 - volume_after/volume_before) * 100
    
    fig.text(0.5, 0.02, 
             f'Quantitative Metrics: Volume Reduction = {reduction_pct:.1f}% | '
             f'Initial Volume = {volume_before} pixels | Residual Volume = {volume_after} pixels',
             ha='center', fontsize=12, style='italic')
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved comparison figure to: {output_path}")
    
    return fig


if __name__ == "__main__":
    print("="*60)
    print("Biological Response Simulation (Tumor Shrinkage)")
    print("="*60)
    
    # Load a sample brain MRI
    data_dir = Path(__file__).parent.parent / "data" / "Task04_Hippocampus" / "Task04_Hippocampus" / "imagesTr"
    print(f"\nLoading sample MRI from: {data_dir}")
    
    slices = load_dataset_slices(str(data_dir), n_images=1, normalize=True)
    baseline = slices[0]
    
    print(f"Image shape: {baseline.shape}")
    
    # Define tumor parameters
    # Place tumor in a visually prominent region
    image_center = (baseline.shape[0] // 2, baseline.shape[1] // 2)
    tumor_size = (12, 16)  # Height, Width in pixels
    
    print(f"\nSimulating tumor at center {image_center} with size {tumor_size}")
    print("Applying 50% volume reduction (treatment response)")
    
    # Simulate response
    baseline_tumor, followup, mask_before, mask_after = simulate_tumor_response(
        baseline,
        tumor_center=image_center,
        tumor_size=tumor_size,
        shrinkage_factor=0.5,  # 50% reduction
        intensity_change=-0.2
    )
    
    # Create visualization
    output_dir = Path(__file__).parent.parent / "results"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "biological_response_simulation.png"
    
    create_comparison_figure(
        baseline_tumor, 
        followup, 
        mask_before, 
        mask_after,
        output_path
    )
    
    # Calculate metrics
    volume_reduction = (1 - np.sum(mask_after > 0.1) / np.sum(mask_before > 0.1)) * 100
    
    print("\n" + "="*60)
    print("RESULTS:")
    print("="*60)
    print(f"✓ Initial tumor volume: {np.sum(mask_before > 0.1):.0f} pixels")
    print(f"✓ Residual tumor volume: {np.sum(mask_after > 0.1):.0f} pixels")
    print(f"✓ Volume reduction: {volume_reduction:.1f}%")
    print(f"✓ Figure saved to: {output_path}")
    print("\nThis demonstrates the capability to model biological")
    print("response changes beyond simple anatomical deformation.")
    print("="*60)
