# Paper Summary: Vestergaard et al. (2024) - CBCT to sCT for Proton Dose

## Full Citation
**Title:** Proton dose calculation on cone-beam computed tomography using unsupervised 3D deep learning networks

**Authors:** Casper Dueholm Vestergaard, Ulrik Vindelev Elstrøm, Ludvig Paul Muren, Jintao Ren, Ole Nørrevang, Kenneth Jensen, Vicki Trier Taasti

**Journal:** *Physics and Imaging in Radiation Oncology* 32 (2024) 100658

**DOI:** https://doi.org/10.1016/j.phro.2024.100658

**Year:** 2024

---

## Main Focus

Evaluation of **unsupervised 3D deep learning networks** for converting CBCT images to synthetic CT (sCT) to enable **accurate proton dose calculation** for online adaptive proton therapy (OAPT).

---

## Deep Learning Methods Tested

### Three Architectures Compared:
1. **CycleGAN** - Cycle-consistent Generative Adversarial Network
2. **CUT** - Contrastive Unpaired Translation
3. **CycleCUT** - Fusion of both approaches

### Key Characteristics:
- **Unsupervised**: No paired CBCT-CT training data required
- **3D networks**: Better preserve spatial consistency across slices vs. 2D approaches
- **Training data**: 82 head-and-neck (H&N) cancer patients
- **Test set**: 20 H&N patients
- **Ground truth**: Resampled fan-beam CT (gt-rCT)

---

## CRITICAL FINDING: Dose Accuracy vs. Image Quality

### **The Paper's Central Message:**
> **Dose accuracy, not just image similarity metrics (SSIM/MAE), is the key validator for sCT.**

While image quality metrics (PSNR, SSIM) showed slight variations between architectures, **these differences did NOT translate into significant differences in dose calculation accuracy.**

---

## Dose Accuracy Results (PRIMARY METRICS)

### 3D Gamma Pass Rates (GPR):
**All three networks achieved:**
- **3%/3mm:** **99.6%** median pass rate
- **2%/2mm:** **~98.7%** median pass rate
- **1%/2mm:** **>97% (~97.5%)** median pass rate (MOST STRINGENT)

✅ **Clinical significance:** Even with strictest criteria (1%/2mm), dose calculations on sCT are highly accurate.

### Dose-Volume Histogram (DVH) Metrics:
- **Target volumes:** Median deviations close to **zero**
- **Mean dose difference:** **<0.5%** for target volumes
- **Clinical impact:** Negligible dosimetric differences vs. ground truth CT

### Speed:
- **sCT generation time:** ~**74 seconds (~1.2 minutes)** for full 3D volume
- ✅ **Clinically feasible** for real-time online workflows

---

## Image Quality Results (SECONDARY METRICS)

### Image Similarity:
- **Mean Absolute Error (MAE):** ~**30 HU** across all networks
- **Mean Error (ME):** **-1.0 to +1.1 HU**
- **SSIM:** **~0.89-0.90**

### Important Note:
- **CycleCUT** showed slightly better image quality metrics
- **BUT:** No significant difference in dose accuracy between architectures
- **Conclusion:** Image quality metrics alone are insufficient to validate sCT for dose calculation

---

## Clinical Application

### Anatomical Site:
- **Head-and-Neck (H&N) cancer** patients
- **102 patients total** (82 training, 20 testing)

### OAPT Workflow Integration:
- **Fast reconstruction** (~1 min) supports daily online adaptation
- **High dose accuracy** enables confident dose re-calculation on daily anatomy
- **No paired training data needed** (unsupervised approach)

---

## Limitations

1. **Anatomical coverage:** H&N only; other sites (pelvic, thoracic) require validation
2. **Motion:** Sites with more motion or larger anatomical variations need testing
3. **Computational requirements:** 3D networks require more GPU memory than 2D models
4. **Training time:** 3D approaches are slower to train

---

## Relevance to Your Proposal

### For Section 2.2 (AI in Radiation Oncology):

**Current text mentions:**
> "diffusion probabilistic models generate synthetic CT from CBCT for dose calculation"

**Should update to:**
> "Recent evaluations demonstrate unsupervised 3D deep learning achieves >97% gamma pass rates (1%/2mm criterion) for proton dose calculation on CBCT-derived synthetic CT, with dose accuracy—not just image similarity metrics—serving as the critical validator \\cite{vestergaard2024}."

### Key Points to Emphasize:

1. **Dose accuracy is the gold standard** (not SSIM/MAE)
2. **High gamma pass rates** (>97% for 1%/2mm) prove clinical viability
3. **Fast reconstruction** (~1 min) supports online workflows
4. **Unsupervised methods** reduce training data requirements

---

## Connection to Your Research

### Parallel to Your Task 1 (Change Classification):
- **Their challenge:** Generate accurate sCT from CBCT
- **Their solution:** Deep learning with dose-based validation
- **Your challenge:** Classify image changes as anatomical vs. biological
- **Your approach:** AI-based characterization with treatment-informed validation

### Validation Philosophy:
- **Their insight:** Image quality metrics ≠ clinical validity; must validate with **dose accuracy**
- **Your equivalent:** Classification accuracy ≠ clinical validity; must validate with **adaptation strategy outcome**

---

## New Bibliography Entry

```latex
\bibitem{vestergaard2024}
Vestergaard CD, Elstrøm UV, Muren LP, Ren J, Nørrevang O, Jensen K, Taasti VT. Proton dose calculation on cone-beam computed tomography using unsupervised 3D deep learning networks. \textit{Physics and Imaging in Radiation Oncology}, 2024; 32:100658. https://doi.org/10.1016/j.phro.2024.100658.
```

---

## Key Takeaways

1. ✅ **Clinical OAPT viability:** CBCT→sCT with deep learning is clinically ready
2. ✅ **Dose-centric validation:** Must validate with dose metrics, not just image quality
3. ✅ **Speed:** 1-minute sCT generation fits OAPT workflows (7-11 min total)
4. ⚠️ **Site-specific:** H&N validated; other anatomies need testing
5. 🔬 **Unsupervised advantage:** No paired training data required
