import numpy as np
import pandas as pd
import os
import glob
import math

def prepare_data():
    with open(os.path.join('rules', 'parks.txt'), 'r') as f:
        parks = [line.strip() for line in f]

    df_list = []
    
    for park in parks:
        try:
            path = os.path.join('data', '*', f'wait{park.upper()}.csv')
            files = glob.glob(path)
            
            if not files:
                continue
            
            df = pd.concat(pd.read_csv(f) for f in files)
            
            df.dropna(subset=df.columns[1:], how='all', inplace=True)
            
            timestamps = pd.to_datetime(df.iloc[:, 0], format='mixed')
            
            df['day_of_week'] = timestamps.dt.dayofweek
            df['hour'] = timestamps.dt.hour
            
            df['hour_sin'] = np.sin(2 * np.pi * df['hour']/24.0)
            df['hour_cos'] = np.cos(2 * np.pi * df['hour']/24.0)
            
            df.drop(df.columns[0], axis=1, inplace=True)
            df.drop(columns=['hour'], inplace=True)
            df = df.fillna(-1)

            new_cols = ['day_of_week', 'hour_sin', 'hour_cos']
            other_cols = [c for c in df.columns if c not in new_cols]
            df = df[new_cols + other_cols]

            df_list.append(df)
            df_new = pd.concat(df_list)

        except Exception as e:
            print(f"Error processing {park}: {e}")
            continue
        
    return df_new