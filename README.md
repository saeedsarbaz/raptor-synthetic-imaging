# RAPTORplus Task 1: Synthetic Medical Image Generation (Proof-of-Concept)

**Author:** Saeed Sarbazzadeh Khosroshahi  
**Project:** RAPTORplus Marie Sklodowska-Curie-Action EU Doctoral Network  
**Institution:** Aarhus University & Danish Centre for Particle Therapy

## Project Overview
This repository contains the proof-of-concept implementation for **Task 1: Synthetic Patient Cohort Generation**. It demonstrates the feasibility of generating scientifically plausible synthetic brain MRI images using deformation fields and Principal Component Analysis (PCA).

## Key Features
- **Deformation-Based Generative Model:** Learns anatomical variations from real populations.
- **PCA Dimensionality Reduction:** Captures 87% of anatomical variance with just 10 components.
- **SimpleITK Integration:** Robust handling of medical coordinate systems and NIfTI formats.
- **Quality Metrics:** Automated evaluation using SSIM, PSNR, and MAE.

## Structure
```
raptor-synthetic-imaging/
├── data/               # Dataset directory (Medical Segmentation Decathlon)
├── notebooks/          # Jupyter notebooks for demonstration
│   ├── demo_synthetic.ipynb  # Basic concept demo
│   └── demo_real_data.ipynb  # FULL DEMO with Real Medical Data
├── src/                # Source code modules
│   ├── data_loader.py  # NIfTI loading & resizing
│   ├── registration.py # Demons registration logic
│   └── ...
└── results/            # Generated images and CSV metrics
```

## Results
The model was validated on the **Medical Segmentation Decathlon (Hippocampus Task)** dataset.
- **Structural Similarity (SSIM):** 0.57 ± 0.09 (vs Real Patient baseline 0.29)
- **Conclusion:** Generated anatomies are stable, realistic, and span the learned manifold of deformation.

## Usage
1. Install dependencies:
   ```bash
   pip install numpy matplotlib seaborn simpleitk scikit-learn tqdm pandas
   ```
2. Run the real data demo:
   ```bash
   jupyter notebook notebooks/demo_real_data.ipynb
   ```

## License
Project specific - RAPTORplus Network.
