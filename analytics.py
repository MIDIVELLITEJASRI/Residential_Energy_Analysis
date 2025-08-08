import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def load_energy_data(filepath="data/energy_data.csv"):
    df = pd.read_csv(filepath, parse_dates=['timestamp'])
    return df

def visualize_daily_usage(df):
    df['date'] = df['timestamp'].dt.date
    daily_usage = df.groupby('date')['total_usage'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=daily_usage, x='date', y='total_usage', marker='o', ax=ax)
    ax.set_title('Daily Energy Usage')
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Usage (kWh)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig
    
def usage_by_appliance(df):
    avg_usage = df[['ac_usage', 'fridge_usage', 'washing_machine_usage', 'lights_usage']].mean()
    fig,ax=plt.subplots(figsize=(6,6))
    plt.pie(avg_usage, labels=avg_usage.index, autopct='%1.1f%%', startangle=90)
    ax.set_title('Average Energy Usage by Appliance')
    ax.axis('equal')
    return fig

def hourly_base_usage(df):
    df['hour'] = df['timestamp'].dt.hour
    hourly_usage = df.groupby('hour')['total_usage'].mean().reset_index()
    fig,ax=plt.subplots(figsize=(12, 6))
    sns.barplot(data=hourly_usage, x='hour', y='total_usage')
    ax.set_title('Average Hourly Energy Usage')
    ax.set_label('Hour of Day')
    ax.set_ylabel('Average Usage (kWh)')
    plt.xticks(rotation=0)
    plt.tight_layout()
    return fig

import pandas as pd
import joblib
import datetime
import numpy as np

def generate_future_features(days=7):
    now = datetime.datetime.now()
    future_dates = [now + datetime.timedelta(days=i) for i in range(1, days + 1)]
    records = []

    for date in future_dates:
        for hour in range(24):  # hourly predictions
            dt = datetime.datetime(date.year, date.month, date.day, hour)
            record = {
                "hour": hour,
                "day": dt.weekday(),
                "is_weekend": 1 if dt.weekday() >= 5 else 0,
                "ac_usage": np.random.uniform(0.05, 0.3),
                "fridge_usage": np.random.uniform(0.1, 0.15),
                "washing_machine_usage": np.random.choice([0.0, 1.5], p=[0.8, 0.2]),
                "lights_usage": np.random.uniform(0.2, 0.9),
                "timestamp": dt
            }
            records.append(record)

    future_df = pd.DataFrame(records)
    return future_df

def forecast_future_usage(model_path="models/linear_model.pkl", days=7):
    model = joblib.load(model_path)
    future_df = generate_future_features(days)

    features = ['hour', 'day', 'is_weekend', 'ac_usage', 'fridge_usage', 'washing_machine_usage', 'lights_usage']
    future_df['predicted_usage'] = model.predict(future_df[features])

    # Aggregate daily usage
    future_df['date'] = future_df['timestamp'].dt.date
    daily_forecast = future_df.groupby('date')['predicted_usage'].sum().reset_index()

    return future_df,daily_forecast


def predict_usage_given_ac(ac_usage, hour, day, is_weekend, fridge_usage, washing_machine_usage, lights_usage, model_path="models/linear_model.pkl"):
    import joblib
    model = joblib.load(model_path)
    features = [[hour, day, is_weekend, ac_usage, fridge_usage, washing_machine_usage, lights_usage]]
    predicted = model.predict(features)[0]
    return predicted