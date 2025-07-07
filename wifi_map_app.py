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

    # Drop rows with missing coordinates
    wifi_df = wifi_df.dropna(subset=['CurrentLatitude', 'CurrentLongitude'])

    # Show number of points
    st.write(f"🛰️ Displaying {len(wifi_df)} WiFi Access Points")

    # Create Folium Map
    midpoint = [wifi_df['CurrentLatitude'].mean(), wifi_df['CurrentLongitude'].mean()]
    m = folium.Map(location=midpoint, zoom_start=12)
    marker_cluster = MarkerCluster().add_to(m)

    # Add markers
    for _, row in wifi_df.iterrows():
        folium.Marker(
            location=[row['CurrentLatitude'], row['CurrentLongitude']],
            popup=f"SSID: {row.get('SSID', 'N/A')}<br>RSSI: {row.get('RSSI', 'N/A')}<br>BSSID: {row.get('MAC', 'N/A')}",
            icon=folium.Icon(color="blue", icon="wifi", prefix="fa")
        ).add_to(marker_cluster)

    # Display map in Streamlit
    folium_static(m)
