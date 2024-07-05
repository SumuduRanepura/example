import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Load the Excel data
file_path = 'C:\\Users\\DELL\\Desktop\\historical_data.xlsx'
df = pd.read_excel(file_path)

# Ensure the 'Date' column is in datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Remove duplicates by summing refill counts for the same dates
df = df.groupby(['Date', 'Initially Purchased Bottle Amount', 'Customer Location'], as_index=False).agg({'Refill Count': 'sum'})

# Adjust data based on initial bottle purchases and refill frequency
def calculate_refill_frequency(initial_bottles):
    if initial_bottles >= 10:
        return 1  # once a week
    elif 4 <= initial_bottles <= 7:
        return 2  # twice a week
    elif 1 <= initial_bottles <= 3:
        return 3  # three times a week
    return 0

df['Weekly Refill Frequency'] = df['Initially Purchased Bottle Amount'].apply(calculate_refill_frequency)

# Calculate metrics
today = datetime.today().date()
today_refills = df.loc[df['Date'] == pd.Timestamp(today), 'Refill Count'].sum()

# Define the login function
def login():
    st.title("Water Supply Co. - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "password":
            st.session_state["logged_in"] = True
            st.success("Login successful!")
        else:
            st.session_state["logged_in"] = False
            st.error("Invalid username or password")

# Function to predict using ARIMA model
def predict_refills(historical_data):
    # Fill in missing dates with zero refills
    historical_data = historical_data.asfreq('D', fill_value=0)

    # Train ARIMA model
    model = ARIMA(historical_data, order=(5,1,0))
    model_fit = model.fit()

    # Forecast next 7 days
    forecast = model_fit.forecast(steps=7)
    forecast = forecast.round().astype(int)  # Round the forecast to the nearest whole number
    return forecast

# Dashboard Page
def dashboard():
    st.title("Water Supply Co. - Dashboard")
    st.write("Welcome to the dashboard! Here you can view your data and manage your water supply system.")

    st.sidebar.title("Navigation")
    pages = ["Overview", "Predictions", "Historical Data", "Settings", "Profile"]
    page = st.sidebar.radio("Go to", pages)

    if page == "Overview":
        show_overview(today_refills)
    elif page == "Predictions":
        show_predictions()
    elif page == "Historical Data":
        show_historical_data()
    elif page == "Settings":
        show_settings()
    elif page == "Profile":
        show_profile()

def show_overview(today_refills):
    st.subheader("Overview")
    
    # Dropdown for initial bottle amount
    initial_bottles = st.selectbox("Select Initial Bottle Amount", options=df['Initially Purchased Bottle Amount'].unique())
    
    # Dropdown for customer location
    customer_location = st.selectbox("Select Customer Location", options=df['Customer Location'].unique())

    # Filter data based on selections
    filtered_data = df[(df['Initially Purchased Bottle Amount'] == initial_bottles) & (df['Customer Location'] == customer_location)]

    # Prepare historical data for ARIMA model
    historical_data = filtered_data.set_index('Date')['Refill Count']

    if not historical_data.empty:
        # Get forecast
        forecast = predict_refills(historical_data)
    else:
        forecast = [0] * 7  # Default to zero if no historical data is available
    
    st.write("Key Metrics:")
    col1, col2, col3 = st.columns(3)
    col1.metric("Today's Refills", today_refills)
    col2.metric("Next 7-Day Forecast", sum(forecast))
    col3.metric("Avg Daily Refills", np.mean(historical_data))

    st.subheader("7-Day Refill Predictions")
    st.write(forecast)

    # Plotting the forecast
    next_seven_days = pd.date_range(start=today + timedelta(days=1), periods=7)
    fig, ax = plt.subplots()
    ax.plot(next_seven_days, forecast, label='Forecasted Refills', marker='o')
    ax.set_xlabel('Date')
    ax.set_ylabel('Refills')
    ax.set_title('7-Day Refill Predictions')
    ax.legend()
    st.pyplot(fig)

def show_predictions():
    st.subheader("7-Day Refill Predictions")

    # Dropdown for initial bottle amount
    initial_bottles = st.selectbox("Select Initial Bottle Amount", options=df['Initially Purchased Bottle Amount'].unique())
    
    # Dropdown for customer location
    customer_location = st.selectbox("Select Customer Location", options=df['Customer Location'].unique())

    # Filter data based on selections
    filtered_data = df[(df['Initially Purchased Bottle Amount'] == initial_bottles) & (df['Customer Location'] == customer_location)]

    # Prepare historical data for ARIMA model
    historical_data = filtered_data.set_index('Date')['Refill Count']

    if not historical_data.empty:
        # Get forecast
        forecast = predict_refills(historical_data)
    else:
        forecast = [0] * 7  # Default to zero if no historical data is available
    
    st.write("Forecasted Refills:")
    st.write(forecast)

    # Convert forecast to DataFrame for better visualization
    forecast_df = pd.DataFrame({
        'Date': pd.date_range(start=today + timedelta(days=1), periods=7),
        'Predicted Refills': forecast
    })
    st.write(forecast_df)

    # Plotting the forecast
    fig, ax = plt.subplots()
    ax.plot(forecast_df['Date'], forecast_df['Predicted Refills'], label='Forecasted Refills', marker='o')
    ax.set_xlabel('Date')
    ax.set_ylabel('Refills')
    ax.set_title('7-Day Refill Predictions')
    ax.legend()
    st.pyplot(fig)

def show_historical_data():
    st.subheader("Historical Data")
    st.write(df)

    st.line_chart(df.set_index("Date")["Refill Count"])

def show_settings():
    st.subheader("Settings")
    st.write("User Settings")
    st.text_input("Username")
    st.text_input("Email")
    st.text_input("Phone")
    st.write("System Settings")
    st.number_input("Prediction Model Parameter 1", min_value=0.0, max_value=10.0, step=0.1)
    st.number_input("Prediction Model Parameter 2", min_value=0.0, max_value=10.0, step=0.1)
    st.checkbox("Enable Email Alerts")
    st.checkbox("Enable SMS Alerts")

def show_profile():
    st.subheader("Profile")
    st.write("User Profile Details")
    st.text("Username: admin")
    st.text("Email: admin@example.com")
    st.text("Phone: 123-456-7890")
    st.write("Recent Activities")
    st.text("Logged in at 10:00 AM")
    st.text("Updated settings at 11:00 AM")

# Main part of the app
def main():
    # Initialize session state for logged_in if it doesn't exist
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Check login status and show dashboard or login page accordingly
    if st.session_state["logged_in"]:
        dashboard()
    else:
        login()

# Call the main function
main()
