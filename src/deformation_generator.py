"""
Synthetic image generator using PCA-based deformation learning.
Core implementation for RAPTORplus Task 1.
"""

import numpy as np
from sklearn.decomposition import PCA
from typing import List, Tuple
from tqdm import tqdm

from .registration import register_images_demons, apply_deformation_field


class SyntheticImageGenerator:
    """
    Generate synthetic anatomical variations using PCA on learned deformation fields.
    
    This implements the deformation-based approach described in the RAPTORplus proposal,
    where population-level anatomical variations are captured through statistical modeling
    of deformation fields.
    """
    
    def __init__(self, n_components: int = 10):
        """
        Initialize the generator.
        
        Args:
            n_components: Number of principal components to retain from PCA
        """
        self.n_components = n_components
        self.reference_image = None
        self.pca_model = None
        self.mean_deformation = None
        self.deformation_shape = None
        self.explained_variance = None
        
    def fit(self, image_list: List[np.ndarray], reference_idx: int = 0, verbose: bool = True):
        """
        Learn deformation patterns from a population of images.
        
        This method:
        1. Registers all images to a reference
        2. Extracts deformation fields
        3. Performs PCA to learn principal deformation modes
        
        Args:
            image_list: List of 2D numpy arrays (all same size)
            reference_idx: Index of image to use as reference
            verbose: Print progress information
        """
        if len(image_list) < 3:
            raise ValueError("Need at least 3 images for PCA analysis")
        
        self.reference_image = image_list[reference_idx]
        
        if verbose:
            print(f"Using image {reference_idx} as reference")
            print(f"Registering {len(image_list)-1} images to reference...")
        
        # Register all images to reference and collect deformation fields
        deformations = []
        iterator = enumerate(image_list)
        if verbose:
            iterator = tqdm(list(iterator), desc="Registering")
        
        for i, img in iterator:
            if i == reference_idx:
                continue
            
            # Perform deformable registration
            dvf = register_images_demons(self.reference_image, img)
            
            # Flatten spatial dimensions but keep vector dimension separate
            dvf_flat = dvf.reshape(-1)
            deformations.append(dvf_flat)
        
        # Stack into matrix: (n_samples, n_features)
        deformation_matrix = np.stack(deformations, axis=0)
        
        if verbose:
            print(f"Deformation matrix shape: {deformation_matrix.shape}")
            print("Performing PCA on deformation fields...")
        
        # Fit PCA model
        self.pca_model = PCA(n_components=self.n_components)
        self.pca_model.fit(deformation_matrix)
        
        # Store mean deformation
        self.mean_deformation = deformation_matrix.mean(axis=0)
        
        # Store shape for reconstruction
        self.deformation_shape = dvf.shape
        
        # Compute explained variance
        self.explained_variance = self.pca_model.explained_variance_ratio_
        
        if verbose:
            print(f"PCA completed:")
            print(f"  - Components: {self.n_components}")
            print(f"  - Total variance explained: {self.explained_variance.sum():.2%}")
            print(f"  - Top 3 components: {self.explained_variance[:3].sum():.2%}")
    
    def generate(self, n_samples: int = 10, variation_scale: float = 1.0, 
                 random_seed: int = None) -> List[np.ndarray]:
        """
        Generate synthetic images by sampling from learned deformation space.
        
        This samples random weights from a Gaussian distribution (weighted by explained variance)
        and reconstructs deformation fields, then applies them to the reference image.
        
        Args:
            n_samples: Number of synthetic images to generate
            variation_scale: Magnitude multiplier (1.0 = typical variation, 2.0 = doubled)
            random_seed: Random seed for reproducibility
        
        Returns:
            List of synthetic images (same shape as reference)
        """
        if self.pca_model is None:
            raise ValueError("Must call fit() before generate()")
        
        if random_seed is not None:
            np.random.seed(random_seed)
        
        synthetic_images = []
        
        for i in range(n_samples):
            # Sample random weights from Gaussian distribution
            # Weights are scaled by sqrt of explained variance (eigenvalues)
            weights = np.random.randn(self.n_components)
            weights *= np.sqrt(self.pca_model.explained_variance_)
            weights *= variation_scale
            
            # Reconstruct deformation field from PCA components
            # dvf = mean + Σ(weight_i * component_i)
            dvf_flat = self.mean_deformation + self.pca_model.components_.T @ weights
            
            # Reshape back to spatial + vector dimensions
            dvf = dvf_flat.reshape(self.deformation_shape)
            
            # Apply deformation to reference image
            synthetic_img = apply_deformation_field(self.reference_image, dvf, scale=1.0)
            
            synthetic_images.append(synthetic_img)
        
        return synthetic_images
    
    def get_pca_summary(self) -> dict:
        """
        Get summary statistics about the learned PCA model.
        
        Returns:
            Dictionary with PCA statistics
        """
        if self.pca_model is None:
            return {}
        
        return {
            'n_components': self.n_components,
            'total_variance_explained': self.explained_variance.sum(),
            'explained_variance_per_component': self.explained_variance.tolist(),
            'deformation_field_shape': self.deformation_shape,
            'reference_image_shape': self.reference_image.shape
        }
