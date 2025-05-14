import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# ------------------ FIREBASE SETUP ------------------
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["firebase"])
    firebase_admin.initialize_app(cred)
db = firestore.client()

# ------------------ STREAMLIT CONFIG ------------------
st.set_page_config(page_title="Security Dashboard", layout="wide")
st.title("🛡️ Security Incident Dashboard – Northern Nigeria")

# ------------------ FETCH INCIDENTS ------------------
def fetch_data():
    docs = db.collection("incidents").stream()
    data = []
    for doc in docs:
        entry = doc.to_dict()
        entry["id"] = doc.id
        data.append(entry)
    return pd.DataFrame(data)

df = fetch_data()

if df.empty:
    st.warning("No incidents reported yet.")
    st.stop()

# ------------------ MAP VIEW ------------------
st.subheader("📍 Incident Map")
m = folium.Map(location=[11.5, 8.5], zoom_start=6)
marker_cluster = MarkerCluster().add_to(m)

for _, row in df.iterrows():
    popup_text = f"""
    <b>Location:</b> {row['location_address']}<br>
    <b>Number of Terrorists:</b> {row['num_terrorists']}<br>
    <b>Weapons:</b> {row['arms_type']}<br>
    <b>Mobility:</b> {row['mobility']}<br>
    <b>Other Info:</b> {row.get('other_info', 'N/A')}<br>
    <b>Time:</b> {row['timestamp']}
    """
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(marker_cluster)

st_folium(m, width=1000, height=500)

# ------------------ TABLE VIEW ------------------
st.subheader("📋 Incident Table")
df["timestamp"] = pd.to_datetime(df["timestamp"])
st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)
