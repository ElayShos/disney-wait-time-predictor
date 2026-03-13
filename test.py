import requests

# Hollywood Studios Live API
hs_url = "https://api.themeparks.wiki/v1/entity/288747d1-8b4f-4a64-867e-ea7c9b27bad8/live"

try:
    print("Connecting to API...")
    response = requests.get(hs_url)
    response.raise_for_status()
    data = response.json()
    
    print("\n--- ALL RIDES IN HOLLYWOOD STUDIOS ---")
    found_any = False
    for ride in data.get("liveData", []):
        if ride.get("entityType") == "ATTRACTION":
            print(f"Name: {ride['name']}")
            found_any = True
            
    if not found_any:
        print("No attractions found in the live data.")
        
except Exception as e:
    print(f"Error: {e}")

input("\nPress Enter to close...")