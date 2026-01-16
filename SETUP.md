# Setup Instructions for RAPTORplus Synthetic Image Generation

## Quick Start

Follow these steps to set up the project and run tests:

### 1. Navigate to Project Directory

```powershell
cd "e:\one drive\OneDrive\Desktop\saeed app 2026\raptor\project 16\raptor-synthetic-imaging"
```

### 2. Create Virtual Environment

```powershell
python -m venv venv
```

### 3. Activate Virtual Environment

```powershell
.\venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

This will install:
- numpy, scipy (numerical computing)
- scikit-image, scikit-learn (image processing & ML)
- SimpleITK (medical image registration)
- matplotlib, seaborn (visualization)
- pandas (data handling)
- nibabel (NIfTI medical image format)
- jupyterlab (notebooks)
- tqdm (progress bars)

**Note:** SimpleITK installation may take 2-3 minutes. This is normal.

### 5. Run Tests

```powershell
python test_modules.py
```

Expected output:
```
============================================================
TESTING RAPTOR SYNTHETIC IMAGE GENERATION MODULES
============================================================

[TEST 1] Importing modules...
[OK] All modules imported successfully

[TEST 2] Testing data loader functions...
[OK] Data loader functions work correctly

[TEST 3] Testing registration...
[OK] Registration functions work correctly

[TEST 4] Testing synthetic image generator...
[OK] Generator works - 89.2% variance explained

[TEST 5] Testing quality metrics...
[OK] Metrics work - SSIM: 0.872, PSNR: 25.3 dB

[TEST 6] Testing evaluation function...
[OK] Evaluation function works correctly

[TEST 7] Testing visualization module...
[OK] Visualization module functions are callable

============================================================
[OK] ALL TESTS PASSED!
============================================================
```

If all tests pass, your code is ready!

### 6. Download Dataset (Optional for now)

For full demo with real medical images:

1. Visit http://medicaldecathlon.com/
2. Download **Task04_Hippocampus** (~1 GB)
3. Extract to `data/hippocampus/`

For proposal purposes, you can skip this and use simulated data first.

---

## Troubleshooting

### "python is not recognized"
Make sure Python 3.8+ is installed and in your PATH.

### "pip install" fails
Try:
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### SimpleITK installation is slow
This is normal - SimpleITK is a large package. Be patient.

### Import errors after installation
Make sure virtual environment is activated (you should see `(venv)` in prompt).

---

## Next Steps After Tests Pass

1. **Create demo notebook** - Demonstrate the workflow
2. **Generate sample results** - Create figures for proposal
3. **Push to GitHub** - Make repository public
4. **Update proposal** - Add GitHub link and result figure

---

## File Overview

- `test_modules.py` - Verification script (run this first)
- `requirements.txt` - Python dependencies
- `src/` - Core package modules
- `notebooks/` - Jupyter notebooks  (will create demo)
- `results/` - Generated outputs (will populate)
- `data/` - Medical imaging datasets (download separately)
