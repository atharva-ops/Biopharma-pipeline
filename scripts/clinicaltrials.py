import requests
url = "https://clinicaltrials.gov/api/v2/studies"
params = {
    "filter.advanced": "AREA[Phase]PHASE3", "filter.overallStatus": "RECRUITING",
    "fields": "NCTId,BriefTitle,OverallStatus,LeadSponsorName,Condition,StartDate",
    "pageSize": 20,
    "format": "json"
}
response = requests.get(url, params=params)
data = response.json()
for study in data["studies"]:
    try:
        info = study["protocolSection"]
        title = info["identificationModule"]["briefTitle"]
        status = info["statusModule"]["overallStatus"]
        sponsor = info["sponsorCollaboratorsModule"]["leadSponsor"]["name"]
        conditions = info["conditionsModule"].get("conditions", ["N/A"])
        condition = conditions[0]
        print(f"Title: {title}")
        print(f"Status: {status}")
        print(f"Sponsor: {sponsor}")
        print(f"Condition: {condition}")
        print("---")
    except KeyError:
        continue