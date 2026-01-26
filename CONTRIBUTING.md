# Contributing to Adaptive Proton Therapy Research

Thank you for your interest in contributing to this PhD research project! This document provides guidelines for collaboration and contributions.

---

## 🎯 Project Status

**Current Phase**: PhD Proposal Development & Preliminary Validation  
**Status**: Submission-ready (v1.0)  
**Principal Investigator**: Saeed Sarbazzadeh Khosroshahi  
**Supervisor**: Prof. Stine Sofia Korreman  
**Institution**: Aarhus University & Danish Centre for Particle Therapy  

---

## 🤝 Ways to Contribute

### 1. Feedback & Review
- Review the proposal and provide scientific feedback
- Identify technical issues or methodological gaps
- Suggest improvements to validation strategies
- Share relevant literature we may have missed

### 2. Data Contributions
We welcome **multi-site collaborations** with institutions that have:
- Longitudinal proton therapy imaging (daily CBCT/in-room CT)
- Mid-treatment functional imaging (DW-MRI, PET)
- Clinical outcomes data
- Ground truth labels for biological response

**Requirements**:
- IRB/ethics approval for data sharing
- De-identification protocols
- Data use agreements
- RAPTORplus consortium membership (preferred)

### 3. Validation Cohorts
Help validate our methods by providing:
- External center holdout datasets (n≥30)
- Site-specific DIR QA benchmarks
- Physics QA baselines for CBCT/sCT conversion
- Clinical expert consensus labels

### 4. Technical Collaboration
Collaborate on:
- CBCT digital twin development
- Diffusion model training for biological synthesis
- Robust optimization algorithm implementation
- TPS integration (RayStation API)
- Conformal prediction calibration methods

### 5. Clinical Workflow Design
Input from clinical experts on:
- Adaptation trigger policies
- Escalation dose prescriptions
- Fallback strategies
- UI/UX for clinician review
- Acceptability rubric validation

---

## 📧 How to Contribute

### For Academic Collaborations:
**Email**: saeed.sarbazzadeh@clin.au.dk  
**Subject Line**: `[Collaboration] [Your Institution] - [Topic]`

**Please Include**:
- Your name, institution, and role
- Area of expertise relevant to this project
- Specific contribution you'd like to make
- Availability and timeline

### For Technical Issues/Suggestions:
**GitHub Issues**: Create an issue on this repository  
**Categories**:
- 🐛 Bug/Error in methodology
- 💡 Enhancement/Improvement
- 📚 Literature/Reference suggestion
- ❓ Question/Clarification
- 🔬 Validation/Data contribution

### For Data Sharing:
**Contact Supervisor**: Prof. Stine Sofia Korreman  
**Email**: stine.korreman@rm.dk  
**Requirements**:
- Formal data sharing agreement
- Ethics/IRB approval documentation
- De-identification certification

---

## 🔬 Research Ethics

### Data Privacy
- All patient data must be de-identified per GDPR/HIPAA
- Data use agreements required for multi-site collaborations
- Differential privacy (DP-SGD) for externally shared models
- Audit trails for all data access

### Research Integrity
- Pre-registered acceptance criteria (no p-hacking)
- Transparent reporting of limitations
- Reproducibility: version control, seeds logged
- Citation of all sources and collaborations

### Authorship
Contributions will be recognized following ICMJE guidelines:
- **Authorship**: Substantial contributions to conception, data acquisition, analysis/interpretation + drafting/revising + final approval
- **Acknowledgment**: Other contributions (funding, data provision, technical support)

---

## 📝 Contribution Process

### For Code/Methods (Future):
1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/your-feature-name`
3. **Make changes** with clear commit messages
4. **Add tests** if applicable
5. **Submit pull request** with description of changes
6. **Review process**: PI + supervisor will review

### For Proposal/Documentation:
1. **Open an issue** describing the suggested change
2. **Discuss** with PI before making major changes
3. **Submit revised text** via pull request or email
4. **Review** by PI + supervisor
5. **Incorporate** approved changes

---

## 🎓 Academic Standards

All contributions must adhere to:
- Scientific rigor and evidence-based recommendations
- Proper citation of sources (APA/Vancouver style)
- Clarity and precision in technical writing
- Reproducibility (code, parameters, seeds documented)
- Ethical research practices

---

## 🔒 Confidentiality

### Public Repository:
- Proposal text and methodology: **Public** (CC BY-NC 4.0)
- General validation results: **Public**
- Figures/diagrams: **Public**

### Confidential (Not in Repo):
- Patient data (NEVER shared publicly)
- Unpublished results
- Proprietary TPS configurations
- RAPTORplus internal documents

**If in doubt, ask before sharing.**

---

## 📅 Timeline & Availability

**Current**: Proposal phase (Q1 2026)  
**Next**: Task 1 implementation (Q2 2026)  
**Year 1**: Synthetic generation + response characterization  
**Year 2**: Dose optimization + integration  
**Year 3**: Clinical validation + thesis  

**Response Time**: We aim to respond to contributions within 2 weeks.

---

## 🌍 RAPTORplus Network

This PhD is part of the RAPTORplus Marie-Sklodowska-Curie-Action EU Doctoral Network.

**Preferred Collaborators**:
- RAPTORplus consortium members
- European proton therapy centers
- Academic institutions with relevant expertise

**External Collaborations**: Welcome, pending supervisor approval and data agreements.

---

## ❓ Questions?

**General Questions**: Open a GitHub issue  
**Collaboration Inquiries**: Email saeed.sarbazzadeh@clin.au.dk  
**Data Sharing**: Contact Prof. Korreman (stine.korreman@rm.dk)  
**RAPTORplus Network**: See [https://raptorplus.eu](https://raptorplus.eu)

---

## 🙏 Acknowledgments

We gratefully acknowledge contributions from:
- RAPTORplus consortium members
- Expert reviewers and advisors
- Data providers and clinical collaborators
- Open-source community (PyTorch, ASTRA, etc.)

---

**Thank you for your interest in advancing adaptive proton therapy!**

---

_Last Updated: January 26, 2026_  
_Version: 1.0_
