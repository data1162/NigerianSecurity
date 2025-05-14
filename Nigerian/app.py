import json
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# ------------------ FIREBASE CONNECTION ------------------
if not firebase_admin._apps:
    # Load the firebase credentials from Streamlit secrets
    firebase_credentials = st.secrets["firebase"]
    
    # Convert the string to a dictionary if necessary
    firebase_credentials_dict = json.loads(firebase_credentials)
    
    # Initialize Firebase with the credentials
    cred = credentials.Certificate(firebase_credentials_dict)
    firebase_admin.initialize_app(cred)
    
    # Initialize Firestore
    db = firestore.client()

# ------------------ STREAMLIT UI ------------------
st.title("Nigerian Security Incidents Report")
st.write("Welcome to the app for reporting and monitoring insecurity incidents in Northern Nigeria.")

# Example of Firebase usage - Display all incidents from Firestore
st.header("Security Incidents")

# Query all incidents from Firestore (assuming incidents are stored in the 'incidents' collection)
incidents_ref = db.collection("incidents")
incidents = incidents_ref.stream()

# Display each incident
for incident in incidents:
    st.write(f"**{incident.id}**: {incident.to_dict()['description']}")

# Form for reporting new incidents
with st.form(key='incident_form'):
    st.subheader("Report a New Incident")
    description = st.text_area("Incident Description", "")
    location = st.text_input("Location", "")
    date = st.date_input("Date of Incident")
    
    submit_button = st.form_submit_button("Submit Incident")
    
    if submit_button:
        # Add the new incident to Firestore
        new_incident_ref = db.collection("incidents").add({
            "description": description,
            "location": location,
            "date": date,
            "status": "Reported"
        })
        st.success("Incident successfully reported!")

# ------------------ END ------------------
