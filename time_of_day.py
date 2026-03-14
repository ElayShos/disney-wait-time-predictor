import pandas as pd
import os
from pathlib import Path
from datetime import datetime
from help_func import convert_date

def round_to_5_as_text(number):

    if number is None or pd.isna(number):
        return None
    rounded = int(5 * round(number / 5))
    return f"\t{rounded}"

def analyze_times(park, user_date):
    if isinstance(user_date, str):
        date_obj, folder_date = convert_date(user_date)
    else:
        date_obj = user_date
        folder_date = date_obj.strftime("%Y-%m-%d")

    if folder_date is None: return # Safety stop

    input_path = os.path.join("data", folder_date, f"wait{park.upper()}.csv")
    if not os.path.exists(input_path):
        print(f"No data found for {park} on {folder_date}")
        return

    time_slots = {
        "Morning (05:00-10:00)": (5, 10),
        "Late Morning (10:00-12:00)": (10, 12),
        "Noon (12:00-14:00)": (12, 14),
        "Afternoon (14:00-16:00)": (14, 16),
        "Late Afternoon (16:00-18:00)": (16, 18),
        "Evening (18:00-20:00)": (18, 20),
        "Night (20:00-24:00)": (20, 24)
    }

    try:
        df = pd.read_csv(input_path, index_col=0)
        df.index = pd.to_datetime(df.index)
        results_dict = {}

        for ride in df.columns:
            if ride in ['date', 'time_of_day']: continue
            results_dict[ride] = {}
            for label, (start, end) in time_slots.items():
                mask = (df.index.hour >= start) & (df.index.hour < end)
                
                if mask.any():
                    avg_wait = df.loc[mask, ride].mean()
                    results_dict[ride][label] = round_to_5_as_text(avg_wait)
                else:
                    results_dict[ride][label] = None

        final_df = pd.DataFrame(results_dict).T
        output_dir = Path("analysis_results") / park.lower()
        output_dir.mkdir(parents=True, exist_ok=True)
        
        final_df.to_csv(output_dir / f"averages_{folder_date}.csv")
        print(f"Successfully saved averages for {park} to {output_dir}")

    except Exception as e:
        print(f"Error in analyze_times for {park}: {e}")

# analyze_times("MK", "2026-03-14")