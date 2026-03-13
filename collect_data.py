# -*- coding: utf-8 -*-
import requests
import pandas as pd
import os
from datetime import datetime
from zoneinfo import ZoneInfo

# Park IDs
mk = "75ea578a-adc8-4116-a54d-dccb60765ef9"
ep = "47f90d2c-e191-4239-a466-5892ef59a88b"
hs = "288747d1-8b4f-4a64-867e-ea7c9b27bad8"
ak = "1c84a229-8862-4648-9c71-378ddd2c7693"

parks = {
    f"https://api.themeparks.wiki/v1/entity/{mk}/live": "mk",
    f"https://api.themeparks.wiki/v1/entity/{ep}/live": "ep",
    f"https://api.themeparks.wiki/v1/entity/{hs}/live": "hs",
    f"https://api.themeparks.wiki/v1/entity/{ak}/live": "ak"
}

rides = {
    "mk": {
        "TRON Lightcycle / Run", "Seven Dwarfs Mine Train", "Jungle Cruise",
        "Tiana's Bayou Adventure", "Peter Pan's Flight", "Big Thunder Mountain Railroad",
        "Space Mountain", "The Barnstormer", "Dumbo the Flying Elephant",
        "Haunted Mansion", "it's a small world", "The Magic Carpets of Aladdin",
        "Mad Tea Party", "Mickey's PhilharMagic", "The Many Adventures of Winnie the Pooh",
        "Pirates of the Caribbean", "Tomorrowland Speedway", 
        "Under the Sea - Journey of The Little Mermaid", "Monsters Inc. Laugh Floor",
        "Buzz Lightyear's Space Ranger Spin"
    },
    "ep": {
        "Test Track", "Guardians of the Galaxy: Cosmic Rewind", "Remy's Ratatouille Adventure",
        "Soarin'", "Living with the Land", "Spaceship Earth", "Mission: SPACE",
        "Frozen Ever After", "Gran Fiesta Tour Starring The Three Caballeros",
        "The Seas with Nemo & Friends"
    },
    "hs": {
        "Star Wars: Rise of the Resistance", 
        "Rock 'n' Roller Coaster Starring Aerosmith",
        "The Twilight Zone Tower of Terror", 
        "Millennium Falcon: Smugglers Run",
        "Slinky Dog Dash", 
        "Mickey & Minnie's Runaway Railway", 
        "Toy Story Mania!",
        "Star Tours"
    },
    "ak": {
        "Expedition Everest - Legend of the Forbidden Mountain", "Avatar Flight of Passage",
        "Na'vi River Journey", "Kilimanjaro Safaris", "Kali River Rapids"
    }
}

# Time setup
now_orlando = datetime.now(ZoneInfo("America/New_York"))
date_str = now_orlando.strftime("%Y-%m-%d")
timestamp = now_orlando.strftime("%Y-%m-%d %H:%M")

# Create a specific directory for the date: data/YYYY-MM-DD
target_dir = os.path.join("data", date_str)
os.makedirs(target_dir, exist_ok=True)

for url, park_name in parks.items():
    row = {}
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        for ride in data.get("liveData", []):
            if ride.get("entityType") == "ATTRACTION":
                ride_name = ride["name"]
                
                # Check for match using startswith
                match = next((r for r in rides[park_name] if ride_name.startswith(r)), None)

                if match:
                    if "queue" in ride and "STANDBY" in ride["queue"]:
                        wait_time = ride["queue"]["STANDBY"]["waitTime"]
                        row[match] = wait_time if wait_time is not None else None

        if row:
            df_new = pd.DataFrame([row], index=[timestamp])
            
            # File path: data/YYYY-MM-DD/waitMK.csv
            file_name = f"wait{park_name.upper()}.csv"
            file_path = os.path.join(target_dir, file_name)

            if os.path.exists(file_path):
                old_df = pd.read_csv(file_path, index_col=0)
                df_combined = pd.concat([old_df, df_new], sort=False)
                df_combined.to_csv(file_path)
            else:
                df_new.to_csv(file_path)
                
            print(f"Updated {park_name} for {timestamp}")

    except Exception as e:
        print(f"Error collecting data for {park_name}: {e}")

print("Job completed.")