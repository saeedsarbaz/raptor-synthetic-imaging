# Paper Summary: IBSI - Image Biomarker Standardization Initiative (2020)

## Full Citation
**Title:** The Image Biomarker Standardization Initiative: Standardized Quantitative Radiomics for High-Throughput Image-based Phenotyping

**Authors:** Alex Zwanenburg, Martin Vallières, Mahmoud A. Abdalah, Hugo J.W.L. Aerts, Vincent Andrearczyk, Aditya Apte, Saeed Ashrafinia, Spyridon Bakas, et al.

**Journal:** *Radiology*

**Year:** 2020 (Published online Jan 14, 2020; Issue May 2020)

**DOI:** https://doi.org/10.1148/radiol.2020191145

---

## Main Focus

Establishing **standardized definitions and computational methods** for radiomic features to ensure reproducibility across different software implementations, research centers, and imaging modalities.

---

## The Reproducibility Crisis in Radiomics

### Core Problem:
**Before IBSI:** The same feature name (e.g., "Entropy," "Sphericity") produced **different numerical values** across different software packages and research teams due to:
- Inconsistent mathematical definitions
- Variability in image preprocessing (resampling, discretization)
- Lack of standardized nomenclature
- Implementation differences across platforms (MATLAB, Python, etc.)

**Impact:** Radiomics models were **not reproducible** across institutions, limiting clinical translation.

---

## IBSI Solution: Three-Phase Standardization

### **Phase I: Feature Standardization**
- **Standardized 174 radiomic features:**
  - Morphology (volume, surface area, sphericity)
  - Intensity statistics (mean, median, kurtosis)
  - Texture features (GLCM, GLRLM, GLSZM, etc.)
- **Provided reference values** for software validation
- **Result:** 166 of 174 features achieved "Strong" or "Very Strong" consensus across 25 research teams

### **Phase II: Image Processing Workflow**
Standardized preprocessing steps:
1. **Image interpolation/resampling** (to common voxel size)
2. **Re-segmentation** (mask interpolation)
3. **Intensity discretization** (binning strategies)

**Critical insight:** Feature values are highly sensitive to preprocessing choices.

### **Phase III: Multi-Institutional Validation**
- **25 research teams** tested IBSI compliance
- **Multiple imaging modalities:** CT, PET, MRI
- **Diverse software platforms:** MATLAB, Python, R, commercial packages
- **Outcome:** Excellent reproducibility when IBSI guidelines followed

---

## IBSI Compliance Requirements

### For Radiomics Research to Be IBSI-Compliant:
1. ✅ **Use IBSI-standardized feature definitions**
2. ✅ **Report detailed image processing steps:**
   - Interpolation method (e.g., trilinear, cubic)
   - Discretization strategy (fixed bin width vs. bin count)
   - ROI resampling approach
3. ✅ **Validate software against IBSI reference values**
4. ✅ **Use IBSI-compliant software/packages**

### Non-Compliance Consequences:
- ❌ Results not comparable across studies
- ❌ Models not generalizable to other datasets
- ❌ Clinical translation impossible

---

## Harmonization: Addressing Multi-Center Variability

### Problem Beyond Feature Standardization:
Even with IBSI-compliant feature extraction, **multi-center studies** face variability due to:
- Different scanner manufacturers (GE, Siemens, Philips)
- Different acquisition protocols (kVp, reconstruction kernels)
- Different imaging sites/institutions

These are **"batch effects"** that reflect technical noise, not biology.

### Harmonization Methods:
1. **ComBat:** Statistical harmonization that removes batch effects while preserving biological signal
2. **Image-based methods:** Converting reconstruction kernels, synthetic image normalization
3. **Standardized acquisition protocols:** When feasible

**IBSI recommendation:** Use harmonization for multi-center data to ensure findings reflect **biology, not technical artifacts**.

---

## Delta-Radiomics: Added Complexity

### Definition:
**Delta-radiomics** = Temporal changes in radiomic features during treatment (baseline vs. mid-treatment vs. post-treatment)

### IBSI Context:
- **Primary IBSI focus:** Baseline (single time-point) feature standardization
- **Delta-radiomics challenge:** Adds longitudinal complexity:
  - Image registration across time points
  - Consistent preprocessing over time
  - Handling anatomical changes (tumor shrinkage, organ motion)

### Quality Concerns:
- **Mixed quality in literature:** Many delta-radiomics studies lack:
  - IBSI compliance at each time point
  - Proper harmonization across longitudinal scans
  - Validation of temporal feature stability
- **User request notes:** "delta-radiomics has mixed quality" aligns with IBSI acknowledgment that temporal features require **additional standardization layers**

---

## Impact on Reproducibility

### With IBSI Compliance:
- ✅ **High inter-software reproducibility** (166/174 features)
- ✅ **Consistent results across research teams**
- ✅ **Validation datasets become comparable**
- ✅ **Clinical translation becomes feasible**

### Without IBSI Compliance:
- ❌ Feature values vary unpredictably
- ❌ Models fail external validation
- ❌ Meta-analyses impossible
- ❌ Clinical adoption blocked

---

## Key Recommendations for Radiomics Research

1. **Use IBSI-compliant software** (e.g., PyRadiomics with IBSI validation)
2. **Report preprocessing in detail** (interpolation, discretization, ROI handling)
3. **Validate against IBSI reference values** before extracting features from clinical data
4. **Apply harmonization** (e.g., ComBat) for multi-center studies
5. **For delta-radiomics:** Ensure IBSI compliance at each time point + longitudinal harmonization

---

## Relevance to Your Proposal

### For Section 2.2 (AI in Radiation Oncology):

**Current text mentions:**
> "Radiomics and deep learning predict treatment response and toxicity"

**Should emphasize:**
> "Radiomics reproducibility hinges on IBSI compliance for standardized feature extraction and harmonization methods (e.g., ComBat) for multi-center studies \\cite{zwanenburg2020ibsi}. Delta-radiomics, showing temporal feature changes during treatment, exhibits mixed quality in current literature and requires rigorous longitudinal standardization \\cite{fave2017}."

### Connection to Your Research:

#### Your Task 1 (Change Classification):
- **IBSI lesson:** Standardization is critical for reproducibility
- **Your equivalent:** AI-based change characterization must have:
  - Standardized definitions of "anatomical" vs. "biological" changes
  - Reproducible classification across different scanners/sites
  - Validation against ground truth

#### Delta-Radiomics Parallel:
- **Delta-radiomics challenge:** Temporal feature extraction with mixed quality
- **Your approach:** Temporal image change characterization with AI
- **Advantage:** Your method integrates biological context (dose, timing) vs. pure feature statistics

---

## Gold Standard Status

**IBSI is now the gold standard for radiomics research:**
- Required by many journals for radiomics studies
- Essential for multi-center collaborations
- Foundational for clinical radiomics adoption
- Ensures "Entropy" in Lab A = "Entropy" in Lab B

**Quote from paper:**
> "The goal of IBSI is to standardize the extraction of image biomarkers from acquired imaging for the purpose of high-throughput quantitative image analysis (radiomics)."

---

## New Bibliography Entry

```latex
\bibitem{zwanenburg2020ibsi}
Zwanenburg A, Vallières M, Abdalah MA, Aerts HJWL, Andrearczyk V, Apte A, Ashrafinia S, Bakas S, et al. The Image Biomarker Standardization Initiative: Standardized Quantitative Radiomics for High-Throughput Image-based Phenotyping. \textit{Radiology}, 2020; 295(2):328-338. https://doi.org/10.1148/radiol.2020191145.
```

---

## Key Takeaways

1. ✅ **IBSI = Reproducibility:** Without IBSI compliance, radiomics results are not reproducible
2. ✅ **Standardization ≠ Harmonization:** Both are needed for multi-center studies
3. ⚠️ **Delta-radiomics complexity:** Temporal features require additional standardization
4. 🔬 **Clinical translation:** IBSI compliance is prerequisite for clinical adoption
5. 📊 **Multi-center studies:** Must use harmonization (e.g., ComBat) to remove batch effects
