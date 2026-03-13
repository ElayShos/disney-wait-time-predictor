import pandas as pd
import glob
import os

def load_all_data(park_code):
    path = f"data/*/wait{park_code.upper()}.csv"
    all_files = glob.glob(path)
    
    if not all_files:
        return None
        
    df_list = [pd.read_csv(f, index_col=0) for f in all_files]
    return pd.concat(df_list).sort_index()

def get_wait_level(current_wait, ride_stats):
    if pd.isna(current_wait):
        return "Unknown"
    
    low = ride_stats['25%']
    high = ride_stats['75%']
    
    if current_wait <= low:
        return "Low"
    elif current_wait >= high:
        return "High"
    else:
        return "Average"

parks = ['MK', 'EP', 'HS', 'AK']

for park in parks:
    df = load_all_data(park)
    if df is None:
        continue
        
    print(f"\n--- Analysis for {park} ---")
    
    stats = df.describe()
    
    for ride in df.columns:
        if ride in stats:
            ride_info = stats[ride]
            latest_wait = df[ride].iloc[-1]
            level = get_wait_level(latest_wait, ride_info)
            
            print(f"{ride}: Current Wait: {latest_wait} mins -> Level: {level}")
            print(f"   (Historical: Avg: {ride_info['mean']:.1f}, Low threshold: {ride_info['25%']}, High threshold: {ride_info['75%']})")