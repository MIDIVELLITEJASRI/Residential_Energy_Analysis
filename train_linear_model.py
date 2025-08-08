import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib
from analytics import load_energy_data  # your custom function

def prepare_data(df):
    df['hour'] = df['timestamp'].dt.hour
    df['day'] = df['timestamp'].dt.dayofweek
    features = ['hour', 'day', 'is_weekend', 'ac_usage', 'fridge_usage', 'washing_machine_usage', 'lights_usage']
    X = df[features]
    y = df['total_usage']
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_linear_model(csv_path="data/energy_data.csv", model_path="models/linear_model.pkl"):
    df = load_energy_data(csv_path)
    
    X_train, X_test, y_train, y_test = prepare_data(df)
    
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save the model using joblib
    joblib.dump(model, model_path)

    print(f"✅ Linear Regression model saved at: {model_path}")

if  __name__ == "__main__":
    train_linear_model()