# Mental Health Pipeline Intelligence
### *CNS Drug Development: Real Progress or Pipeline Theatre?*

A Python pipeline that pulls live clinical trial data from ClinicalTrials.gov and analyses industry commitment across 5 major mental health indications.

Built as a strategic intelligence tool to answer one question: **is the pharmaceutical industry actually solving mental health, or just creating the appearance of activity?**

---

## Key Finding

When you map industry sponsorship across development stages, a striking pattern emerges:

| Indication | Late-Stage Industry Sponsorship |
|---|---|
| Anxiety | 75% |
| Schizophrenia | 63% |
| Bipolar | 45% |
| Depression / TRD | **22%** |
| PTSD | **0%** |

Industry commits heavily where trials are predictable — and systematically retreats from Depression and PTSD, the two largest unmet markets in mental health. This is not a science problem. It is a risk appetite problem. And it represents a first-mover commercial opportunity.

---

## Data Source

All data pulled live from the [ClinicalTrials.gov REST API v2](https://clinicaltrials.gov/api/v2/studies).

- **191 interventional trials** across 5 CNS indications
- Indications: Depression/TRD, PTSD, Bipolar, Schizophrenia, Anxiety
- Sponsor classification: INDUSTRY / NIH / FED / OTHER
- Phase classification: Early stage (Phase I/II) vs Late stage (Phase III/IV)
- Data current as of April 2026

---

## How To Run

**1. Install dependencies**
```bash
pip install requests pandas matplotlib
```

**2. Fetch live data**
```bash
python scripts/test_API.py
```
This queries the ClinicalTrials.gov API and saves `data/pipeline_data.csv`.

**3. Run analysis**
```bash
python analyses/analyse.py
```
This generates industry sponsorship breakdowns by indication and development stage.

---

## Strategic Context

This project was built to demonstrate how programmatic access to public clinical trial data can generate strategic insights comparable to bespoke pharma consulting deliverables — at a fraction of the time and cost.

The analysis surfaces a clear gap: **Depression and PTSD are the largest unmet needs in mental health, yet have the lowest industry commitment in late-stage development.** Academic institutions are filling the void, but cannot bring drugs to market alone. The company that commits capital to late-stage trials in these indications captures a market with near-zero competition.

---

## Author

**Atharva Patharkar**  
PhD in Chemical Biology (magna cum laude), Humboldt University Berlin  
[LinkedIn](www.linkedin.com/in/atharva-patharkar-b84790227) · [GitHub](https://github.com/atharva-ops)
