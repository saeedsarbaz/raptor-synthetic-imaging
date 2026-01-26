# Paper Summary: Zhong (2024) - Energy-Conserving Dose Accumulation

## Full Citation
**Title:** An energy-conserving dose summation method for dose accumulation in radiotherapy

**Author:** Hualiang Zhong

**Journal:** *Medical Physics*, 2024

**DOI:** https://doi.org/10.1002/mp.17514

---

## Main Problem Addressed

**Traditional Direct Dose Summation (DDS) Fails:**
- Conventional dose accumulation simply **sums dose values** from different fractions onto a reference image
- **PROBLEM:** Does NOT conserve total energy when mass or density changes occur
- **Why it matters:** Dose = Energy/Mass ($D = E/m$)
  - If mass changes (tumor shrinkage, weight loss, organ filling) but we just add doses → **unphysical results**
  - Leads to **inaccurate treatment outcome assessments**

### Example Errors Found:
- **PTV:** Energy conservation error up to **41.8%** with DDS
- **Lung:** Error up to **11.2%** with DDS
- **Mean dose differences:** 10.2% (PTV), 14.5% (lung) between DDS and correct method

---

## Proposed Solution: Mass-Weighted Dose Summation (MDS)

### Mathematical Principle

$$D_T(\nu) = \frac{\sum_{i=1}^K E_i(\nu)}{M_A(\nu)}$$

Where:
- $D_T(\nu)$ = Total accumulated dose at voxel $\nu$
- $E_i(\nu)$ = Energy transferred from fraction $i$ to voxel $\nu$ in reference image
- $M_A(\nu)$ = **Average mass** at that voxel across all fractions
- $K$ = Number of fractions

### Key Advantages
1. **Energy conservation:** Total energy in each organ matches sum of fractional energies
2. **Algorithm-independent:** Robust regardless of specific DIR method used
3. **Physically principled:** Respects $D = E/m$ relationship
4. **Prevents voxel disappearance errors:** Handles regions where anatomy changes significantly

---

## Validation Results

### Accuracy Comparison (Lung Cancer Case Study)

| Method | PTV Energy Error | Lung Energy Error |
|--------|------------------|-------------------|
| **DDS (traditional)** | **41.8%** | **11.2%** |
| **MDS (proposed)** | **<0.18%** | **<0.18%** |

### Dose Differences (DDS vs MDS)
- **Mean dose difference in PTV:** 10.2%
- **Mean dose difference in lung:** 14.5%
- **Conclusion:** Traditional methods significantly **misrepresent delivered dose** in regions with anatomical changes

---

## DIR Quality Assurance Recommendations

### Energy-Based QA Metric
The paper proposes using **summed energy conservation** as a physical metric to verify DIR accuracy:

1. **Calculate total energy** from each fraction's dose and mass
2. **Sum energies** across fractions
3. **Compare with accumulated dose × reference mass**
4. **Metric:** Energy conservation error should be **<1%** for high-quality DIR

### Advantages Over Geometric Metrics
- More clinically relevant than Jacobian determinants
- Directly reflects dose calculation accuracy
- Detects physically implausible mass mappings

---

## Clinical Implications for Adaptive Radiotherapy

### 1. Gold Standard for Dose Accumulation
- MDS provides **reliable correlation** between delivered dose and treatment outcomes
- Critical for **informed adaptation decisions** (escalation/de-escalation)

### 2. Adaptive Strategy Impact
- Enables accurate assessment of whether dose deviations are:
  - Due to **anatomical changes** (restore original plan)
  - Due to **biological response** (adapt dose levels)
- Without energy-conserving accumulation → **wrong adaptation decisions**

### 3. Outcome Model Training
- Accurate accumulated dose is essential for training TCP/NTCP models
- Enables reliable radiomics/delta-radiomics analysis

---

## Relevance to Proton Therapy (High Priority!)

### Why Even More Critical for Protons:
1. **Range sensitivity:** Protons are highly sensitive to tissue density
   - Small density changes → large Bragg peak position shifts
   - Energy-conserving accumulation ensures range changes are accurately tracked

2. **IMPT applications:** Paper explicitly cites IMPT literature
   - Intensity-modulated proton therapy requires precise dose tracking

3. **Biological adaptation:** 
   - RBE varies with depth/LET
   - Accurate physical dose accumulation is prerequisite for biological dose calculations

4. **Adaptive proton therapy:**
   - Online/offline adaptation decisions depend on accurate dose history
   - 10-40% dose errors (from DDS) → completely wrong adaptation strategy

---

## Relevance to Your Proposal

### 1. Objective 2 Enhancement
**Current:** "accumulated dose"  
**Should cite:** Energy-conserving dose summation (Zhong 2024) with DIR QA

**Suggested text:**
> "Accumulated dose computed via mass-weighted energy-conserving dose summation methods [Zhong2024], with deformable image registration (DIR) quality assurance using energy conservation metrics (<1% error threshold) per best practices [Brock2017]."

### 2. Task 2 Feature Engineering
Your AI model uses "accumulated dose" as a feature → **MUST use physically correct method**
- Wrong accumulation = wrong feature values = wrong AI predictions
- Energy-conserving method ensures reliable biological signal extraction

### 3. Task 3 Dose Optimization
Adaptation decisions require knowing "how much dose was actually delivered"
- DDS can be off by 10-40% → adaptation on wrong baseline
- MDS provides correct baseline for escalation/de-escalation decisions

### 4. Uncertainty Quantification
Energy conservation error serves as **QA metric** for DIR uncertainty:
- High energy error → low confidence in spatial mapping
- Can feed into your uncertainty-aware AI layer

---

## Implementation Notes for Your Project

### Computational Steps:
1. **For each fraction $i$:**
   - Compute dose distribution $D_i$ on fraction image
   - Get mass distribution $M_i$ from CT/CBCT (HU → density conversion)
   - Calculate energy: $E_i = D_i \times M_i$ (voxel-wise)

2. **Deformable registration:**
   - Map each fraction to reference image
   - Propagate energy grids (not dose grids!)

3. **Accumulate energy:**
   - Sum energies: $E_{total}(\nu) = \sum_i E_i(\nu)$

4. **Calculate accumulated dose:**
   - Compute average mass: $M_A(\nu) = \frac{1}{K}\sum_i M_i(\nu)$
   - Final dose: $D_T(\nu) = E_{total}(\nu) / M_A(\nu)$

5. **QA check:**
   - Energy conservation error per organ: $\frac{|E_{organ,accumulated} - \sum_i E_{organ,i}|}{\sum_i E_{organ,i}} < 1\%$

---

## New Bibliography Entry

```latex
\bibitem{zhong2024}
Zhong H. An energy-conserving dose summation method for dose accumulation in radiotherapy. \textit{Medical Physics}, 2024. https://doi.org/10.1002/mp.17514.
```

---

## Key Takeaways for Section 1.2

1. ✅ **Specify method:** Not just "accumulated dose" → "mass-weighted energy-conserving dose summation"
2. ✅ **Cite correctly:** Zhong 2024 for method, Brock 2017 for DIR best practices
3. ✅ **Include QA:** DIR quality assurance via energy conservation metrics
4. ✅ **Emphasize importance:** Especially critical for proton therapy (range sensitivity)
5. ✅ **Link to objectives:** Affects Task 2 (features), Task 3 (dose baseline), Task 4 (validation)
