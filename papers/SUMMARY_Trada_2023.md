# Paper Summary: Trada et al. (2023) - Biological Response Biomarkers

## Full Citation
**Title:** Changes in serial multiparametric MRI and FDG-PET/CT functional imaging during radiation therapy can predict treatment response in patients with head and neck cancer

**Authors:** Yuvnik Trada, Paul Keall, Michael Jameson, et al.

**Journal:** *European Radiology*, 2023

**DOI:** https://doi.org/10.1007/s00330-023-09843-2

---

## Main Focus
Investigating whether **serial biological markers** from DWI-MRI and FDG-PET/CT during radiotherapy can predict treatment response (local recurrence) in head and neck cancer patients.

---

## Key Biological Markers

### 1. ADC (Apparent Diffusion Coefficient) - from DWI-MRI
- **Measures:** Tumor cellularity
- **Mechanism:** 
  - Dense tumor tissue restricts water diffusion → **low ADC**
  - Cell death/necrosis increases extracellular space → **high ADC (↑)**
- **Predictive Threshold:** **>24.4% increase** in ADC_mean at Week 3 → better local control

### 2. SUV (Standardized Uptake Value) - from FDG-PET
- **Measures:** Glucose metabolism intensity
- **Used metrics:** SUV_max, SUV_mean
- **Response pattern:** Radiotherapy reduces metabolic activity → **SUV decreases (↓)**

### 3. MTV (Metabolic Tumor Volume) - from FDG-PET
- **Measures:** Volume of metabolically active tumor
- **Most robust predictor** in this study
- **Predictive Threshold:** **>50.4% reduction** in MTV at Week 3 → favorable response

### 4. TLG (Total Lesion Glycolysis)
- **Calculation:** MTV × SUV_mean
- **Measures:** Total metabolic burden

---

## Biological vs. Anatomical Changes

### Anatomical Changes (NOT predictive)
- Geometric tumor volume changes on T2-weighted MRI or CT
- **Finding:** NOT significantly correlated with clinical outcomes
- Reflects only spatial/geometric changes, not underlying physiology

### Biological/Functional Changes (HIGHLY predictive)
- Changes in **ADC** (cellularity/microstructure)
- Changes in **MTV** (metabolic activity)
- Reflect underlying **physiological response** to treatment

---

## Specific Biological Phenomena

### 1. Tumor Cellularity Changes
- **Mechanism:** Irradiation → apoptosis/necrosis → cell membrane breakdown
- **Imaging signature:** Increased water diffusion → **↑ ADC_mean**

### 2. Necrosis
- Dead cells create extracellular space
- **↑ ADC** due to increased water mobility

### 3. Edema & Inflammation (CONFOUNDING FACTOR)
- **Early treatment effect** (before Week 3)
- Also increases water diffusion → **↑ ADC**
- **PROBLEM:** Can confound true tumor response if measured too early
- **Solution:** Week 3 timing allows inflammation to settle

### 4. Metabolic Changes
- Radiotherapy sterilizes/kills tumor cells
- **↓ MTV** as metabolic activity decreases
- More robust than anatomical volume changes

---

## Optimal Timing for Response Assessment
**Week 3 of radiotherapy** identified as optimal time-point:
- Allows acute inflammation/edema to settle
- Captures genuine biological response
- Enables "right-time" adaptive decisions

---

## Quantitative Thresholds (Week 3)

| Biomarker | Threshold | Interpretation |
|-----------|-----------|----------------|
| **ΔADC_mean** | **>24.4% increase** | Favorable response (better local control) |
| **ΔMTV** | **>50.4% reduction** | Most significant PET-based predictor |
| **Combined model** | High ΔADC + High ΔMTV | Significantly improved response classification |

---

## Relevance to Your Proposal

### 1. Definition of Biological Changes (Category C)
Use these **specific examples** in Introduction 1.1:

**Biological Response Changes:**
- ↑ ADC (increased diffusion → cellularity loss, necrosis)
- ↓ SUV (decreased metabolism → treatment response)
- ↓ MTV (reduced metabolic volume)
- Inflammation/edema (early toxicity)
- Fibrosis (late toxicity, density changes)

### 2. Distinction from Anatomical Changes
- **Anatomical:** Geometric volume, shape, position (organ filling, rigid motion)
- **Biological:** Microstructural (ADC), metabolic (SUV/MTV), tissue property changes

### 3. Clinical Justification for Your Project
> "While anatomical tumor volumes do not predict treatment response, functional imaging biomarkers such as ADC and MTV demonstrate significant predictive power \\cite{trada2023}, highlighting the critical need to distinguish biological from anatomical changes in adaptive therapy decision-making."

### 4. Multimodal Feature Engineering (Task 2)
This paper validates your proposed use of:
- Quantitative image biomarkers (radiomics)
- Delta-radiomics (temporal changes)
- Multimodal integration (imaging + dose)

---

## Suggested Citation Points

**Introduction 1.1 (Defining Biological Changes):**
> "Biological changes during radiotherapy include alterations in tumor cellularity (detectable via diffusion-weighted MRI ADC changes), metabolic activity (FDG-PET SUV/MTV reductions), inflammation, edema, and tissue density modifications \\cite{trada2023}."

**State of the Art 2.3 (Research Gap):**
> "Recent evidence demonstrates that functional imaging biomarkers (ADC, MTV) predict treatment response better than anatomical volume changes \\cite{trada2023}, yet no automated methods exist to integrate these biological signals into adaptive dose planning."
