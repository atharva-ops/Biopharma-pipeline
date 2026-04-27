"""
Catenion Project — Mental Health Pipeline Mapper
Queries ClinicalTrials.gov API v2 for Depression & PTSD trials
"""

import requests
import pandas as pd
import json
import time

BASE_URL = "https://clinicaltrials.gov/api/v2/studies"
QUERIES = [
    ("Depression", "major depressive disorder"),
    ("PTSD", "PTSD"),
]

def fetch_trials(condition_label, query, max_results=500):
    """Fetch interventional drug trials from ClinicalTrials.gov v2 API."""
    all_studies = []
    next_token = None
    page = 0

    print(f"  Fetching {condition_label}...")

    while len(all_studies) < max_results:
        params = {
            "query.cond": query,
            "filter.overallStatus": "RECRUITING,ACTIVE_NOT_RECRUITING,COMPLETED,NOT_YET_RECRUITING",
            "filter.studyType": "INTERVENTIONAL",
            "pageSize": 100,
            "format": "json",
        }
        if next_token:
            params["pageToken"] = next_token

        resp = requests.get(BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        studies = data.get("studies", [])
        if not studies:
            break

        all_studies.extend(studies)
        page += 1
        print(f"    Page {page}: {len(all_studies)} studies so far")

        next_token = data.get("nextPageToken")
        if not next_token:
            break

        time.sleep(0.3)

    return all_studies

def extract_fields(study, condition_label):
    """Flatten nested ClinicalTrials v2 JSON into a flat dict."""
    ps = study.get("protocolSection", {})
    id_mod = ps.get("identificationModule", {})
    status_mod = ps.get("statusModule", {})
    design_mod = ps.get("designModule", {})
    sponsor_mod = ps.get("sponsorCollaboratorsModule", {})
    cond_mod = ps.get("conditionsModule", {})
    intervention_mod = ps.get("armsInterventionsModule", {})

    phases = design_mod.get("phases", [])
    phase = phases[0] if phases else "UNKNOWN"

    interventions = intervention_mod.get("interventions", [])
    drug_interventions = [i for i in interventions if i.get("type") in ("DRUG", "BIOLOGICAL", "COMBINATION_PRODUCT")]
    intervention_names = [i.get("name", "") for i in drug_interventions[:3]]

    lead_sponsor = sponsor_mod.get("leadSponsor", {})

    enrollment = design_mod.get("enrollmentInfo", {}).get("count")

    return {
        "nct_id": id_mod.get("nctId", ""),
        "title": id_mod.get("briefTitle", ""),
        "condition_label": condition_label,
        "conditions": "; ".join(cond_mod.get("conditions", [])),
        "status": status_mod.get("overallStatus", ""),
        "phase": phase,
        "sponsor": lead_sponsor.get("name", ""),
        "sponsor_class": lead_sponsor.get("class", ""),
        "intervention": "; ".join(intervention_names),
        "enrollment": enrollment,
        "start_date": status_mod.get("startDateStruct", {}).get("date", ""),
        "completion_date": status_mod.get("primaryCompletionDateStruct", {}).get("date", ""),
        "study_type": design_mod.get("studyType", ""),
    }

def clean_phase(phase):
    mapping = {
        "PHASE1": "Phase I",
        "PHASE2": "Phase II",
        "PHASE3": "Phase III",
        "PHASE4": "Phase IV",
        "EARLY_PHASE1": "Phase I",
        "NA": "N/A",
        "UNKNOWN": "Unknown",
    }
    return mapping.get(phase, phase)

def clean_sponsor_class(sc):
    mapping = {
        "INDUSTRY": "Industry",
        "NIH": "Academic/NIH",
        "FED": "Academic/NIH",
        "OTHER_GOV": "Academic/NIH",
        "INDIV": "Academic/NIH",
        "NETWORK": "Academic/NIH",
        "OTHER": "Academic/NIH",
        "UNKNOWN": "Unknown",
    }
    return mapping.get(sc, sc)

def main():
    all_records = []

    for label, query in QUERIES:
        studies = fetch_trials(label, query, max_results=500)
        for s in studies:
            rec = extract_fields(s, label)
            all_records.append(rec)

    df = pd.DataFrame(all_records)

    # Deduplicate by NCT ID (a trial may match both queries)
    df = df.drop_duplicates(subset="nct_id")

    # Clean
    df["phase_clean"] = df["phase"].apply(clean_phase)
    df["sponsor_class_clean"] = df["sponsor_class"].apply(clean_sponsor_class)

    # Filter to drug/biological only (some slipped through)
    df = df[df["study_type"] == "INTERVENTIONAL"]

    print(f"\nTotal unique trials: {len(df)}")
    print(df["phase_clean"].value_counts())
    print(df["sponsor_class_clean"].value_counts())

    df.to_csv("/home/claude/pipeline_data.csv", index=False)
    print("\nSaved to pipeline_data.csv")

    return df

if __name__ == "__main__":
    df = main()
