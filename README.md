# Institutional Intelligence: User Segmentation Model using Unsupervised Learning

## Executive Summary
This repository contains the end-to-end implementation of a behavioral user segmentation model developed for the **Jorge Roa Martínez Library** at the **Universidad Tecnológica de Pereira (UTP)**. By extracting and consolidating **1,784,919 transactional records**, the project transitions traditional library descriptive statistics into institutional intelligence, providing an empirical framework to optimize digital resource allocation and support early student retention strategies.

## Tech Stack & Methods
* **Language:** Python
* **Data Processing:** Pandas, NumPy (Advanced ETL, Schema Harmonization)
* **Machine Learning:** Scikit-Learn (`DBSCAN` for noise/outlier diagnostic filter, `K-Means` for final partitioning)
* **Interactive Visualization:** Streamlit & Plotly Express (Dynamic Operational Dashboard)
* **Validation Framework:** Elbow Method & Silhouette Criterion ($K=4$, Score: **0.4269**)

---

## Analytical Pipeline & Core Implementation

1. **Advanced ETL & Data Integrity:** Unified highly heterogeneous ecosystems (Physical Loans vs. Digital Access Logs). Handled manual nomenclature variances and resolved a critical **43% missing value rate** in academic attributes via a multi-period longitudinal cross-imputation algorithm, raising analytical data integrity above **95%**.
2. **Behavioral Feature Engineering (Adapted RFM):** Formulated an institutional framework by mapping Recency (`recency_dias`), Frequency (`frequency_dias_activos` using unique active days to prevent transaction volume bias), and Digital Intensity (`intensidad_digital`). Applied a logarithmic transformation (`log1p`) to mitigate extreme positive skewness prior to feature scaling via `StandardScaler`.
3. **Clustering Architecture:** Evaluated dataset robustness using density-based filtering (`DBSCAN`) as a diagnostic step, ensuring structural noise was minimized. Built the final partitioning structure using stabilized `K-Means` ($K=4$), optimizing both mathematical cohesion and institutional interpretability.

---

## Institutional Insights & Strategic Action Windows

The model identified 4 clear behavioral profiles across the analyzed population:
* **Digital Consolidated:** High-frequency, active users relying heavily on digital platforms. Represents the largest and most valuable segment, structurally tied to Engineering and Health faculties.
* **Digital Lost:** Users with minor, virtual-only footprints over a year ago. High potential window for re-engagement campaigns.
* **Physical Active:** Veteran library users with steady, physical-only book loans and high average longevity.
* **Físico Perdido (Physical Lost):** Historical physical-only users who have not interacted with library services in over 2 years.

### Data-Driven Impact
* **Budget Optimization:** Validated that digital subscriptions (e.g., *ScienceDirect*, *Scopus*) represent the core utility center of the institution, allowing directors to anchor budget negotiations to objective interaction volume.
* **Student Retention Coordination:** Identified a distinct drop in activity during **Weeks 4 and 5 of the academic semester** for vulnerable clusters. This provides an empirical action window for the library to sync with University Student Welfare units to trigger targeted academic counseling.

---

## Streamlit Dashboard Features (`src/app.py`)
The deployed web application translates the mathematical model into an interactive monitoring system including:
* **Metric Overviews:** Real-time summary of user tenure, active days, and digital behavior.
* **Cross-Analysis Visuals:** Dynamic Plotly scatter and box plots evaluating feature metrics.
* **Top Resources KPI:** Automated tracking of the Top 10 physical and digital academic materials demanded per user profile.
