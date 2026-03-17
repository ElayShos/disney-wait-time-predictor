import numpy as np
import train_model

def run_prediction():
    print("Training model and checking accuracy...")
    package = train_model.train_model()
    model = package['model']
    mapping = package['mapping']
    metrics = package['metrics']
    
    print(f"\nModel Accuracy Metrics:")
    print(f"- Average Error (MAE): {metrics['mae']:.2f} minutes")
    print(f"- Accuracy Score (R2): {metrics['r2']:.2%}")

    all_rides = list(mapping.keys())

    while True:
        user_input = input("\nEnter Ride Name (or 'exit'): ").lower().strip()
        if user_input == 'exit': break

        matches = [ride for ride in all_rides if user_input in ride]
        if not matches:
            print(f"Error: '{user_input}' not found.")
            continue
        
        ride_name = matches[0] if len(matches) == 1 else ""
        if not ride_name:
            print(f"Matches: {', '.join(matches)}")
            selection = input("Which one? ").lower().strip()
            ride_name = selection if selection in matches else matches[0]

        try:
            day_val = int(input("Day (0-6): "))
            hour_val = int(input("Hour (0-23): "))
        except ValueError:
            print("Error: Numbers only.")
            continue
            
        ride_id = mapping[ride_name]
        h_sin = np.sin(2 * np.pi * hour_val / 24.0)
        h_cos = np.cos(2 * np.pi * hour_val / 24.0)
        
        features = [[day_val, h_sin, h_cos, ride_id]]
        prediction = model.predict(features)[0]
        
        print(f"\n--- Prediction for {ride_name.upper()} ---")
        print(f"Estimated Wait: {prediction:.1f} minutes")
        print(f"Confidence (Avg Error): +/- {metrics['mae']:.1f} min")

if __name__ == "__main__":
    run_prediction()