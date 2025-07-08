import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import base64
import os

# Streamlit App Title
st.title("📡 WiFi Access Points Map")

# File uploader
uploaded_file = st.file_uploader("Upload a Wigle WiFi CSV file", type=["csv"])
if uploaded_file is None:
    st.info("📁 Please upload a Wigle WiFi CSV file to continue.")
    st.stop()

# Read the CSV and clean it up
df = pd.read_csv(uploaded_file, skiprows=1)
df.columns = [col.strip().lower() for col in df.columns]

# 🧪 Check for required columns
required_cols = ['type', 'currentlatitude', 'currentlongitude']
if not all(col in df.columns for col in required_cols):
    st.error(f"Missing one or more required columns: {required_cols}")
    st.stop()

# Filter for Type == 'WIFI'
wifi_df = df[df['type'].str.upper() == 'WIFI']

# Drop rows with missing coordinates (prevents possible errors below)
wifi_df = wifi_df.dropna(subset=['currentlatitude', 'currentlongitude'])

# Show number of points
st.write(f"🛰️ Displaying {len(wifi_df)} WiFi Access Points")


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


# Create Folium Map
midpoint = [
    wifi_df['currentlatitude'].mean(),
    wifi_df['currentlongitude'].mean()
]
m = folium.Map(location=midpoint, zoom_start=12)
marker_cluster = MarkerCluster().add_to(m)

# Add markers
for _, row in wifi_df.iterrows():
    color = strength_to_color(row.get('rssi', 'N/A'))
    folium.Marker(
        location=[row['currentlatitude'], row['currentlongitude']],
        popup=(
            f"SSID: {row.get('ssid', 'N/A')}<br>"
            f"MAC: {row.get('mac', 'N/A')}<br>"
            f"Signal: {row.get('rssi', 'N/A')} dBm"
        ),
        icon=folium.Icon(color=color, icon="wifi", prefix="fa")
    ).add_to(marker_cluster)

# Display map in Streamlit
st_folium(m, width=700, height=500)


# 💾 Export to HTML
html_file = "wifi_map_export.html"
m.save(html_file)
with open(html_file, "rb") as f:
    b64 = base64.b64encode(f.read()).decode()
    href = (
        f'<a href="data:text/html;base64,{b64}" '
        f'download="{html_file}">📥 Download Map as HTML</a>'
    )
    st.markdown(href, unsafe_allow_html=True)
os.remove(html_file)
