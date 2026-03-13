import pandas as pd
import glob
import os
from pathlib import Path

def load(park):
    path = f"data\*\wait{park.upper()}.csv"
    all_files = glob.glob(path)

    if not all_files:
        print(f"No files found for park code: {park}")
        return None

    df_list = [] # initiating a new list of dates
    for f in all_files: # all_files holds a reference of all files of 'park' from all dates
        try: # try to perform without returning an error
            file_path = Path(f) # saves the value of the path as a path type
            date = file_path.parent.name # saves the file's parent name as the date
            df = pd.read_csv(f, index_col=0) # saving the csv of the file of that specific date into a data frame df
            df['date'] = date # creates a new COLUMN - syntax df['name'] is for columns, syntax df.loc['name'] is for rows
            df_list.append(df) # appends the new data frame df into the new list we initiated
            # so eventually what we got here is basically ALL the files combined from all dates of that specific park + a new column of dates.
        except:

