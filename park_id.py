import requests

url = "https://api.themeparks.wiki/v1/destinations"

data = requests.get(url).json()

for destination in data["destinations"]:
    if "Disney World" in destination["name"]:
        for park in destination["parks"]:
            print(park["name"], park["id"])