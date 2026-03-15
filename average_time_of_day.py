import pandas as pd
import glob
import os

def average_hourly_wait_time(park):
    path = os.path.join('data','*', f'wait{park.upper()}.csv')
    files = glob.glob(path)
    df = pd.concat(pd.read_csv(f) for f in files)
    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], format='mixed')
    df.set_index(df.columns[0], inplace=True)

    rules = []
    with open(os.path.join('rules','time_of_day.txt'), 'r') as f:
        for line in f:
            name, start, end = line.strip().split(',')
            rules.append((name, start, end))

    time_blocks = {}
    for name, start, end in rules:
        time_blocks[name] = df.between_time(start, end)

    row = {}

    def fix_num(x):
        x = int(x) if pd.notna(x) else 0
        if (x != 13):
            x = round(x/5) * 5
        return x

    for ride in df.columns:
        avg_lines = []

        for name, start, end in rules:
            val = time_blocks[name][ride].replace(0, pd.NA).mean()
            val = fix_num(val)
            avg_lines.append(val)

        row[ride] = avg_lines
    new_df = pd.DataFrame(row, index=[name for name, _, _ in rules])
    print("finished calculating average wait times")

    os.makedirs(os.path.join('analysis_results', 'average_wait_times'), exist_ok=True)
    path_save = os.path.join('analysis_results', 'average_wait_times', f'average_wait_{park.upper()}.csv')
        
    new_df.to_csv(path_save)


average_hourly_wait_time('mk')
average_hourly_wait_time('ep')
average_hourly_wait_time('hs')
average_hourly_wait_time('ak')

    