import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="🚌 Bus Booking System", layout="centered")

st.title("🚌 Bus Booking System")
st.caption("A simple Streamlit interface for your FastAPI backend")

# --- Sidebar Navigation ---
menu = st.sidebar.radio("Navigation", ["View Buses", "Book Ticket", "View Bookings", "Cancel Booking"])

# --- View Buses ---
if menu == "View Buses":
    st.header("🚌 Available Buses")

    try:
        response = requests.get(f"{API_URL}/buses")
        if response.status_code == 200:
            buses = response.json()
            if buses:
                for bus in buses:
                    st.markdown(f"""
                        **Bus ID:** {bus['bus_id']}  
                        **Route:** {bus['route']}  
                        **Time:** {bus['time']}  
                        **Fare:** Rs {bus['fare']}  
                        **Seats Available:** {bus['seats_available']}
                        ---
                    """)
            else:
                st.info("No buses available.")
        else:
            st.error("Failed to fetch buses.")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the FastAPI server. Make sure it’s running.")

# --- Book Ticket ---
elif menu == "Book Ticket":
    st.header("🎟️ Book a Ticket")

    name = st.text_input("Your Name")
    bus_id = st.number_input("Bus ID", min_value=1, step=1)
    seats = st.number_input("Number of Seats", min_value=1, max_value=30, step=1)

    if st.button("Book Now"):
        booking_data = {
            "name": name,
            "bus_id": bus_id,
            "seats": seats
        }
        try:
            response = requests.post(f"{API_URL}/bookings", json=booking_data)
            if response.status_code == 200:
                booking = response.json()
                st.success(f"✅ Booking Successful! Booking ID: {booking['booking_id']}")
                st.json(booking)
            else:
                st.error(f"❌ Failed to book: {response.json().get('detail', 'Unknown error')}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI server. Start it before booking.")

# --- View All Bookings ---
elif menu == "View Bookings":
    st.header("📋 Current Bookings")

    try:
        response = requests.get(f"{API_URL}/bookings")
        if response.status_code == 200:
            bookings = response.json()
            if bookings:
                for booking in bookings:
                    st.markdown(f"""
                        **Booking ID:** {booking['booking_id']}  
                        **Name:** {booking['name']}  
                        **Bus ID:** {booking['bus_id']}  
                        **Route:** {booking['route']}  
                        **Time:** {booking['time']}  
                        **Seats:** {booking['seats']}  
                        **Total Fare:** Rs {booking['total_fare']}  
                        **Booking Time:** {booking['booking_time']}
                        ---
                    """)
            else:
                st.info("No bookings found.")
        else:
            st.error("Failed to retrieve bookings.")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to FastAPI server.")

# --- Cancel Booking ---
elif menu == "Cancel Booking":
    st.header("❌ Cancel a Booking")

    name = st.text_input("Enter your Name to cancel booking")

    if st.button("Cancel Booking"):
        cancel_data = {"name": name}
        try:
            response = requests.delete(f"{API_URL}/bookings", json=cancel_data)
            if response.status_code == 200:
                st.success(response.json().get("message"))
            else:
                st.error(f"❌ {response.json().get('detail', 'Booking not found')}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI server.")
