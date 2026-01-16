# RAPTORplus Task 1: Synthetic Medical Image Generation (Proof-of-Concept)

**Author:** Saeed Sarbazzadeh Khosroshahi  
**Project:** RAPTORplus Marie Sklodowska-Curie-Action EU Doctoral Network  
**Institution:** Aarhus University & Danish Centre for Particle Therapy

## Project Overview
This repository contains the proof-of-concept implementation for **Task 1: Synthetic Patient Cohort Generation**. It demonstrates the feasibility of generating scientifically plausible synthetic brain MRI images using deformation fields and Principal Component Analysis (PCA), with extensions for biological response modeling.

## Key Features
- **Deformation-Based Generative Model:** Learns anatomical variations from real populations
- **PCA Dimensionality Reduction:** Captures 87% of anatomical variance with just 10 components
- **SimpleITK Integration:** Robust handling of medical coordinate systems and NIfTI formats
- **Multi-Metric Evaluation:** SSIM, PSNR, MAE, and **FID (Fréchet Inception Distance)**
- **Biological Response Simulation:** Tumor shrinkage modeling for treatment response

## Structure
```
raptor-synthetic-imaging/
├── data/               # Dataset directory (Medical Segmentation Decathlon)
├── notebooks/          # Jupyter notebooks for demonstration
│   ├── demo_synthetic.ipynb      # Basic concept demo
│   └── demo_real_data.ipynb      # FULL DEMO with Real Medical Data
├── src/                # Source code modules
│   ├── data_loader.py            # NIfTI loading & resizing
│   ├── registration.py           # Demons registration logic
│   ├── deformation_generator.py  # PCA-based synthetic generation
│   ├── calculate_fid.py          # FID metric calculation
│   └── simulate_tumor_response.py # Biological response modeling
└── results/            # Generated images and CSV metrics
    ├── quality_metrics_real.csv
    ├── comparison_grid_real.png
    ├── pca_variance_real.png
    └── biological_response_simulation.png
```

## Results
Validated on the **Medical Segmentation Decathlon (Hippocampus Task)** dataset:

**Anatomical Generation (Baseline PoC):**
- **Structural Similarity (SSIM):** 0.57 ± 0.09 (vs Real Patient baseline 0.29)
- **Fréchet Inception Distance (FID):** 254.06
- **PCA Components:** 87.4% variance captured with 10 components

**Biological Response Simulation:**
- **Tumor Volume Reduction:** 73.3% simulated regression
- **Modeling Capability:** Demonstrates feasibility beyond anatomical-only generation

**Interpretation:** The baseline PoC confirms that anatomical variation can be learned from data, establishing feasibility for scaling to advanced diffusion models in the PhD.

## Usage
1. Install dependencies:
   ```bash
   pip install numpy matplotlib seaborn simpleitk scikit-learn tqdm pandas nibabel scikit-image
   # For FID calculation (optional):
   pip install torch torchvision pytorch-fid
   ```

2. Run the real data demo:
   ```bash
   jupyter notebook notebooks/demo_real_data.ipynb
   ```

3. Calculate FID metric (requires PyTorch):
   ```bash
   python src/calculate_fid.py
   ```

4. Generate biological response simulation:
   ```bash
   python src/simulate_tumor_response.py
   ```

## Citation
If using this code for research, please cite:
```
Sarbazzadeh Khosroshahi, S. (2026). 
RAPTORplus Synthetic Medical Image Generation Proof-of-Concept.
Aarhus University & Danish Centre for Particle Therapy.
```

## License
Project specific - RAPTORplus Network.
