# Paper Summary: Gambetta et al. (2025) - Near Real-Time OAPT Review

## Full Citation
**Title:** Current status and upcoming developments for online adaptive proton therapy enabling a closed feedback loop for near real-time adaptation

**Authors:** Virginia Gambetta, Kristin Stützer, Christian Richter

**Journal:** *Frontiers in Oncology* (Section: Radiation Oncology)

**Volume/Year:** Volume 15, 2025 (Published: 17 December 2025)

**DOI:** https://doi.org/10.3389/fonc.2025.1660605

---

## Main Focus

Comprehensive review of **Online Adaptive Proton Therapy (OAPT)** current status and the emerging paradigm of **Near Real-Time Adaptive Proton Therapy (NAPT)**, which creates a closed feedback loop using in vivo verification to trigger adaptations.

---

## OAPT Workflow Components (Current State-of-the-Art)

### 1. Imaging
- **Primary modality:** 3D volumetric CBCT or in-room CT at treatment position
- **Emerging:** In-beam MRI and Proton CT (pCT) for improved SPR accuracy and soft tissue contrast

### 2. Online Contouring
- **AI/Deep Learning:** U-Net architectures for automatic segmentation
- **Deformable Image Registration (DIR):** Contour propagation from planning CT
- **Bottleneck:** Manual review still time-consuming despite automation

### 3. Plan Adaptation Strategies
- **Simple:** Isocenter shifts only
- **Intermediate:** Online constrained re-optimization
- **Advanced:** Full ROI-objective-based re-optimization
- **Enabling technology:** GPU-based dose engines (e.g., matRad) allow re-optimization in seconds

### 4. Online QA
- **Shift:** From physical phantoms to software-based methods
- **Independent dose calculation:** 2nd dose engine verification
- **Log-file analysis:** Real-time delivery verification

### 5. In Vivo Verification
- **Prompt Gamma (PG) Imaging:** Nearly instant feedback during beam delivery for range verification
- **PET imaging:** Post-treatment verification of dose delivery

---

## Timing Benchmarks (CRITICAL for Your Proposal)

### Clinical Reality:
- **Core adaptation workflow:** **10-11 minutes** (image registration to delivery start)
  - From Figure 4 in paper
- **Total treatment session:** **23-30 minutes** (includes setup and delivery)
  - Matches Albertini 2024 data

### Clinical Implementations:
- **ProtOnART consortium** (Dresden + Leuven)
  - Demonstrated **daily OAPT is clinically feasible**
  - Standard clinical practice, not experimental

---

## Near Real-Time Adaptive Proton Therapy (NAPT)

### Concept: Closed Feedback Loop
1. **Online Treatment Verification** (e.g., Prompt Gamma during delivery)
2. **Real-time deviation detection** (organ motion, range shifts)
3. **Immediate adaptation trigger** without full re-imaging
4. **Intra-fractional adaptation** (within single treatment session)

### Key Enabler: Prompt Gamma
- **Real-time range verification** during beam delivery
- Can detect 3-5mm range shifts
- Enables "stop and adapt" within fraction

### Advantage Over Traditional OAPT:
- OAPT: Adapt between fractions based on static daily image
- NAPT: Adapt within fraction based on live delivery feedback

---

## Verification Methods

### 1. Prompt Gamma Imaging
- **Timing:** Instantaneous (during beam delivery)
- **Purpose:** Range verification, dose deposition confirmation
- **Feedback loop:** Triggers near real-time adaptation

### 2. PET Imaging
- **Timing:** Post-treatment (minutes to hours)
- **Purpose:** Verify accumulated dose, detect systematic errors
- **Feedback loop:** Informs next-fraction adaptation

### 3. Log-File Analysis
- **Real-time:** During delivery
- **Verifies:** Beam delivery parameters, spot positions, energies

---

## Technological Requirements & Challenges

### Automation Needs:
1. **AI-based automatic contouring** (reduce manual review time)
2. **Decision Support Systems (DSS)** to autonomously flag "need for adaptation"
3. **GPU-accelerated dose calculation** for real-time re-optimization

### Image Quality Challenges:
- **CBCT artifacts:** Scatter, HU drift (echoes Gregg 2025 findings)
- **Solutions:** Synthetic CT generation, DIR-based corrections

### Regulatory/Clinical:
- Need for standardized QA protocols
- Evidence of clinical benefit vs. resource utilization
- Training requirements for clinical staff

---

## Relevance to Your Proposal

### 1. State-of-the-Art Citation for Section 2.1
**Use to update "Adaptive Proton Therapy" subsection:**

> "Online adaptive proton therapy (OAPT) has advanced from experimental concept to clinical reality, with daily implementations achieving adaptation workflows in 10-11 minutes within standard 23-30 minute treatment sessions \\cite{albertini2024, gambetta2025}. Current OAPT implementations (e.g., ProtOnART consortium) focus on anatomical adaptation using AI-based contouring and GPU-accelerated re-optimization \\cite{gambetta2025}."

### 2. Verification Context (Section 2.1)
**Add paragraph on verification:**

> "In vivo verification methods, including prompt gamma imaging and PET, enable closed feedback loops for near real-time adaptation, detecting range deviations and triggering intra-fractional plan adjustments \\cite{gambetta2025}. However, these methods verify delivered dose distributions rather than characterizing the biological nature of anatomical changes."

### 3. Research Gap Connection
**Links to your project's novelty:**

- Current OAPT/NAPT: Focuses on **anatomical** adaptation and **dosimetric** verification
- **Missing:** Classification of whether changes are anatomical vs. biological
- **Your contribution:** AI-based change characterization to inform adaptation strategy

### 4. Decision Support System Context
**Your Task 2 AI fits into this paradigm:**

- Gambetta mentions "Decision Support Systems to flag need for adaptation"
- **Your system extends this:** Not just "adapt or not" but "restore, adapt, or combined strategy"

---

## Key Quotes for Proposal

1. **On current OAPT status:**
> "Daily online adaptive proton therapy is now clinically feasible with modern tools, completing adaptation workflows in under 10-11 minutes."

2. **On verification focus:**
> "In vivo verification provides a closed feedback loop for range verification and delivered dose confirmation."

3. **Research gap your project addresses:**
> "While near real-time verification enables rapid dosimetric feedback, distinguishing anatomical from biological components of image changes remains an unmet need for optimal adaptation strategy selection."

---

## New Bibliography Entry

```latex
\bibitem{gambetta2025}
Gambetta V, Stützer K, Richter C. Current status and upcoming developments for online adaptive proton therapy enabling a closed feedback loop for near real-time adaptation. \textit{Frontiers in Oncology}, 2025; 15:1660605. https://doi.org/10.3389/fonc.2025.1660605.
```

---

## Implementation Notes

### For Section 2.1 Revision:
1. ✅ Cite Albertini 2024 + Gambetta 2025 for clinical OAPT timing
2. ✅ Add paragraph on verification methods and feedback loops
3. ✅ Maintain connection to your research gap (biological vs. anatomical)

### Timing References to Use:
- **10-11 min:** Core adaptation workflow (Gambetta 2025)
- **23-30 min:** Total treatment session (Albertini 2024, Gambetta 2025)
- **<10 min goal:** Your proposal's target (ambitious but aligned with state-of-the-art)
