import pandas as pd
import glob
import os
from pathlib import Path
from datetime import datetime

def analyze_distribution_csv(park, user_date):
    # 1. Convert input date format (dd/mm/yyyy -> yyyy-mm-dd)
    try:
        date_obj = datetime.strptime(user_date, "%d/%m/%Y")
        folder_date = date_obj.strftime("%Y-%m-%d")
    except ValueError:
        print("Invalid date format! Please use dd/mm/yyyy")
        return

    # 2. Construct the input path
    input_path = os.path.join("data", folder_date, f"wait{park.upper()}.csv")
    files = glob.glob(input_path)

    if not files:
        print(f"No data found for {park} on {folder_date} at {input_path}")
        return

    file = files[0]

    # 3. Define the ranges
    bins_start = list(range(5, 215, 15)) 
    bins_end = [b + 10 for b in bins_start]
    range_labels = [f"{s}-{e}" for s, e in zip(bins_start, bins_end)]

    try:
        df = pd.read_csv(file, index_col=0)
        
        # Results will be stored here
        results = []

        for ride in df.columns:
            if ride == 'date': continue
            
            all_samples = df[ride]
            total_count = len(all_samples)
            if total_count == 0: continue
            
            # Initialize row data for this ride
            ride_data = {"Ride": ride}
            
            # Calculate Closed Down %
            nan_count = all_samples.isna().sum()
            ride_data["Closed Down"] = round((nan_count / total_count) * 100, 1) if nan_count > 0 else 0
            
            # Calculate Range %
            wait_times = pd.to_numeric(all_samples, errors='coerce').dropna()
            for start, end in zip(bins_start, bins_end):
                count = ((wait_times >= start) & (wait_times <= end)).sum()
                pct = (count / total_count) * 100
                label = f"{start}-{end}"
                ride_data[label] = round(pct, 1)

            results.append(ride_data)

        # 4. Create DataFrame
        final_df = pd.DataFrame(results)
        
        # Ensure 'Ride' and 'Closed Down' are the first columns
        cols = ['Ride', 'Closed Down'] + [c for c in final_df.columns if c not in ['Ride', 'Closed Down']]
        final_df = final_df[cols]

        # 5. Save Logic
        output_dir = Path("analysis_results") / park.lower()
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = output_dir / f"distribution_{folder_date}.csv"
        final_df.to_csv(filename, index=False)

    except Exception as e:
        print(f"Error: {e}")

# --- Main Interaction ---
if __name__ == "__main__":
    print("--- Disney World Distribution Analyzer ---")
    u_date = input("Enter date (dd/mm/yyyy): ")
    u_park = input("Enter park (mk, ep, hs, ak): ").lower()
    
    analyze_distribution_csv(u_park, u_date)