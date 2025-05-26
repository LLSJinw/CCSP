import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Configuration and Data Initialization ---
DATA_FILE = "ccsp_study_log.csv"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S" # Used for timestamping entries

# Official (ISC)² CCSP Domains and Sub-objectives (Effective August 1, 2024)
# Based on (ISC)² CCSP Certification Exam Outline [1, 2, 3]
CCSP_DOMAINS = {
    "Domain 1: Cloud Concepts, Architecture, and Design (17%)":,
    "Domain 2: Cloud Data Security (20%)":
        "2.7 Plan and implement data retention, deletion, and archiving policies",
        "2.8 Design and implement auditability, traceability, and accountability of data events"
    ],
    "Domain 3: Cloud Platform & Infrastructure Security (17%)":,
    "Domain 4: Cloud Application Security (17%)":,
    "Domain 5: Cloud Security Operations (16%)":,
    "Domain 6: Legal, Risk, and Compliance (13%)": [
        "6.1 Articulate legal requirements and unique risks within the cloud environment",
        "6.2 Understand privacy issues",
        "6.3 Understand audit process, methodologies, and required adaptations for a cloud environment",
        "6.4 Understand implications of cloud to enterprise risk management",
        "6.5 Understand outsourcing and cloud contract design",
        "6.6 Execute vendor management"
    ]
}

# Suggested resources (can be expanded by the user)
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
    try:
        return pd.read_csv(DATA_FILE)
    except pd.errors.EmptyDataError:
         return pd.DataFrame(columns=)


def save_data(df):
    """Saves the DataFrame to the CSV file."""
    df.to_csv(DATA_FILE, index=False)

def add_study_entry(entry_date, domain, sub_objective, resources_used, time_spent, notes, confidence, status):
    """Adds a new entry to the study log."""
    df = load_data()
    timestamp = datetime.now().strftime(DATE_FORMAT)
    new_entry_data = {
        "Timestamp": [timestamp],
        "Date": [entry_date.strftime("%Y-%m-%d")],
        "Domain": [domain],
        "Sub-Objective": [sub_objective],
        "Resources Used": [", ".join(resources_used)], # Store as comma-separated string
        "Time Spent (Minutes)": [time_spent],
        "Notes": [notes],
        "Confidence (1-5)": [confidence],
        "Status": [status]
    }
    new_entry_df = pd.DataFrame(new_entry_data)
    df = pd.concat([df, new_entry_df], ignore_index=True)
    save_data(df)

# --- Streamlit App UI ---
st.set_page_config(page_title="CCSP Study Tracker", layout="wide")
st.title("🚀 Personalized CCSP Certification Study Tracker 🚀")
st.markdown("""
This app helps you track your daily study progress for the (ISC)² CCSP certification.
Ensure your daily study sessions align with your **1-1.5 hour (max 90 minutes)** goal.
""")

# Initialize data file
initialize_data_file()

# --- Sidebar for Navigation ---
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to",)

# --- Page 1: Add Study Entry ---
if page == "Add Study Entry":
    st.header("📝 Add New Study Entry")
    with st.form("study_entry_form", clear_on_submit=True):
        entry_date = st.date_input("Date of Study", value=datetime.today())

        selected_domain_key = st.selectbox("Domain Studied", options=list(CCSP_DOMAINS.keys()))

        # Get sub-objectives for the selected domain
        # Add a blank option or a prompt to select
        sub_objectives_for_domain = + CCSP_DOMAINS.get(selected_domain_key,)
        selected_sub_objective = st.selectbox("Sub-Objective Focused On", options=sub_objectives_for_domain)

        resources = st.multiselect("Resources Used", options=SUGGESTED_RESOURCES, default= if SUGGESTED_RESOURCES else None])
        other_resource = st.text_input("Other resource not listed? (Type and press Enter)")
        if other_resource and other_resource not in resources: # Add if typed and not already selected
            resources.append(other_resource)


        # Time spent: Max 90 minutes (1.5 hours)
        time_spent_minutes = st.number_input("Time Spent (Minutes)", min_value=1, max_value=90, value=60, step=5,
                                             help="Log your study time in minutes. Max 90 minutes per entry to align with daily goal.")

        notes = st.text_area("Key Takeaways / Notes / Areas of Confusion")
        confidence = st.slider("Confidence Level (1=Low, 5=High)", min_value=1, max_value=5, value=3)
        status_options =
        current_status = st.selectbox("Status of this Sub-Objective/Topic", options=status_options, index=1)

        submitted = st.form_submit_button("Add Entry to Log")

        if submitted:
            if selected_domain_key == "--Select a Domain--" or not selected_domain_key:
                 st.error("Please select a valid Domain.")
            elif selected_sub_objective == "--Select a Sub-Objective--" or not selected_sub_objective :
                st.error("Please select a valid Sub-Objective.")
            elif not resources:
                st.warning("No resources selected. Please select or add the resources used.")
            else:
                add_study_entry(entry_date, selected_domain_key, selected_sub_objective,
                                resources, time_spent_minutes, notes, confidence, current_status)
                st.success(f"Study entry for '{selected_sub_objective}' added successfully!")

# --- Page 2: View Progress Log ---
elif page == "View Progress Log":
    st.header("📊 Study Progress Log")
    df_log = load_data()

    if df_log.empty:
        st.info("No study entries yet. Add some from the 'Add Study Entry' page to see your progress!")
    else:
        st.dataframe(df_log.sort_values(by="Date", ascending=False), use_container_width=True)

        st.subheader("📈 Summary Statistics")
        total_time_minutes = df_log.sum()
        total_time_hours = total_time_minutes / 60
        st.metric("Total Study Time", f"{total_time_hours:.2f} hours ({total_time_minutes} minutes)")

        if not df_log.empty and "Confidence (1-5)" in df_log.columns and df_log["Confidence (1-5)"].notna().any():
            # Filter out entries where confidence might not have been recorded or is NaN
            valid_confidence_series = df_log["Confidence (1-5)"].dropna()
            if not valid_confidence_series.empty:
                avg_confidence = valid_confidence_series.mean()
                st.metric("Average Confidence (where recorded)", f"{avg_confidence:.2f} / 5")
            else:
                st.metric("Average Confidence (where recorded)", "N/A")
        else:
            st.metric("Average Confidence (where recorded)", "N/A")


        st.subheader("🕒 Time Spent per Domain")
        if not df_log.empty and "Domain" in df_log.columns and "Time Spent (Minutes)" in df_log.columns:
            domain_time = df_log.groupby("Domain").sum().sort_values(ascending=False)
            if not domain_time.empty:
                st.bar_chart(domain_time)
            else:
                st.info("No time logged per domain yet.")
        else:
            st.info("Log entries with Domain and Time Spent to see this chart.")

        st.subheader("🚦 Progress by Status (Latest Entry per Sub-Objective)")
        if not df_log.empty and "Sub-Objective" in df_log.columns and "Status" in df_log.columns and "Timestamp" in df_log.columns:
            # For status, we consider the latest entry for each unique sub-objective
            latest_status_df = df_log.sort_values('Timestamp').drop_duplicates(subset=, keep='last')
            if not latest_status_df.empty:
                status_counts = latest_status_df.value_counts()
                if not status_counts.empty:
                    st.bar_chart(status_counts)
                else:
                    st.info("No status logged yet for sub-objectives.")
            else:
                st.info("No sub-objectives with status logged yet.")
        else:
            st.info("Log entries with Sub-Objective, Status, and Timestamp to see this chart.")


# --- Page 3: Study Plan Overview ---
elif page == "Study Plan Overview":
    st.header("🗺️ CCSP Exam Outline & Study Plan")
    st.markdown("This section provides an overview of the CCSP domains and their sub-objectives to guide your study. [1, 2, 3]")
    st.markdown("*(Refer to the official (ISC)² CCSP Exam Outline for the most current and detailed information.)*")

    df_log = load_data()

    for domain_key, objectives_list in CCSP_DOMAINS.items():
        with st.expander(f"{domain_key}"):
            for obj_index, objective_name in enumerate(objectives_list):
                # Find the latest status for this objective
                latest_entry_for_objective = None
                if not df_log.empty:
                    filtered_df = df_log == domain_key) & (df_log == objective_name)]
                    if not filtered_df.empty:
                        latest_entry_for_objective = filtered_df.sort_values(by="Timestamp", ascending=False).iloc

                status_emoji = "⚪" # Default: Not Started (or no entry)
                if latest_entry_for_objective is not None:
                    status = latest_entry_for_objective
                    if status == "Completed":
                        status_emoji = "✅"
                    elif status == "In Progress":
                        status_emoji = "⏳"
                    elif status == "Needs Review":
                        status_emoji = "⚠️"

                st.markdown(f"{status_emoji} **{objective_name}**")


st.sidebar.info(
    "This app is a tool to help you structure and track your CCSP studies. "
    "Remember to consult official (ISC)² materials for the most accurate exam information."
)
st.sidebar.markdown("---")
st.sidebar.markdown("Created to help with your CCSP journey!")

# --- Footer ---
st.markdown("---")
st.markdown("CCSP Study Tracker | Good luck with your certification! 🍀")
