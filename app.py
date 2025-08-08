from analytics import load_energy_data,visualize_daily_usage,usage_by_appliance,hourly_base_usage # type: ignore
import streamlit as st
# if _name=="main_":
#     df=load_energy_data()
#     visualize_daily_usage(df)
#     usage_by_appliance(df)
#     hourly_base_usage(df)

#---Dashboard Header ---#
st.markdown("<h1 style='text-align:center;'>🏡AI Smart Energy Console</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>Detect •Forecast •Optimize ⚙</h3>", unsafe_allow_html=True)
# --- Custom CSS for Metric Boxes --- #
st.markdown("""
    <style>
    .metric-box {
        background-color: #1f2937;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        text-align: center;
        color: white;
        margin-top: 10px;
    }
    .metric-box h4 {
        font-size: 1.6rem;
        color: white;
        margin: 0;
    }
    .metric-box h2 {
        font-size: 1.0rem;
        margin: 5px 0 0 0;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# === Load Data ===#
df = load_energy_data()
#---Metric Cards----
col1,col2,col3=st.columns(3)
with col1:
    st.markdown(f"<div class='metric-box'><h4>Total Usage</h4><h2>{round(df['total_usage'].sum(),2)} kWh</h2></div>", unsafe_allow_html=True)
with col2:
    avg_day=round(df.groupby(df['timestamp'].dt.date)['total_usage'].sum().mean(),2)
    st.markdown(f"<div class='metric-box'><h4>Average Daily Usage</h4><h2>{avg_day} kWh</h2></div>", unsafe_allow_html=True)
with col3:
    ac_pct=round((df['ac_usage'].sum() / df['total_usage'].sum()) * 100, 1)
    st.markdown(f"<div class='metric-box'><h4>AC Usage</h4><h2>{ac_pct}%</h2></div>", unsafe_allow_html=True)
# === Charts ===#
st.markdown("## Daily Usage Trend")
st.pyplot(visualize_daily_usage(df))

st.markdown("## Appliance-Based Usage")
st.pyplot(usage_by_appliance(df))


st.markdown("## Hourly Usage Pattern")
st.pyplot(hourly_base_usage(df))




from analytics import forecast_future_usage
import altair as alt

st.header("🔮 Linear Forecast: Next 7 Days Energy Usage")

future_df, daily_forecast = forecast_future_usage(days=7)

# Line chart
line_chart = alt.Chart(daily_forecast).mark_line(point=True).encode(
    x='date:T',
    y='predicted_usage:Q',
    tooltip=['date:T', 'predicted_usage:Q']
).properties(
    width=700,
    height=400,
    title='Predicted Daily Total Usage (kWh)'
)

st.altair_chart(line_chart)

# Expandable table
with st.expander("📊 Detailed Hourly Predictions"):
    st.dataframe(future_df[['timestamp', 'predicted_usage']].reset_index(drop=True))
    
    
from analytics import predict_usage_given_ac

st.markdown("## 🎛️ Try Your Own AC Usage Scenario")

with st.form("ac_predict_form"):
    st.write("Enter your expected usage values for prediction:")
    ac_usage = st.slider("AC Usage (kWh)", 0.0, 2.0, 0.2, 0.01)
    hour = st.slider("Hour of Day", 0, 23, 18)
    day = st.slider("Day of Week (0=Mon, 6=Sun)", 0, 6, 0)
    is_weekend = st.selectbox("Is Weekend?", [0, 1])
    fridge_usage = st.slider("Fridge Usage (kWh)", 0.0, 0.5, 0.12, 0.01)
    washing_machine_usage = st.slider("Washing Machine Usage (kWh)", 0.0, 2.0, 0.0, 0.1)
    lights_usage = st.slider("Lights Usage (kWh)", 0.0, 2.0, 0.5, 0.01)
    submitted = st.form_submit_button("Predict Usage")

if submitted:
    pred = predict_usage_given_ac(ac_usage, hour, day, is_weekend, fridge_usage, washing_machine_usage, lights_usage)
    st.success(f"Predicted Total Usage: {pred:.2f} kWh")
    if ac_usage > 1.0:
        st.warning("High AC usage! Consider increasing the thermostat or using fans to save energy.")
    elif pred < 1.0:
        st.info("Your predicted usage is efficient. Good job!")
    else:
        st.info("Your predicted usage is moderate. Keep monitoring your appliances for savings.")