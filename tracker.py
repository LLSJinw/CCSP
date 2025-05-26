import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Configuration and Data Initialization ---
DATA_FILE = "study_log.csv"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Official (ISC)² CCSP Domains and Sub-objectives (Effective August 1, 2024)
# Based on information from sources like isc2.org/certifications/ccsp/ccsp-certification-exam-outline [1]
CCSP_DOMAINS = {
    "Domain 1: Cloud Concepts, Architecture, and Design (17%)":,
    "Domain 2: Cloud Data Security (20%)":,
    "Domain 3: Cloud Platform & Infrastructure Security (17%)":,
    "Domain 4: Cloud Application Security (17%)":,
    "Domain 5: Cloud Security Operations (16%)":,
    "Domain 6: Legal, Risk, and Compliance (13%)":
}

# Suggested resources (general, can be expanded)
SUGGESTED_RESOURCES =

# --- Helper Functions ---
def initialize_data_file():
    """Creates the CSV file with headers if it doesn't exist."""
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=)
        df.to_csv(DATA_FILE, index=False)

def load_data():
    """Loads study log data from the CSV file."""
    initialize_data_file()
    return pd.read_csv(DATA_FILE)

def save_data(df):
    """Saves the DataFrame to the CSV file."""
    df.to_csv(DATA_FILE, index=False)

def add_study_entry(date, domain, sub_objective, resources_used, time_spent, notes, confidence, status):
    """Adds a new entry to the study log."""
    df = load_data()
    timestamp = datetime.now().strftime(DATE_FORMAT)
    new_entry = pd.DataFrame()
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)

# --- Streamlit App UI ---
st.set_page_config(page_title="CCSP Study Tracker", layout="wide")
st.title(" personalized CCSP Certification Study Tracker")
st.markdown("""
This app helps you track your daily study progress for the (ISC)² CCSP certification.
Ensure your daily study sessions align with your 1-1.5 hour goal.
""")

# Initialize data file
initialize_data_file()

# --- Sidebar for Navigation ---
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to",)

# --- Page 1: Add Study Entry ---
if page == "Add Study Entry":
    st.header("Add New Study Entry")
    with st.form("study_entry_form", clear_on_submit=True):
        entry_date = st.date_input("Date of Study", value=datetime.today())
        
        selected_domain = st.selectbox("Domain Studied", options=list(CCSP_DOMAINS.keys()))
        
        sub_objectives_for_domain = [""] + CCSP_DOMAINS.get(selected_domain,)
        selected_sub_objective = st.selectbox("Sub-Objective Focused On", options=sub_objectives_for_domain)

        resources = st.multiselect("Resources Used", options=SUGGESTED_RESOURCES)
        other_resource = st.text_input("Other resource not listed?")
        if other_resource:
            resources.append(other_resource)

        # Time spent: Max 90 minutes (1.5 hours)
        time_spent_minutes = st.number_input("Time Spent (Minutes)", min_value=1, max_value=90, value=60, step=5)
        
        notes = st.text_area("Key Takeaways / Notes")
        confidence = st.slider("Confidence Level (1=Low, 5=High)", min_value=1, max_value=5, value=3)
        status_options =
        current_status = st.selectbox("Status of this Sub-Objective/Topic", options=status_options, index=1)

        submitted = st.form_submit_button("Add Entry")

        if submitted:
            if not selected_domain or not selected_sub_objective:
                st.error("Please select a Domain and Sub-Objective.")
            elif not resources:
                st.warning("No resources selected. Please select or add the resources used.")
            else:
                add_study_entry(entry_date, selected_domain, selected_sub_objective,
                                resources, time_spent_minutes, notes, confidence, current_status)
                st.success("Study entry added successfully!")

# --- Page 2: View Progress Log ---
elif page == "View Progress Log":
    st.header("Study Progress Log")
    df_log = load_data()

    if df_log.empty:
        st.info("No study entries yet. Add some to see your progress!")
    else:
        st.dataframe(df_log.sort_values(by="Date", ascending=False), use_container_width=True)

        st.subheader("Summary Statistics")
        total_time_hours = df_log.sum() / 60
        st.metric("Total Study Time", f"{total_time_hours:.2f} hours")

        if not df_log.empty:
            avg_confidence = df_log[df_log["Confidence (1-5)"] > 0]["Confidence (1-5)"].mean() # Avoid division by zero if no confidence recorded
            st.metric("Average Confidence (where recorded)", f"{avg_confidence:.2f} / 5" if pd.notna(avg_confidence) else "N/A")

        st.subheader("Time Spent per Domain")
        if not df_log.empty:
            domain_time = df_log.groupby("Domain").sum().sort_values(ascending=False)
            if not domain_time.empty:
                st.bar_chart(domain_time)
            else:
                st.info("No time logged per domain yet.")
        
        st.subheader("Progress by Status")
        if not df_log.empty:
            # For status, we consider the latest entry for each unique sub-objective
            latest_status_df = df_log.sort_values('Timestamp').drop_duplicates(, keep='last')
            status_counts = latest_status_df.value_counts()
            if not status_counts.empty:
                st.bar_chart(status_counts)
            else:
                st.info("No status logged yet.")


# --- Page 3: Study Plan Overview ---
elif page == "Study Plan Overview":
    st.header("CCSP Exam Outline & Study Plan")
    st.markdown("This section provides an overview of the CCSP domains and their sub-objectives to guide your study.")

    for domain, objectives in CCSP_DOMAINS.items():
        with st.expander(f"{domain}"):
            for obj_index, objective in enumerate(objectives):
                st.markdown(f"- **{objective}**")
                # You could add checkboxes here if you want to manually track overall completion
                # st.checkbox(f"Mark as studied: {objective}", key=f"{domain}_{obj_index}_studied")
    
    st.sidebar.info(
        "This app is a tool to help you structure and track your CCSP studies. "
        "Remember to consult official (ISC)² materials for the most accurate exam information."
    )

# --- Footer ---
st.markdown("---")
st.markdown("CCSP Study Tracker | Good luck with your certification!")
