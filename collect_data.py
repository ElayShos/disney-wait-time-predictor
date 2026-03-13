import requests
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
import os

# ensure data folder exists
os.makedirs("data", exist_ok=True)

# park ids
mk = "75ea578a-adc8-4116-a54d-dccb60765ef9"
ep = "47f90d2c-e191-4239-a466-5892ef59a88b"
hs = "288747d1-8b4f-4a64-867e-ea7c9b27bad8"
ak = "1c84a229-8862-4648-9c71-378ddd2c7693"

parks = {
    "mk": mk,
    "ep": ep,
    "hs": hs,
    "ak": ak
}

base_url = "https://api.themeparks.wiki/v1/entity/{}/live"

# timestamp in Orlando time
timestamp = datetime.now(ZoneInfo("America/New_York")).replace(second=0, microsecond=0)

rows = []

for park_name, park_id in parks.items():

    url = base_url.format(park_id)
    data = requests.get(url).json()

    for ride in data["liveData"]:

        if ride.get("entityType") == "ATTRACTION":

            queue = ride.get("queue", {})
            standby = queue.get("STANDBY", {})

            wait_time = standby.get("waitTime")

            if wait_time is None:
                continue

            rows.append({
                "timestamp": timestamp,
                "park": park_name.upper(),
                "ride": ride["name"],
                "wait_time": wait_time,
                "hour": timestamp.hour,
                "day_of_week": timestamp.weekday()
            })

print("Collected rides:", len(rows))

df = pd.DataFrame(rows)

file = "data/wait_times.csv"

df.to_csv(
    file,
    mode="a",
    header=not os.path.exists(file),
    index=False
)

print("Saved data at:", timestamp)