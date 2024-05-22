import streamlit as st
import pandas as pd
import numpy as np

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


# Dashboard Page
def dashboard():
    st.title("Water Supply Co. - Dashboard")
    st.sidebar.title("Navigation")
    pages = ["Overview", "Predictions", "Historical Data", "Settings", "Profile"]
    page = st.sidebar.radio("Go to", pages)

    if page == "Overview":
        show_overview()
    elif page == "Predictions":
        show_predictions()
    elif page == "Historical Data":
        show_historical_data()
    elif page == "Settings":
        show_settings()
    elif page == "Profile":
        show_profile()

def show_overview():
    st.subheader("Overview")
    st.write("Key Metrics:")
    col1, col2, col3 = st.columns(3)
    col1.metric("Today's Refills", "150")
    col2.metric("7-Day Forecast", "1100")
    col3.metric("Avg Daily Refills", "158")

def show_predictions():
    st.subheader("7-Day Refill Predictions")
    # Dummy data for demonstration
    data = {
        "Date": pd.date_range(start="2024-05-01", periods=7),
        "Predicted Refills": [130, 140, 145, 150, 160, 155, 150],
        "Temperature": [25, 27, 28, 29, 30, 26, 25],
        "Precipitation": [0, 2, 0, 1, 0, 5, 0],
        "Humidity": [60, 55, 50, 52, 48, 65, 60],
        "Special Event": ["No", "No", "No", "No", "Yes", "No", "No"],
        "Marketing Campaign": ["Yes", "No", "Yes", "No", "Yes", "No", "Yes"]
    }
    df = pd.DataFrame(data)
    st.write(df)

    st.line_chart(df.set_index("Date")["Predicted Refills"])
    st.bar_chart(df.set_index("Date")["Predicted Refills"])

def show_historical_data():
    st.subheader("Historical Data")
    # Dummy data for demonstration
    data = {
        "Date": pd.date_range(start="2024-04-01", periods=30),
        "Actual Refills": np.random.randint(100, 200, size=30),
        "Temperature": np.random.randint(20, 35, size=30),
        "Precipitation": np.random.randint(0, 10, size=30),
        "Humidity": np.random.randint(40, 70, size=30),
        "Special Event": np.random.choice(["No", "Yes"], size=30),
        "Marketing Campaign": np.random.choice(["No", "Yes"], size=30)
    }
    df = pd.DataFrame(data)
    st.write(df)

    st.line_chart(df.set_index("Date")["Actual Refills"])
    st.area_chart(df.set_index("Date")[["Temperature", "Precipitation", "Humidity"]])

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
