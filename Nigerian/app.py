import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from streamlit_folium import st_folium
import folium
from datetime import datetime

# ------------------ FIREBASE CONNECTION ------------------
if not firebase_admin._apps:
    firebase_credentials = st.secrets["firebase"]  # Accessing the credentials from Streamlit secrets
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)
db = firestore.client()

# ------------------ STREAMLIT APP ------------------
st.set_page_config(page_title="Insecurity Incident Reporter", layout="centered")

st.title("🛡️ Report Insecurity Incident in Northern Nigeria")

with st.form("incident_form"):
    st.subheader("📍 Incident Details")

    # Map for picking location
    st.markdown("**Step 1:** Pinpoint the incident location on the map.")
    m = folium.Map(location=[11.5, 8.5], zoom_start=6)  # Northern Nigeria
    marker = folium.Marker(location=[11.5, 8.5], draggable=True)
    marker.add_to(m)
    map_data = st_folium(m, height=350, width=700)

    st.markdown("**Step 2:** Fill in incident information.")
    location_address = st.text_input("🗺️ Location Address")
    num_terrorists = st.number_input("👥 Number of Terrorists", min_value=1)
    arms_type = st.text_area("🔫 Type of Weapons Observed (e.g., AK-47s, RPGs)")
    mobility = st.selectbox("🚙 How are they moving?", ["Motorbikes", "Vehicles", "On foot"])
    other_info = st.text_area("📝 Other Relevant Info (optional)")

    submitted = st.form_submit_button("🚨 Submit Report")

    if submitted:
        if not location_address or not map_data["last_clicked"]:
            st.warning("Please provide an address and select a location on the map.")
        else:
            report = {
                "timestamp": datetime.utcnow(),
                "location_address": location_address,
                "latitude": map_data["last_clicked"]["lat"],
                "longitude": map_data["last_clicked"]["lng"],
                "num_terrorists": num_terrorists,
                "arms_type": arms_type,
                "mobility": mobility,
                "other_info": other_info
            }
            db.collection("incidents").add(report)
            st.success("✅ Report submitted successfully. Thank you for helping keep Nigeria safe.")
