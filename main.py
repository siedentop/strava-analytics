import requests
import json
import os

TOKEN = os.environ.get("STRAVA_BEARER")

try:
    response_length = 100000
    data = []
    page = 1
    while response_length > 0:
        r = requests.get(
            "https://www.strava.com/api/v3/athlete/activities?per_page=30",
            headers={f"Authorization": "Bearer {TOKEN}"},
            params={"per_page": 30, "page": page},
        )
        r.raise_for_status()
        d = r.json()
        response_length = len(d)
        page += 1
        data.extend(d)

finally:
    print(f"Length: {len(data)} / {page}")

    with open("output.json", "w") as fh:
        json.dump(data, fh)
