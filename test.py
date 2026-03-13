import pandas as pd
import requests
import pandas as pd
from datetime import datetime
import os
from datetime import datetime

row = {}

ride_name = "Space Mountain"
wait_time = 45
row[ride_name] = wait_time

ride_name = "Tron"
wait_time = 65
row[ride_name] = wait_time
time = ["15:00"]

df = pd.DataFrame([row], [time])

ride_name = "Space Mountain"
wait_time = 35
row[ride_name] = wait_time

ride_name = "Tron"
wait_time = 75
row[ride_name] = wait_time
time = ["16:00"]

df = pd.concat([df, pd.DataFrame([row], [time])])

print(df)

mkurl = "https://api.themeparks.wiki/v1/entity/75ea578a-adc8-4116-a54d-dccb60765ef9/live"

data = requests.get(mkurl).json()

for ride in data["liveData"]:
    if (
        ride.get("entityType") == "ATTRACTION"
        and "queue" in ride
        and "STANDBY" in ride["queue"]
    ):
        wait = ride["queue"]["STANDBY"]["waitTime"]
        print(ride["name"], wait)