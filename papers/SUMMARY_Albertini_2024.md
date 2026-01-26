# Paper Summary: Albertini et al. (2024) - OAPT Implementation

## Full Citation
**Title:** First clinical implementation of a highly efficient daily online adapted proton therapy (DAPT) workflow

**Authors:** Albertini F, et al.

**Journal:** *Physics in Medicine & Biology*, 69 (2024) 215030

**DOI:** https://doi.org/10.1088/1361-6560/ad7cbd

---

## Main Focus
Clinical implementation and feasibility of **daily online adaptive proton therapy (DAPT)** workflow at the Paul Scherrer Institute (PSI).

---

## Key Findings

### Clinical Feasibility
- **First in-patient clinical delivery** of DAPT
- Demonstrated on **5 patients** with brain or skull base tumors
- Successfully delivered adapted plans in **>85% of fractions**

### Timing Constraints (CRITICAL FOR PROPOSAL)
- **Total treatment session:** Average **23 minutes** (range: 15–30 min)
  - Fits within standard 30-minute clinical slot
- **Adaptation process:** Average **7 minutes** (range: 3:30–16 min)
  - Includes: daily imaging, contouring, plan re-optimization, automated QA

### Clinical Impact
- **92% of fractions:** Adapted plans showed improved dose metrics for targets and/or OARs
- Compared to non-adapted plans

### Workflow Components
- Uses **in-room CT-on-rails** for daily imaging
- **Rigid propagation** of contours (anatomical adaptation)
- Full **re-optimization** of proton plan on daily anatomy
- Highly **automated QA**: geometric checks, sanity checks, independent dose calculations

---

## Relevance to Your Proposal

### 1. State-of-the-Art Citation
✅ **Use as reference** for current OAPT state-of-the-art (published 2024)

### 2. Timing Benchmarks
- Your proposal should reference these **realistic clinical timing constraints**:
  - Online adaptation must complete in **<10 minutes** (your current target aligns well)
  - Total workflow fits in **23-30 minute** slot

### 3. Current Limitation
- This implementation focuses on **anatomical adaptation only** (rigid propagation)
- Sets the stage for your project: need to move toward **biological adaptation**
- Your work extends beyond rigid/deformable geometry to biological response

### 4. Suggested Citation Points
**Introduction Section 1.1:**
> "Recent clinical implementations of online adaptive proton therapy (OAPT) have demonstrated feasibility with adaptation workflows completing in ~7 minutes within standard treatment slots \\cite{albertini2024}, yet these implementations focus primarily on anatomical restoration rather than biological response adaptation."

---

## Notes
- Does NOT explicitly discuss LET-aware evaluation or biological adaptation
- Focuses on technical workflow efficiency and anatomical adaptation
