import requests
import pandas as pd
from datetime import datetime
import os
from datetime import datetime
from zoneinfo import ZoneInfo

mk = "75ea578a-adc8-4116-a54d-dccb60765ef9"
ep = "47f90d2c-e191-4239-a466-5892ef59a88b"
hs = "288747d1-8b4f-4a64-867e-ea7c9b27bad8"
ak = "1c84a229-8862-4648-9c71-378ddd2c7693"

mkurl = "https://api.themeparks.wiki/v1/entity/" + mk + "/live"
epurl = "https://api.themeparks.wiki/v1/entity/" + ep + "/live"
hsurl = "https://api.themeparks.wiki/v1/entity/" + hs + "/live"
akurl = "https://api.themeparks.wiki/v1/entity/" + ak + "/live"

wdw = [mkurl, epurl, hsurl, akurl]

timestamp = datetime.now(ZoneInfo("America/New_York"))

for park in wdw:

    row = {}

    data = requests.get(park).json()

    for ride in data["liveData"]:

        if ride.get("entityType") == "ATTRACTION" and "queue" in ride and "STANDBY" in ride["queue"]:

            ride_name = ride["name"]
            wait_time = ride["queue"]["STANDBY"]["waitTime"]

            row[ride_name] = wait_time

    df = pd.DataFrame([row], [timestamp])

    parks = {
        mkurl: "mk",
        epurl: "ep",
        hsurl: "hs",
        akurl: "ak"
    }

    park_name = parks[park]

    file = "data/wait"+ park_name.upper() +".csv"

    if os.path.exists(file):
        df.to_csv(file, mode="a", header=False)
    else:
        df.to_csv(file)
    print("Data collected:", len(row))

print("Collected Data for all parks at", timestamp)