import pandas as pd
import os
from pathlib import Path
from help_func import convert_date

def analyze_distribution(park, user_date):
    if isinstance(user_date, str):
        date_obj, folder_date = convert_date(user_date)
    else:
        date_obj = user_date
        folder_date = date_obj.strftime("%Y-%m-%d")

    if folder_date is None: return

    input_path = os.path.join("data", folder_date, f"wait{park.upper()}.csv")
    if not os.path.exists(input_path):
        print(f"No data for distribution: {park} on {folder_date}")
        return

    bins_start = list(range(5, 215, 15)) 
    bins_end = [b + 10 for b in bins_start]

    try:
        df = pd.read_csv(input_path, index_col=0)
        results = []

        for ride in df.columns:
            if ride in ['date', 'time_of_day']: continue
            
            all_samples = df[ride]
            total_count = len(all_samples)
            if total_count == 0: continue
            
            ride_data = {"Ride": ride}
            nan_count = all_samples.isna().sum()
            ride_data["Closed Down"] = round((nan_count / total_count) * 100, 1)
            
            wait_times = pd.to_numeric(all_samples, errors='coerce').dropna()
            for start, end in zip(bins_start, bins_end):
                count = ((wait_times >= start) & (wait_times <= end)).sum()
                ride_data[f"{start}-{end}"] = round((count / total_count) * 100, 1)

            results.append(ride_data)

        final_df = pd.DataFrame(results)
        cols = ['Ride', 'Closed Down'] + [c for c in final_df.columns if c not in ['Ride', 'Closed Down']]
        final_df = final_df[cols]

        output_dir = Path("analysis_results") / park.lower()
        output_dir.mkdir(parents=True, exist_ok=True)
        final_df.to_csv(output_dir / f"distribution_{folder_date}.csv", index=False)
        print(f"Successfully saved distribution for {park}")

    except Exception as e:
        print(f"Error in analyze_distribution for {park}: {e}")