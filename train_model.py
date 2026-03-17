from data_preparation import prepare_data
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import pandas as pd
import numpy as np

def train_model():
    df = prepare_data()
    
    data = df.melt(id_vars=['day_of_week', 'hour_sin', 'hour_cos'], 
                   var_name='ride_name', value_name='wait_time')
    
    data = data.dropna(subset=['wait_time'])
    data = data[data['wait_time'] != -1]

    data['ride_name_lower'] = data['ride_name'].str.lower()
    data['ride_name_lower'] = data['ride_name_lower'].astype('category')
    data['ride_id'] = data['ride_name_lower'].cat.codes
    
    X = data[['day_of_week', 'hour_sin', 'hour_cos', 'ride_id']]
    y = data['wait_time']
    
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(x_train, y_train)
    
    preds = rf.predict(x_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = rf.score(x_test, y_test)

    cats = data['ride_name_lower'].cat.categories
    mapping = {name: i for i, name in enumerate(cats)}
    
    return {
        'model': rf, 
        'mapping': mapping,
        'metrics': {'mae': mae, 'r2': r2}
    }