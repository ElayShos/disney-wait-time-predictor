import pandas as pd
import glob
import os
from pathlib import Path
from datetime import datetime

def round_to_5(number):
    """Rounds a number to the nearest multiple of 5"""
    if number is None or pd.isna(number):
        return None
    return int(5 * round(number / 5))

def analyze_times(park, date_str):
    try:
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        folder_date = date_obj.strftime("%Y-%m-%d")
    except ValueError:
        print("Invalid date format! Please use dd/mm/yyyy")
        return

    input_path = os.path.join("data", folder_date, f"wait{park.upper()}.csv")
    files = glob.glob(input_path)

    if not files:
        print(f"No data found for {park} on {folder_date}")
        return

    file = files[0]

    time_slots = {
        "Morning (05-10)": (5, 10),
        "Late Morning (10-12)": (10, 12),
        "Noon (12-14)": (12, 14),
        "Afternoon (14-16)": (14, 16),
        "Late Afternoon (16-18)": (16, 18),
        "Evening (18-20)": (18, 20),
        "Night (20-24)": (20, 24)
    }

    try:
        df = pd.read_csv(file, index_col=0)
        df.index = pd.to_datetime(df.index)
        
        results_dict = {}

        for ride in df.columns:
            if ride == 'date': continue
            
            results_dict[ride] = {}

            for label, (start, end) in time_slots.items():
                mask = (df.index.hour >= start) & (df.index.hour < end)
                avg_wait = df.loc[mask, ride].mean()
                
                # Apply the rounding to 5 logic here
                results_dict[ride][label] = round_to_5(avg_wait)

        final_df = pd.DataFrame(results_dict).T
        
        output_dir = Path("analysis_results") / park.lower()
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = output_dir / f"averages_{folder_date}.csv"
        final_df.to_csv(filename)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("--- Disney World Wait Time Analyzer ---")
    user_date = input("Which date (dd/mm/yyyy): ")
    user_park = input("Which park (mk, ep, hs, ak): ").lower()
    
    analyze_times(user_park, user_date)