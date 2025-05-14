import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from streamlit_folium import st_folium
import folium
from datetime import datetime

# ------------------ FIREBASE CONNECTION ------------------
if not firebase_admin._apps:
    # Firebase credentials from Streamlit secrets
    firebase_credentials = st.secrets["firebase"]

    # Create a dictionary with parsed credentials
    cred_dict = {
        "type": firebase_credentials["type"],
        "project_id": firebase_credentials["project_id"],
        "private_key_id": firebase_credentials["private_key_id"],
        "private_key": firebase_credentials["private_key"],
        "client_email": firebase_credentials["client_email"],
        "client_id": firebase_credentials["client_id"],
        "auth_uri": firebase_credentials["auth_uri"],
        "token_uri": firebase_credentials["token_uri"],
        "auth_provider_x509_cert_url": firebase_credentials["auth_provider_x509_cert_url"],
        "client_x509_cert_url": firebase_credentials["client_x509_cert_url"],
        "universe_domain": firebase_credentials["universe_domain"]
    }

    # Initialize Firebase Admin SDK with the credentials dictionary
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

# Firestore client setup
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
            # Create the report data
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

            # Save the report to Firestore
            db.collection("incidents").add(report)

            st.success("✅ Report submitted successfully. Thank you for helping keep Nigeria safe.")
