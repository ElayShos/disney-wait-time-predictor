import os
import pandas as pd
import glob

def run_analysis():
    # Get the directory where the script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(current_dir, 'analysis_results')
    
    if not os.path.exists(base_path):
        print(f"Error: Base directory '{base_path}' not found.")
        return

    # Create the output directory for aggregated results
    output_dir = os.path.join(base_path, 'averages')
    os.makedirs(output_dir, exist_ok=True)

    parks = ['mk', 'ep', 'hs', 'ak']
    
    for park in parks:
        park_folder = os.path.join(base_path, park)
        
        if not os.path.exists(park_folder):
            continue
            
        # Search for files named averages_*.csv within each park folder
        search_pattern = os.path.join(park_folder, 'averages_*.csv')
        file_list = glob.glob(search_pattern)
        
        if not file_list:
            print(f"No files starting with 'averages_' found in {park_folder}")
            continue
            
        print(f"Processing {len(file_list)} files for {park}...")
        
        all_dfs = []
        for file in file_list:
            try:
                # Load CSV, automatically detecting tab/comma separators
                df = pd.read_csv(file, index_col=0, sep=None, engine='python')
                
                # Clean the ride names (index) to ensure duplicates are merged correctly
                # This removes leading/trailing spaces and hidden tab characters
                df.index = df.index.astype(str).str.strip()
                
                # Convert all columns to numeric to ensure math works
                df = df.apply(pd.to_numeric, errors='coerce')
                
                all_dfs.append(df)
            except Exception as e:
                print(f"Error reading file {file}: {e}")
        
        if all_dfs:
            # Combine all files found for this park
            combined_df = pd.concat(all_dfs)
            
            # COMBINE AND AVERAGE:
            # groupby(level=0) groups by the ride name.
            # .mean() averages the wait times for the same time slots.
            final_df = combined_df.groupby(combined_df.index).mean()
            
            # Clean up: round to 1 decimal and sort rides alphabetically
            final_df = final_df.round(1).sort_index()
            
            # Save the final consolidated file
            save_path = os.path.join(output_dir, f'{park}.csv')
            final_df.to_csv(save_path)
            print(f"Successfully saved aggregated averages to: {save_path}")

if __name__ == '__main__':
    run_analysis()