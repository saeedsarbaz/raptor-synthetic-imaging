# Changelog

All notable changes to the PhD proposal will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to semantic versioning principles.

---

## [1.0.0] - 2026-01-26

### Summary
Complete revision incorporating expert feedback across all three priority tiers (Critical, High Priority, Polish). Total of 14 items addressed resulting in submission-ready proposal.

### Added

#### TIER 1: CRITICAL
- **Section 1 (Introduction, Line 95)**: Added biological ground truth validation strategy with physics QA and conformal prediction gating
- **Section 3.2 (Task 2, Lines 392-415)**: Added comprehensive 3-tier ground truth approach:
  - PRIMARY: Synthetic with known decomposition
  - SECONDARY: Clinical surrogates (volume change, ΔHU, consensus)
  - TERTIARY: Biological anchors (DW-MRI ADC, PET SUV) where available
  - Explicit limitation acknowledgment
- **Abstract + Section 1 (Lines 56, 118-120)**: Added LET/RBE framework positioned as exploratory with dual reporting:
  - Clinical dose (RBE=1.1) for prescriptions
  - Variable RBE (McNamara model) for sensitivity analysis
  - ΔNTCP sensitivity to RBE model choice

#### TIER 2: HIGH PRIORITY
- **Section 3.1 (Task 1, Lines 232-236)**: Upgraded CBCT physics:
  - Physics-informed scatter model (single-scatter + density-dependent residual)
  - Polyenergetic FDK with beam-hardening compensation
  - SPR validation: RMSE ≤0.02
  - Joint WEPL/dose fidelity: median ≤1.5mm, P95 ≤3mm
  - Concurrent acceptance requirement
- **Section 3.1 (Task 1, Lines 208-209)**: Added comprehensive leakage controls:
  - Dose-dropout during training (30% of epochs)
  - Inference-time dose shuffles
  - Negative controls (no-dose runs)
  - Tissue-bounded HU priors (-1000 to +2000 HU)
  - Counterfactual testing (±20% dose → <5% texture change)
- **Section 3.2 (Task 2, Lines 354-367)**: Added domain adaptation framework:
  - Site-specific DIR QA thresholds (H&N: ≤2-3mm; Lung: ≤3-5mm)
  - Domain-adversarial training
  - Test-time entropy minimization
  - Physics provenance controls (angles, filter, I₀, scatter α)
- **Section 3.2 (Task 2, After Line 453)**: Added calibration monitoring subsection:
  - Held-out calibration set per site (30% withheld)
  - Temperature scaling with drift monitoring (ECE >0.05 triggers re-fit)
  - Site-wise conformal threshold (α=0.10 for 90% coverage)
  - External holdout validation requirement
- **Section 3.4 (Task 4, After Line 609)**: Added external validation with power analysis:
  - External center hold-out for generalization
  - Power analysis via TOST: n=30/site, α=0.05, power=80%, SD=8pp
  - Target n=50/site for mixed-effects analysis
  - Generalization acceptance criteria (F1 ≥0.65, AUC-PR ≥0.70, ECE ≤0.05)
- **Section 3.3 (Task 3, After Line 511)**: Added scenario bank expansion:
  - Correlated setup/range scenarios
  - HU→SPR bias models for sCT uncertainty
  - 4D respiratory phases for lung (repainting ≥3-4, gating, breath-hold)
  - CVaR implementation within TPS

#### TIER 3: POLISH
- **Section 3.2 (Task 2, After Line 344)**: Added IBSI Part 2 delta-radiomics protocol:
  - 6-step extraction procedure
  - Rigid + DIR alignment to planning CT
  - ROI propagation with TG-132 QA
  - SAME voxel grid feature extraction
  - Δfeature = (fraction_k - baseline) / baseline
  - Site-wise ComBat harmonization
  - ICC <0.75 feature removal
  - Specific features: GLCM, GLRLM, GLSZM, shape
  - Bin width: 25 HU; Resampling: 1.5mm isotropic
- **Section 3.4 (Task 4, After Line 610)**: Added 4D evaluation for motion sites:
  - 4D dose accumulation across respiratory phases
  - Phase-averaged DVH and worst-phase metrics
  - Interplay mitigation KPIs (repainting ≥3-4, gating, breath-hold)
  - 4D robust pass rate
- **Section 3.4 (Task 4, After Line 610)**: Added clinician acceptability rubric:
  - Likert scale (1-5) with 5 anchored criteria:
    1. Target coverage
    2. OAR safety
    3. Hotspot location plausibility
    4. Adaptation rationale clarity
    5. Workflow time acceptability
  - Audit logging for defer/restore/adapt decisions
- **References (After Line 889)**: Added four critical references:
  - Unkelbach et al. 2018 (robust proton planning)
  - McNamara et al. 2015 (phenomenological RBE model)
  - Vovk et al. 2005 (conformal prediction framework)
  - Grassberger et al. 2013 (motion interplay in lung proton therapy)

### Changed

#### TIER 1: CRITICAL
- **Section 3.3 (Task 3, Lines 480-487, 495-508)**: Replaced voxel-level with ROI-level adaptation:
  - ROI-level prescriptions for biological regions
  - Spatial regularization (total variation penalty) for deliverability
  - RESTORATION (anatomy): Restore D₉₅, D₉₈ on conformal-accepted anatomical ROIs
  - ADAPTATION (biology): Modify ROI prescription by Δ (+5 to +10 Gy for regression/progression; -5 to -10 Gy for favorable response)
  - MIXED: Weighted ROI prescription λD_plan + (1-λ)D_adapt averaged over ROI
  - OAR constraint: D_max increase ≤2 Gy across all scenarios

### Removed

#### TIER 3: POLISH
- **Section 3.1 (Task 1, Line 304)**: Removed FID (Fréchet Inception Distance) metric:
  - Rationale: Dose-centric validation is sufficient for proton therapy
  - FID has limitations in medical imaging contexts
  - Secondary metrics (SSIM, PSNR, LPIPS) retained

---

## [0.9.0] - 2026-01-25 (Pre-Revision Baseline)

### Initial Submission
- Complete PhD proposal draft with four-task methodology
- Preliminary CBCT digital twin validation results
- Initial acceptance criteria defined
- Basic references and structure established

### Known Issues/Gaps (Addressed in v1.0)
- Biological validation strategy needed clarification
- LET/RBE positioning unclear
- Voxel-level optimization not deliverable
- Missing calibration monitoring
- Missing external validation power analysis
- Incomplete IBSI Part 2 details
- Missing key references

---

## Future Planned

### [1.1.0] - Target: Q2 2026
- Add actual figure files (methodology overview, synthetic generation, etc.)
- Compile final PDF
- Address minor technical corrections from referee review
- Add data availability inventory table
- Add ROI generation algorithm specification

### [1.2.0] - Target: Q3 2026
- Add preliminary Task 1 results (full synthetic cohort v0.9)
- Update validation results section
- Add ablation study results
- Expand risk mitigation based on early findings

### [2.0.0] - Target: 2027
- Task 2 model performance results
- Multi-site validation outcomes
- Updated timeline based on Year 1 progress
- First publication references

---

## Review History

### Expert Referee Review - 2026-01-26
- **Overall Score**: 9.5/10 (95%)
- **Recommendation**: ACCEPT WITH MINOR REVISIONS
- **Strengths**: Scientific rigor, innovation, clinical impact
- **Main Concerns**: Synthetic-to-real gap, data availability, 4D lung complexity
- **Required Changes**: 7 items (see referee_review_report.md)

---

## Contributors

- **Saeed Sarbazzadeh Khosroshahi** - PhD Candidate, Proposal Author
- **Prof. Stine Sofia Korreman** - Primary Supervisor
- **RAPTORplus Consortium** - Collaborative Input & Review

---

## Notes

- All changes follow pre-registered acceptance criteria
- Revisions maintain consistency with RAPTORplus objectives
- Version numbering: MAJOR.MINOR.PATCH
  - MAJOR: Fundamental methodology changes
  - MINOR: Significant additions (new sections, results)
  - PATCH: Minor clarifications, corrections

---

[1.0.0]: https://github.com/yourusername/adaptive-proton-therapy/releases/tag/v1.0.0
[0.9.0]: https://github.com/yourusername/adaptive-proton-therapy/releases/tag/v0.9.0
