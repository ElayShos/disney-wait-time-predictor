import pandas as pd
import glob
import os
from pathlib import Path

# --- Helper Functions ---

def load_all_data(park_code):
    """Loads CSV files based on naming: waitMK.csv, waitEP.csv, etc."""
    path = f"data/*/wait{park_code.upper()}.csv"
    all_files = glob.glob(path)
    
    if not all_files:
        print(f"No files found for park code: {park_code}")
        return None
        
    df_list = []
    for f in all_files:
        file_path = Path(f)
        try:
            df = pd.read_csv(f, index_col=0)
            # Use folder name as date reference
            df['date'] = file_path.parent.name
            df_list.append(df)
        except Exception as e:
            print(f"Error reading file {f}: {e}")
    
    return pd.concat(df_list).sort_index() if df_list else None

def save_daily_distribution(df, park_code, date_str):
    """Calculates distribution with custom ranges and Closed Down (NaN) percentage"""
    # Define starts: [5, 20, 35, 50, ...] and ends: [15, 30, 45, 60, ...]
    bins_start = list(range(5, 215, 15)) 
    bins_end = [b + 10 for b in bins_start] 
    
    output_lines = [
        f"Daily Analysis for Park: {park_code.upper()}",
        f"Date: {date_str}",
        "=" * 45
    ]

    for ride in df.columns:
        if ride == 'date':
            continue
            
        # Get all samples for this ride (including NaNs)
        all_samples = df[ride]
        total_count = len(all_samples)
        
        if total_count == 0:
            continue
            
        output_lines.append(f"\nRide: {ride}")
        has_visible_data = False
        
        # 1. Calculate Closed Down (NaN) percentage
        nan_count = all_samples.isna().sum()
        if nan_count > 0:
            nan_pct = (nan_count / total_count) * 100
            output_lines.append(f"  Closed Down   : {nan_pct:>5.1f}%")
            has_visible_data = True

        # 2. Calculate Standby wait time ranges
        # Convert to numeric for range calculation
        wait_times = pd.to_numeric(all_samples, errors='coerce').dropna()
        
        for start, end in zip(bins_start, bins_end):
            count = ((wait_times >= start) & (wait_times <= end)).sum()
            pct = (count / total_count) * 100
            
            if pct > 0:
                label = f"{start}-{end}"
                output_lines.append(f"  {label.ljust(14)}: {pct:>5.1f}%")
                has_visible_data = True
        
        if not has_visible_data:
            output_lines.append("  No status recorded for this ride today.")
            
        output_lines.append("-" * 20)

    # --- Directory Logic ---
    date_folder = Path("analysis_results") / park_code
    date_folder.mkdir(parents=True, exist_ok=True)
    
    filename = date_folder / f"distribution_{date_str}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

# --- Main Logic ---

if __name__ == "__main__":
    park_codes = ['mk', 'ep', 'hs', 'ak']

    for code in park_codes:
        print(f"Processing: {code}...")
        df_all = load_all_data(code)
        
        if df_all is None:
            continue
            
        all_dates = df_all['date'].unique()
        
        for current_date in all_dates:
            df_today = df_all[df_all['date'] == current_date]
            save_daily_distribution(df_today, code, current_date)
            
        print(f"Done processing {code}.")

    print("\nAll tasks finished. Check 'analysis_results' folder.")