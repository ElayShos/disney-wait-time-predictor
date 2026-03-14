from time_of_day import analyze_times
from analyze_data import analyze_distribution
from zoneinfo import ZoneInfo
from datetime import datetime

parks = {"mk", "ep", "hs", "ak"}
now_orlando = datetime.now(ZoneInfo("America/New_York"))
timestamp = now_orlando.strftime("%Y-%m-%d %H:%M")

print(f"Starting analysis for timestamp: {timestamp}")

for park in parks:
    analyze_times(park, timestamp)
    analyze_distribution(park, timestamp)

print("All tasks completed.")