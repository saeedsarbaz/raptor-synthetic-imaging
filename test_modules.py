"""
Simple test script to verify all modules work correctly.
Run this before generating real data to catch any errors.
"""

import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

print("=" * 60)
print("TESTING RAPTOR SYNTHETIC IMAGE GENERATION MODULES")
print("=" * 60)

# Test 1: Import all modules
print("\n[TEST 1] Importing modules...")
try:
    from src import data_loader, registration, deformation_generator, quality_metrics, visualization
    print("[OK] All modules imported successfully")
except Exception as e:
    print(f"[FAIL] Import error: {e}")
    sys.exit(1)

# Test 2: Data loader functions
print("\n[TEST 2] Testing data loader functions...")
try:
    # Create dummy image
    dummy_img = np.random.rand(100, 100).astype(np.float32)
    
    # Test normalization
    normalized = data_loader.normalize_image(dummy_img)
    assert normalized.min() >= 0 and normalized.max() <= 1, "Normalization failed"
    
    # Test slice extraction from 3D volume
    volume_3d = np.random.rand(50, 50, 50)
    slice_2d = data_loader.select_middle_slice(volume_3d, axis=2)
    assert slice_2d.shape == (50, 50), "Slice extraction failed"
    
    print("[OK] Data loader functions work correctly")
except Exception as e:
    print(f"[FAIL] Data loader error: {e}")
    sys.exit(1)

# Test 3: Registration
print("\n[TEST 3] Testing registration...")
try:
    # Create two similar images
    img1 = np.random.rand(64, 64).astype(np.float32)
    img2 = img1 + np.random.randn(64, 64).astype(np.float32) * 0.1  # Add small noise
    
    # Test registration
    dvf = registration.register_images_demons(img1, img2, n_iterations=10)
    assert dvf.shape == (64, 64, 2), f"Deformation field shape is {dvf.shape}, expected (64, 64, 2)"
    
    # Test warping
    warped = registration.apply_deformation_field(img2, dvf, scale=1.0)
    assert warped.shape == img1.shape, "Warped image shape mismatch"
    
    print("[OK] Registration functions work correctly")
except Exception as e:
    print(f"[FAIL] Registration error: {e}")
    sys.exit(1)

# Test 4: Synthetic Generator
print("\n[TEST 4] Testing synthetic image generator...")
try:
    # Create a small population of images
    population = [np.random.rand(64, 64).astype(np.float32) for _ in range(5)]
    
    # Create and fit generator
    generator = deformation_generator.SyntheticImageGenerator(n_components=3)
    generator.fit(population, verbose=False)
    
    # Check PCA was successful
    summary = generator.get_pca_summary()
    assert summary['n_components'] == 3, "PCA components mismatch"
    assert summary['total_variance_explained'] > 0, "No variance explained"
    
    # Generate synthetic images
    synthetic = generator.generate(n_samples=3, variation_scale=1.0, random_seed=42)
    assert len(synthetic) == 3, "Wrong number of synthetic images"
    assert synthetic[0].shape == (64, 64), "Synthetic image shape mismatch"
    
    print(f"[OK] Generator works - {summary['total_variance_explained']:.1%} variance explained")
except Exception as e:
    print(f"[FAIL] Generator error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Quality metrics
print("\n[TEST 5] Testing quality metrics...")
try:
    img_ref = np.random.rand(64, 64).astype(np.float32)
    img_test = img_ref + np.random.randn(64, 64).astype(np.float32) * 0.1
    
    # Test individual metrics
    ssim_val = quality_metrics.compute_ssim(img_ref, img_test)
    psnr_val = quality_metrics.compute_psnr(img_ref, img_test)
    mae_val = quality_metrics.compute_mae(img_ref, img_test)
    rmse_val = quality_metrics.compute_rmse(img_ref, img_test)
    
    assert 0 <= ssim_val <= 1, f"SSIM out of range: {ssim_val}"
    assert psnr_val > 0, f"PSNR should be positive: {psnr_val}"
    assert mae_val >= 0, f"MAE should be non-negative: {mae_val}"
    assert rmse_val >= 0, f"RMSE should be non-negative: {rmse_val}"
    
    print(f"[OK] Metrics work - SSIM: {ssim_val:.3f}, PSNR: {psnr_val:.1f} dB")
except Exception as e:
    print(f"[FAIL] Metrics error: {e}")
    sys.exit(1)

# Test 6: Evaluation function
print("\n[TEST 6] Testing evaluation function...")
try:
    ref = np.random.rand(64, 64).astype(np.float32)
    synthetic_list = [ref + np.random.randn(64, 64).astype(np.float32) * 0.1 for _ in range(3)]
    real_list = [ref + np.random.randn(64, 64).astype(np.float32) * 0.15 for _ in range(3)]
    
    df = quality_metrics.evaluate_synthetic_images(ref, synthetic_list, real_list)
    
    assert len(df) == 6, "Wrong number of evaluations"
    assert set(df['type'].unique()) == {'synthetic', 'real'}, "Missing image types"
    assert all(col in df.columns for col in ['ssim', 'psnr', 'mae', 'rmse']), "Missing metric columns"
    
    print("[OK] Evaluation function works correctly")
    print(f"   Sample metrics - Synthetic SSIM: {df[df['type']=='synthetic']['ssim'].mean():.3f}")
except Exception as e:
    print(f"[FAIL] Evaluation error: {e}")
    sys.exit(1)

# Test 7: Visualization (basic import test)
print("\n[TEST 7] Testing visualization module...")
try:
    # Just test that functions are callable (won't display plots in test)
    assert callable(visualization.create_comparison_grid), "create_comparison_grid not callable"
    assert callable(visualization.plot_metrics_comparison), "plot_metrics_comparison not callable"
    print("[OK] Visualization module functions are callable")
except Exception as e:
    print(f"[FAIL] Visualization error: {e}")
    sys.exit(1)

# Summary
print("\n" + "=" * 60)
print("[OK] ALL TESTS PASSED!")
print("=" * 60)
print("\nThe code is ready to use with real medical imaging data.")
print("Next steps:")
print("  1. Download Medical Segmentation Decathlon dataset")
print("  2. Run the demo notebook")
print("  3. Generate results for your proposal")
