# Paper Summary: Gregg et al. (2025) - CBCT Artifacts & HU Characterization

## Full Citation
**Title:** Hounsfield Unit characterization and dose calculation on a C-arm linac with novel on-board cone-beam computed tomography feature and advanced reconstruction algorithms

**Authors:** Kenneth W. Gregg, Theodore Arsenault, Atefeh Rezaei, Rojano Kashani, Lauren Henke, Alex T. Price

**Journal:** *Journal of Applied Clinical Medical Physics*

**Year:** 2025 (Published/Accepted May 2025, Received Oct 2024)

**DOI:** https://doi.org/10.1002/acm2.70145

---

## Main Focus
Evaluating **Hounsfield Unit (HU) precision** and **dose calculation accuracy** on novel on-board CBCT, comparing:
- Conventional **FDK (Feldkamp–Davis–Kress)** reconstruction
- Advanced **iterative reconstruction (Acuros-CTS iCBCT)** with metal artifact reduction

---

## Technical Artifacts in CBCT

### 1. Scatter (PRIMARY CAUSE of HU inaccuracy)
- **Source:** CBCT's wide-beam geometry
- **Effect:** Significantly degrades HU accuracy
- **Clinical impact:** Can mimic or obscure real density changes

### 2. Beam Hardening
- **Effect:** "Cupping" artifacts in images
- **Occurs:** Especially with high-density materials (bone, metal)

### 3. Photon Starvation
- **Occurs:** In large patients or near high-density regions
- **Effect:** Increased noise and HU inconsistency

### 4. HU Inconsistency/Drift
- **Problem:** CBCT historically lacks CT number precision required for direct dose calculation
- **Critical issue:** Without correction, HU values unreliable for electron density mapping

---

## Density Changes vs. Artifacts

### Near-Water Density Materials (≤1.08 g/cc)
- **FDK reconstruction:** High variance (7.2 ± 15.4 HU)
- **iCBCT reconstruction:** Much better (2.6 ± 5.7 HU)
- **Interpretation:** Scatter artifacts create false density variations

### High-Density Materials (Bone) & Low-Density (Lung)
- Larger deviations observed
- **Problem:** Scatter artifacts can be **mistaken for actual tissue density changes**
- **Clinical risk:** May trigger inappropriate adaptation decisions

---

## Dose Calculation Impact

### FDK Reconstruction (Conventional)
- **PTV-D98% deviations:** Up to **-11.7% drop** in target coverage
- **Cause:** Inaccurate HU → incorrect electron density mapping
- **Clinical significance:** Unacceptable for proton therapy dose calculation

### Iterative Reconstruction (iCBCT)
- **Significant improvement** in HU accuracy
- **3D Gamma Analysis (1%/1mm):**
  - FDK: ~70-75% pass rate (complex spine SBRT)
  - **iCBCT: 93-94% pass rate**
- **Clinical viability:** Improved HU fidelity enables reliable dose restoration

---

## Key Quantitative Metrics

| Reconstruction | HU Variance (water-equiv.) | Gamma Pass Rate (1%/1mm) |
|----------------|---------------------------|-------------------------|
| **FDK (conventional)** | 7.2 ± 15.4 HU | 70-75% |
| **iCBCT (iterative)** | 2.6 ± 5.7 HU | 93-94% |

---

## Relevance to Your Proposal

### 1. Category D: Technical/Artifact Changes
**Essential for Introduction 1.1 classification system:**

**Technical/Artifact Changes (Category D):**
- CBCT scatter artifacts
- HU drift/inconsistency
- Beam hardening artifacts
- Reconstruction-dependent variations

### 2. Challenge for AI Classification
Your AI model (Task 2) must distinguish:
- **Real biological density change** (tumor necrosis, fibrosis)
- **Real anatomical change** (organ filling, positioning)
- **Artifact-induced apparent density change** (CBCT scatter, HU drift)

### 3. Uncertainty Quantification (Task 2, Feature 5)
This paper validates your proposed **uncertainty quantification** approach:
> "Registration uncertainty and imaging noise quantification ensures genuine biological signals aren't misclassified as anatomical artifacts."

Should extend to:
> "...ensures genuine biological/anatomical signals aren't misclassified as technical artifacts \\cite{gregg2025}."

### 4. Clinical Impact Statement
Modern iterative reconstruction (iCBCT) **enables** reliable adaptive workflows, but:
- Still has residual uncertainty (2.6 ± 5.7 HU variance)
- Your AI must be robust to these technical variations
- Needs to filter out artifacts before biological/anatomical classification

---

## Suggested Citation Points

**Introduction 1.1 (Defining Technical Artifacts):**
> "Daily CBCT imaging introduces technical artifacts—scatter, beam hardening, and HU drift—that can mimic genuine anatomical or biological changes \\cite{gregg2025}. These must be distinguished from true tissue property alterations to avoid erroneous adaptation decisions."

**Methodology Task 2 (Uncertainty Quantification):**
> "Uncertainty quantification incorporates imaging artifacts (CBCT scatter inducing HU variance of ~2.6-5.7 HU in modern systems \\cite{gregg2025}) alongside registration uncertainty, ensuring robust classification in the presence of technical noise."

**State of the Art 2.3 (Research Gap):**
> "While advanced CBCT reconstruction algorithms have improved HU accuracy \\cite{gregg2025}, automated methods to distinguish residual imaging artifacts from genuine biological or anatomical responses remain absent."

---

## Critical Insight for Your Project
**Technical artifacts are a CONFOUNDER** that must be accounted for in your AI pipeline:

```
Daily Image Change
     ↓
Is it technical artifact? → YES → Filter/correct
     ↓ NO
Is it anatomical? → Dose restoration
     ↓ NO
Is it biological? → Dose adaptation
```

This justifies your multi-branch architecture and uncertainty-aware layer in Task 2.
