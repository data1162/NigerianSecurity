import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# -------------------- Firebase Setup --------------------
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["firebase"])
    firebase_admin.initialize_app(cred)
db = firestore.client()

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="Insecurity Reporting App", layout="wide")
st.title("🚨 Report an Insecurity Incident")
st.markdown("Please provide accurate and timely information to help Nigerian security agencies respond effectively.")

with st.form("incident_form"):
    st.subheader("📍 Location of Incident")
    col1, col2 = st.columns(2)

    # Map to select coordinates
    with col1:
        m = folium.Map(location=[11.5, 8.5], zoom_start=6)
        map_data = st_folium(m, height=300, returned_objects=["last_clicked"])

    with col2:
        location_address = st.text_input("Location Address (Town, LGA, State)")

    st.subheader("⚠️ Incident Details")
    num_terrorists = st.number_input("Number of terrorists involved", min_value=1, step=1)
    arms = st.text_area("Type of arms (e.g., AK-47s, explosives)")
    transport_mode = st.selectbox("Mode of transport", ["Motorbikes", "Vehicles", "On Foot", "Unknown"])
    extra_info = st.text_area("Additional Information (e.g., direction they fled, dress code)")

    submitted = st.form_submit_button("📤 Submit Report")

# -------------------- Submit to Firebase --------------------
if submitted:
    if map_data and map_data["last_clicked"] and location_address:
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]

        report = {
            "timestamp": datetime.utcnow(),
            "latitude": lat,
            "longitude": lon,
            "location_address": location_address,
            "num_terrorists": num_terrorists,
            "arms": arms,
            "transport_mode": transport_mode,
            "extra_info": extra_info
        }

        db.collection("incident_reports").add(report)
        st.success("✅ Report submitted successfully!")
        st.balloons()
    else:
        st.warning("⚠️ Please click on the map and provide a location address.")
