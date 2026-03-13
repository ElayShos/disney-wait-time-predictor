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

parks = {
    mkurl: "mk",
    epurl: "ep",
    hsurl: "hs",
    akurl: "ak"
}

rides = {
    "mk": {
        "TRON Lightcycle / Run",
        "Seven Dwarfs Mine Train",
        "Jungle Cruise",
        "Tiana's Bayou Adventure",
        "Peter Pan's Flight",
        "Big Thunder Mountain Railroad",
        "Space Mountain",
        "The Barnstormer",
        "Dumbo the Flying Elephant",
        "Haunted Mansion",
        "it's a small world",
        "The Magic Carpets of Aladdin",
        "Mad Tea Party",
        "Mickey's PhilharMagic",
        "The Many Adventures of Winnie the Pooh",
        "Pirates of the Caribbean",
        "Tomorrowland Speedway",
        "Under the Sea - Journey of The Little Mermaid",
        "Monsters Inc. Laugh Floor",
        "Buzz Lightyear's Space Ranger Spin"
    },

    "ep": {
        "Test Track",
        "Guardians of the Galaxy: Cosmic Rewind",
        "Remy's Ratatouille Adventure",
        "Soarin'",
        "Living with the Land",
        "Spaceship Earth",
        "Mission: SPACE",
        "Frozen Ever After",
        "Gran Fiesta Tour Starring The Three Caballeros",
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
        "Star Tours - The Adventures Continue"
    },

    "ak": {
        "Expedition Everest - Legend of the Forbidden Mountain",
        "Avatar Flight of Passage",
        "Na'vi River Journey",
        "Kilimanjaro Safaris",
        "Kali River Rapids"
    }
}

wdw = [mkurl, epurl, hsurl, akurl]

timestamp = datetime.now(ZoneInfo("America/New_York"))

for park in wdw:

    park_name = parks[park]
    row = {}

    data = requests.get(park).json()

    for ride in data["liveData"]:

        if ride.get("entityType") == "ATTRACTION":

            ride_name = ride["name"]

            if ride_name not in rides[park_name]:
                continue

            if "queue" in ride and "STANDBY" in ride["queue"]:

                wait_time = ride["queue"]["STANDBY"]["waitTime"]

                row[ride_name] = wait_time if wait_time else None

    df = pd.DataFrame([row], [timestamp])

    file = "data/wait"+ park_name.upper() +".csv"

    if os.path.exists(file):
        df.to_csv(file, mode="a", header=False)
    else:
        df.to_csv(file)
    print("Data collected:", len(row))

print("Collected Data for all parks at", timestamp)