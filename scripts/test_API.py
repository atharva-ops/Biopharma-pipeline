import requests
import pandas as pd
import time

CONDITIONS = [
    ("Depression/TRD", "treatment resistant depression"),
    ("PTSD", "PTSD"),
    ("Bipolar", "bipolar disorder"),
    ("Schizophrenia", "schizophrenia"),
    ("Anxiety", "generalized anxiety disorder"),
]

results = []

for condition_label, query in CONDITIONS:
    print(f"Fetching {condition_label}...")
    resp = requests.get(
        "https://clinicaltrials.gov/api/v2/studies",
        params={
            "query.cond": query,
            "pageSize": 100,
            "format": "json",
        }
    )
    print("Status:", resp.status_code)
    print("Response:", resp.text[:200])
    data = resp.json()

    for study in data["studies"]:
        protocol = study["protocolSection"]
        phase = protocol["designModule"].get("phases", "UNKNOWN")
        if phase != "UNKNOWN" and phase != ["NA"]:
            title = protocol["identificationModule"].get("officialTitle", "NO TITLE")
            sponsor = protocol["sponsorCollaboratorsModule"]["leadSponsor"].get("name", "UNKNOWN")
            sponsor_class = protocol["sponsorCollaboratorsModule"]["leadSponsor"].get("class", "UNKNOWN")
            results.append({
                "condition": condition_label,
                "title": title,
                "phase": phase,
                "sponsor": sponsor,
                "sponsor_class": sponsor_class,
            })

    time.sleep(0.5)

df = pd.DataFrame(results)
df["phase"] = df["phase"].apply(lambda x: x[0] if isinstance(x, list) else x)
df.to_csv("pipeline_data.csv", index=False, quotechar='"', quoting=1)
print("Done! Saved", len(results), "trials across", len(CONDITIONS), "conditions")