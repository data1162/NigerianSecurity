import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# ------------------ FIREBASE CONNECTION ------------------
if not firebase_admin._apps:
    # Load Firebase credentials from Streamlit secrets
    firebase_credentials = st.secrets["firebase"]  # Accessing the credentials as a dictionary
    cred = credentials.Certificate(firebase_credentials)  # Pass directly if it's a dictionary
    firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()

# ------------------ Streamlit UI ------------------
st.title("Nigerian Security Dashboard")

# Fetch and display security incidents from Firestore
incident_ref = db.collection('incidents')
incident_docs = incident_ref.stream()

st.write("### Security Incidents")
for doc in incident_docs:
    st.write(f"**Incident ID**: {doc.id}")
    st.write(f"**Description**: {doc.to_dict().get('description')}")
    st.write(f"**Location**: {doc.to_dict().get('location')}")
    st.write(f"**Date**: {doc.to_dict().get('date')}")
    st.write("-" * 30)

# Form to report a new incident
st.write("### Report a New Incident")
with st.form(key='incident_form'):
    description = st.text_area("Description")
    location = st.text_input("Location")
    date = st.date_input("Date of Incident")
    submit_button = st.form_submit_button("Submit Incident")

    if submit_button:
        if description and location and date:
            incident_ref.add({
                'description': description,
                'location': location,
                'date': date.strftime("%Y-%m-%d")
            })
            st.success("Incident reported successfully!")
        else:
            st.error("Please fill in all fields.")
