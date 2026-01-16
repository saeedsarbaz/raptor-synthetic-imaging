"""
Calculate FID (Fréchet Inception Distance) for synthetic vs real images.
Addresses reviewer feedback: "Add FID metric for perceptual realism assessment"
"""

import numpy as np
import torch
from pathlib import Path
import pandas as pd
from PIL import Image
import tempfile

def prepare_images_for_fid(image_list, output_dir):
    """
    Prepare images for FID calculation by saving as RGB images.
    FID requires RGB images, so we convert grayscale to RGB.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for idx, img in enumerate(image_list):
        # Normalize to 0-255 range
        img_normalized = ((img - img.min()) / (img.max() - img.min()) * 255).astype(np.uint8)
        
        # Convert to RGB (replicate grayscale across 3 channels)
        img_rgb = np.stack([img_normalized] * 3, axis=-1)
        
        # Save as PNG
        img_pil = Image.fromarray(img_rgb)
        img_pil.save(output_dir / f"img_{idx:03d}.png")
    
    return len(image_list)

def calculate_fid(real_images, synthetic_images):
    """
    Calculate FID score between real and synthetic image sets.
    Lower FID = better quality (more similar to real distribution).
    
    Args:
        real_images: List of real images (numpy arrays)
        synthetic_images: List of synthetic images (numpy arrays)
    
    Returns:
        fid_score: Scalar FID value
    """
    from pytorch_fid import fid_score
    
    # Create temporary directories
    with tempfile.TemporaryDirectory() as tmpdir:
        real_dir = Path(tmpdir) / "real"
        synth_dir = Path(tmpdir) / "synthetic"
        
        # Prepare images
        print(f"Preparing {len(real_images)} real images...")
        prepare_images_for_fid(real_images, real_dir)
        
        print(f"Preparing {len(synthetic_images)} synthetic images...")
        prepare_images_for_fid(synthetic_images, synth_dir)
        
        # Calculate FID
        print("Calculating FID score...")
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {device}")
        
        fid_value = fid_score.calculate_fid_given_paths(
            [str(real_dir), str(synth_dir)],
            batch_size=8,
            device=device,
            dims=2048
        )
        
        return fid_value

if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    # Add src to path
    src_dir = Path(__file__).parent
    sys.path.insert(0, str(src_dir))
    parent_dir = src_dir.parent
    sys.path.insert(0, str(parent_dir))
    
    # Import from src
    import data_loader
    import deformation_generator
    
    print("="*60)
    print("FID Metric Calculation for Synthetic Images")
    print("="*60)
    
    # Load real data - point to imagesTr subdirectory where .nii.gz files are
    data_dir = parent_dir / "data" / "Task04_Hippocampus" / "Task04_Hippocampus" / "imagesTr"
    print(f"\nLoading real MRI data from: {data_dir}")
    
    real_slices = data_loader.load_dataset_slices(
        str(data_dir),
        n_images=20,
        normalize=True
    )
    
    # Generate synthetic images (using same process as demo)
    print("\nTraining generator on real data...")
    generator = deformation_generator.SyntheticImageGenerator(n_components=10)
    generator.fit(real_slices, reference_idx=0, verbose=True)
    
    print("\nGenerating 15 synthetic images...")
    synthetic_slices = generator.generate(n_samples=15, random_seed=42)
    
    # Calculate FID
    print("\n" + "="*60)
    print("Computing FID Score...")
    print("="*60)
    
    fid_value = calculate_fid(real_slices, synthetic_slices)
    
    print(f"\n{'='*60}")
    print(f"RESULT: FID Score = {fid_value:.2f}")
    print(f"{'='*60}")
    print("\nInterpretation:")
    print("  - Lower FID = Better perceptual similarity to real data")
    print("  - Typical ranges:")
    print("    * FID < 50:  Excellent quality")
    print("    * FID 50-100: Good quality")
    print("    * FID 100-200: Moderate quality")  
    print("    * FID > 200:  Requires improvement")
    
    # Update CSV
    csv_path = parent_dir / "results" / "quality_metrics_real.csv"
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        
        # Add FID column if not exists
        if 'fid' not in df.columns:
            df['fid'] = np.nan
        
        # Set FID for synthetic images only
        df.loc[df['type'] == 'synthetic', 'fid'] = fid_value
        
        df.to_csv(csv_path, index=False)
        print(f"\nUpdated {csv_path} with FID scores")
    
    print("\n✅ FID calculation complete!")
