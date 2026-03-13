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
print(load_all_data("MK"))