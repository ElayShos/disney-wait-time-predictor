from data_preparation import prepare_data
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import pandas as pd
import numpy as np

def train_model():
    df = prepare_data()
    df_long = df.melt(id_vars=['day_of_week', 'hour_sin', 'hour_cos'], var_name='ride_name', value_name='wait_time')
    df_long = df_long.dropna(subset=['wait_time'])
    df_long = df_long[df_long['wait_time'] != -1]

    df_long['ride_name_lower'] = df_long['ride_name'].str.lower()
    df_long['ride_name_lower'] = df_long['ride_name_lower'].astype('category')
    df_long['ride_id'] = df_long['ride_name_lower'].cat.codes
    
    X = df_long[['day_of_week', 'hour_sin', 'hour_cos', 'ride_id']]
    y = df_long['wait_time']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Accuracy check
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    accuracy_score = model.score(X_test, y_test) # R^2 Score

    ride_categories = df_long['ride_name_lower'].cat.categories
    ride_to_id = {name: i for i, name in enumerate(ride_categories)}
    
    return {
        'model': model, 
        'mapping': ride_to_id,
        'metrics': {'mae': mae, 'r2': accuracy_score}
    }