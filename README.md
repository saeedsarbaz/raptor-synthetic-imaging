# 🎯 AI-Driven Anatomical and Response-Adapted Proton Therapy

[![PhD Proposal](https://img.shields.io/badge/Status-PhD%20Proposal-blue.svg)](https://github.com/saeedsarbaz/raptor-synthetic-imaging)
[![LaTeX](https://img.shields.io/badge/Made%20with-LaTeX-008080.svg)](https://www.latex-project.org/)
[![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

> **PhD Research Proposal**: Distinguishing Biological from Anatomical Changes for Personalized Dose Optimization in Adaptive Proton Therapy

**Author**: Saeed Sarbazzadeh Khosroshahi  
**Current Affiliation**: PhD Candidate, Istanbul Technical University (ITU)  
**Application**: RAPTORplus Marie-Sklodowska-Curie-Action EU Doctoral Network (Prospective Candidate)  
**Proposed Supervisor**: Professor Stine Sofia Korreman (Aarhus University & Danish Centre for Particle Therapy)  
**Last Updated**: January 26, 2026

---

## 📖 Abstract

Adaptive radiotherapy currently focuses on anatomical variations, using daily imaging to restore planned dose distributions when anatomy changes occur. However, many image changes during treatment reflect biological responses—tumor regression or progression, and early normal-tissue effects—which may require genuine dose adaptation rather than dose restoration.

This PhD project aims to develop **novel AI-based methods** to distinguish between anatomical and biological components of daily image changes during proton therapy, and implement corresponding dose optimization strategies.

**Key Innovation**: First systematic framework to disentangle biological versus anatomical drivers of image changes in adaptive proton therapy using conformal prediction and robust optimization.

---

## 🎯 Research Objectives

1. **Synthetic Image Generation** - Develop dose-valid synthetic datasets with controlled anatomy/biology decomposition
2. **AI-Based Response Characterization** - Build multimodal models to classify changes with calibrated uncertainty
3. **Dose Optimization Strategies** - Implement confidence-aware robust IMPT for restoration/adaptation/escalation
4. **Clinical Integration** - Create end-to-end pipeline with automated QA and validation

---

## 📁 Repository Structure

```
raptor-synthetic-imaging/
├── README.md                          # This file
├── main_revised.tex                   # PhD proposal (LaTeX source)
├── main_revised.pdf                   # Compiled proposal (to be added)
├── CHANGELOG.md                       # Revision history
├── LICENSE                            # CC BY-NC 4.0
│
├── docs/                              # Documentation
│   ├── revision_completion_summary.md # Full revision log
│   ├── referee_review_report.md       # Expert peer review
│   └── figures/                       # Proposal figures
│       ├── fig_methodology_overview.png
│       ├── fig_synthetic_generation.png
│       ├── fig_response_characterization.png
│       ├── fig_dose_optimization.png
│       ├── fig_task1_real_results.png
│       ├── fig_task1_real_comparison.png
│       └── fig_task1_real_profile.png
│
├── validation/                        # Preliminary validation results
│   ├── cbct_digital_twin/            # Task 1 CBCT validation
│   │   ├── metrics.csv
│   │   └── validation_report.md
│   └── acceptance_gates/             # Pre-registered criteria
│       └── task_acceptance_criteria.md
│
├── methodology/                       # Detailed methodology notes
│   ├── task1_synthetic_generation.md
│   ├── task2_response_characterization.md
│   ├── task3_dose_optimization.md
│   └── task4_integration_validation.md
│
└── references/                        # Key references (BibTeX)
    └── proposal.bib
```

---

## 🔬 Methodology Overview

### Four-Task Research Pipeline

#### **Task 1: Synthetic Image Generation**
- **Methods**: Deformation-based anatomy, diffusion-based biology, CBCT digital twin
- **Validation**: Dose-centric (WEPL, gamma, DVH), SPR RMSE ≤0.02
- **Acceptance**: Median range error ≤1.5mm, P95 ≤3mm

#### **Task 2: AI-Based Response Characterization**
- **Architecture**: Multimodal (imaging, dose, radiomics, population anatomy) with physics QA gate
- **Features**: IBSI-compliant delta-radiomics, mass-/energy-conserving dose accumulation
- **Uncertainty**: Conformal prediction (α=0.10 for 90% coverage), calibration monitoring
- **Acceptance**: Biology F1 ≥0.65, AUC-PR ≥0.70, ECE ≤0.05

#### **Task 3: Dose Optimization**
- **Approach**: Confidence-aware robust IMPT (setup ±3mm, range ±3.5%)
- **Strategy**: ROI-level restoration (anatomy) vs. adaptation (biology)
- **Robustness**: CVaR for OAR chance-constraints, expanded scenario bank (4D for lung)
- **Acceptance**: |ΔD₉₅|, |ΔD₉₈| ≤2% Rx; OAR ≤2 Gy(RBE); runtime <10 min

#### **Task 4: Clinical Integration**
- **System**: End-to-end orchestrator with TPS integration (RayStation API)
- **QA**: Automated DIR QA (TG-132), provenance hashing, deliverability checks
- **Validation**: Retrospective study (n≥30/site), external hold-out, TOST equivalence testing

---

## ✅ Validation & Acceptance Criteria

All tasks have **pre-registered acceptance gates** to ensure scientific rigor:

| Task | Primary Metric | Target | Status |
|------|----------------|--------|--------|
| Task 1 | WEPL median error | ≤1.5 mm | Preliminary✓ |
| Task 1 | Gamma pass (2%/2mm) | Δ≤5 pp | Preliminary✓ |
| Task 2 | Biology F1 (external) | ≥0.65 | Planned |
| Task 2 | Calibration ECE | ≤0.05 | Planned |
| Task 3 | Robust DVH | ≤2% Rx | Planned |
| Task 3 | OAR safety | ≤2 Gy(RBE) | Planned |
| Task 4 | Runtime | <10 min | Planned |
| Task 4 | Clinician accept. | Likert ≥4/5 | Planned |

---

## 📊 Preliminary Results

### CBCT Digital Twin Validation (5 Respiratory Phases)

✅ **Targets Met:**
- PSNR: 23.2–23.5 dB (target ≥20 dB)
- NCC: 0.846–0.850 (target ≥0.85)

✅ **Near Targets:**
- SSIM: 0.779–0.794 (93% of 0.85 stretch target)
- Lung HU bias: +65–68 HU (113% of ±60 HU stretch target)

See [`docs/validation/cbct_digital_twin/`](docs/validation/cbct_digital_twin/) for details.

---

## 🔄 Revision History

**v1.0 (January 26, 2026)** - Complete revision incorporating expert feedback:
- ✅ Added 3-tier biological ground truth validation strategy
- ✅ Positioned LET/RBE as exploratory (not prescriptive)
- ✅ Changed to ROI-level (not voxel-level) dose optimization
- ✅ Added physics-informed CBCT scatter correction + SPR validation
- ✅ Added leakage controls for biology synthesis
- ✅ Added domain adaptation + site-specific DIR QA
- ✅ Added calibration monitoring with drift detection
- ✅ Added external validation + power analysis
- ✅ Added expanded scenario bank with CVaR
- ✅ Added IBSI Part 2 delta-radiomics protocol
- ✅ Added 4D evaluation for lung + clinician rubric
- ✅ Added key references (Unkelbach, McNamara, Vovk, Grassberger)

See [`CHANGELOG.md`](CHANGELOG.md) for full revision details.

---

## 📚 Key References

- **Adaptive Proton Therapy**: Albertini et al. (2024), Gambetta et al. (2025)
- **Robust Optimization**: Unkelbach & Bortfeld (2018)
- **Biological Response**: Trada et al. (2023)
- **CBCT for Protons**: Vestergaard et al. (2024), Gregg et al. (2025)
- **Radiomics**: IBSI (Zwanenburg et al., 2020)
- **Dose Accumulation**: Zhong (2024)
- **DIR QA**: TG-132 (Brock et al., 2017)
- **Variable RBE**: McNamara et al. (2015)
- **Conformal Prediction**: Vovk et al. (2005)

Full bibliography in [`references/proposal.bib`](references/proposal.bib)

---

## 🎓 Academic Context

### RAPTORplus Doctoral Network

This PhD is part of the **RAPTORplus Marie-Sklodowska-Curie-Action EU Doctoral Network**, focusing on "Right-time Adaptive Particle Therapy." The network provides:

- Multi-site proton therapy data across Europe
- Secondments: NTNU (Norway), Politecnico Milano (Italy), industrial partners
- Collaborative research infrastructure
- Training in multimodal imaging, robust optimization, clinical workflow engineering

### Expected Outcomes

**Scientific**:
- 3-4 peer-reviewed publications (*Medical Physics*, *PMB*, *Radiotherapy & Oncology*)
- Novel framework for anatomy/biology disentanglement
- Open-source tools and synthetic datasets (where permitted)

**Clinical**:
- Personalized dose adaptation based on biological response
- Improved local control and reduced toxicity
- Efficient workflows compatible with clinical time constraints

**Training**:
- Cross-disciplinary expertise (AI, medical physics, robust optimization)
- International network and collaborative research skills
- Career readiness for academic/industrial precision oncology roles

---

## 🔧 Technical Requirements

### Software & Tools
- **LaTeX**: TeXLive 2023+ or Overleaf
- **Treatment Planning**: RayStation (MC dose engine, robust scenarios)
- **Deep Learning**: PyTorch 2.0+, CUDA 11.8+
- **Image Processing**: ASTRA Toolbox (CBCT reconstruction)
- **Version Control**: Git, GitHub
- **Data**: DICOM, NIfTI formats

### Computational Resources
- GPU: NVIDIA A100 or equivalent (for DL training + MC dose)
- Storage: Secure, encrypted (clinical data with audit trails)
- Compute: <10 min runtime target for clinical workflow

---

## 📄 License

This proposal is licensed under **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.

- ✅ Share and adapt with attribution
- ❌ Commercial use prohibited without permission
- See [`LICENSE`](LICENSE) for details

Code and software will be released under **Apache 2.0** upon publication.

---

## 🤝 Contributing

This is an active PhD research project. Feedback, suggestions, and collaborations are welcome!

**Contact**:
- **Email**: saeed.sarbazzadeh@clin.au.dk (to be confirmed)
- **Institution**: Danish Centre for Particle Therapy, Aarhus University Hospital
- **Supervisor**: Prof. Stine Sofia Korreman

**Areas for Collaboration**:
- Multi-site data contributions (RAPTORplus partners)
- Validation cohorts with DW-MRI/PET functional imaging
- Clinical workflow integration and testing
- Robust optimization algorithm development

---

## 🏆 Acknowledgments

- **RAPTORplus Consortium** - Marie Skłodowska-Curie Actions funding
- **Danish Centre for Particle Therapy** - Clinical infrastructure and data
- **Aarhus University** - Academic supervision and resources
- **Secondment Partners** - NTNU, Politecnico Milano, industrial collaborators

---

## 📊 Project Timeline

```
Year 1 (2026-2027)
├── Q1-Q2: Ethics, DMP, CBCT digital twin ✓
├── Q2:    Task 1 v0.9 (synthetic generation)
├── Q3-Q4: Task 2 v1.0 (response characterization)
└── Q4:    Secondment @ NTNU (3 months)

Year 2 (2027-2028)
├── Q1-Q2: Task 2 validation, Task 3 prototype
├── Q2-Q3: Task 3 hardening (robust optimization)
├── Q3-Q4: Secondment @ Politecnico Milano (3 months)
└── Q4:    Industrial partner integration (2 months)

Year 3 (2028-2029)
├── Q1-Q2: Task 4 integration & retrospective study
└── Q3-Q4: Thesis writing & defense
```

---

## 📈 Current Status

**Phase**: Proposal Development & Preliminary Validation  
**Date**: January 26, 2026  
**Revision**: v1.0 (submission-ready)  
**Review Status**: Expert review complete (9.5/10, Accept with Minor Revisions)

**Next Steps**:
1. ✅ Complete proposal revisions (DONE)
2. ✅ Expert review (DONE - see `docs/referee_review_report.md`)
3. ⏳ Supervisor final approval
4. ⏳ Formal submission to PhD program
5. ⏳ Begin Task 1 implementation (CBCT digital twin v1.0)

---

## 🔗 Related Resources

- [RAPTORplus Network](https://raptorplus.eu) (to be confirmed)
- [Danish Centre for Particle Therapy](https://www.auh.dk/afdelinger/dansk-center-for-partikelterapi/)
- [Aarhus University](https://www.au.dk)
- [IBSI Initiative](https://theibsi.github.io)
- [AAPM TG-132 DIR QA](https://www.aapm.org/pubs/reports/RPT_132.pdf)

---

## 📞 Contact & Links

**Saeed Sarbazzadeh Khosroshahi**  
PhD Candidate, Istanbul Technical University (ITU)  
Applicant: RAPTORplus Marie-Sklodowska-Curie-Action EU Doctoral Network

- 🐙 GitHub: [@saeedsarbaz](https://github.com/saeedsarbaz)
- 📧 Email: khosroshahis19@itu.edu.tr
- 📱 Phone: +90 551 011 8486
- 🏛️ Current Institution: Istanbul Technical University
- 🎯 Target Program: RAPTORplus Doctoral Network

---

**Last Updated**: January 26, 2026  
**Version**: 1.0  
**Status**: Submission-Ready
