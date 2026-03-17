import numpy as np
import pandas as pd
import train_model
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

def main():
    res = train_model.train_model()
    model = res['model']
    mapping = res['mapping']
    m = res['metrics']
    
    print(f"MAE (Margin of Error): {m['mae']:.2f} min | R2 (Accuracy): {m['r2']:.2%}")

    names = list(mapping.keys())

    while True:
        inp = input("\nRide: ").lower().strip()
        if inp == 'exit': 
            break

        matches = [n for n in names if inp in n]
        if not matches:
            print("No match found.")
            continue
        
        target = matches[0]
        if len(matches) > 1:
            print(f"Matches: {matches}")
            sel = input("Select specific: ").lower().strip()
            target = sel if sel in matches else matches[0]

        try:
            d = int(input("Day (0-6): "))
            h = int(input("Hour (0-23): "))
        except:
            print("Invalid input.")
            continue
            
        r_id = mapping[target]
        s = np.sin(2 * np.pi * h / 24.0)
        c = np.cos(2 * np.pi * h / 24.0)
        
        cols = ['day_of_week', 'hour_sin', 'hour_cos', 'ride_id']
        sample = pd.DataFrame([[d, s, c, r_id]], columns=cols)
        
        pred = int(round(model.predict(sample)[0]))
        
        print(f"Result for {target.upper()}: {pred:.1f}m (+/- {m['mae']:.1f})")

if __name__ == "__main__":
    main()