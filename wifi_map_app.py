import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# Streamlit App Title
st.title("📡 WiFi Access Points Map")

# File uploader
uploaded_file = st.file_uploader("Upload a Wigle WiFi CSV file", type=["csv"])
if uploaded_file is not None:
    # Read the CSV
    df = pd.read_csv(uploaded_file, skiprows=1)

    # Filter for Type == 'WIFI'
    wifi_df = df[df['Type'].str.upper() == 'WIFI']

    # Drop rows with missing coordinates (prevents possible errors below)
    wifi_df = wifi_df.dropna(subset=['CurrentLatitude', 'CurrentLongitude'])

    # Show number of points
    st.write(f"🛰️ Displaying {len(wifi_df)} WiFi Access Points")

    # Create Folium Map
    midpoint = [wifi_df['CurrentLatitude'].mean(), wifi_df['CurrentLongitude'].mean()]
    m = folium.Map(location=midpoint, zoom_start=12)
    marker_cluster = MarkerCluster().add_to(m)

    # Function to convert signal strength to color
    def strength_to_color(dbm_val):
        try:
            dbm = float(dbm_val)
            if dbm > -50:
                return "green"
            elif -70 <= dbm < -50:
                return "orange"        # “yellowish” in Leaflet/Folium
            else:
                return "red"
        except (TypeError, ValueError):
            return "gray"

    # Add markers
    for _, row in wifi_df.iterrows():
        color = strength_to_color(row.get('RSSI', 'N/A'))
        folium.Marker(
            location=[row['CurrentLatitude'], row['CurrentLongitude']],
            popup=(
                f"SSID: {row.get('SSID', 'N/A')}<br>"
                f"MAC: {row.get('MAC', 'N/A')}<br>"
                f"Signal: {row.get('RSSI', 'N/A')} dBm"
            ),
            icon=folium.Icon(color=color, icon="wifi", prefix="fa")
        ).add_to(marker_cluster)

    # Display map in Streamlit
    folium_static(m)
