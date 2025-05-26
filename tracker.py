import streamlit as st
import datetime
import pandas as pd
import os

# Initialize session state
if 'study_log' not in st.session_state:
    st.session_state.study_log = []

st.title("📘 CCSP Daily Study Tracker")
st.markdown("Track your CCSP exam preparation progress with 1–1.5 hours/day study goals.")

# Input Section
st.subheader("📝 Log Today's Study Progress")
today = datetime.date.today()
study_date = st.date_input("Date", value=today, max_value=today)
study_duration = st.slider("Study duration (hours)", 0.5, 1.5, 1.0, 0.25)
study_domain = st.selectbox("Domain Studied", [
    "Domain 1 – Cloud Concepts, Architecture, and Design",
    "Domain 2 – Cloud Data Security",
    "Domain 3 – Cloud Platform and Infrastructure Security",
    "Domain 4 – Cloud Application Security",
    "Domain 5 – Cloud Security Operations",
    "Domain 6 – Legal, Risk, and Compliance",
    "Review / Practice Exam",
    "Other"
])
study_notes = st.text_area("Notes (e.g., chapters read, practice tests done, key points)")

if st.button("Add Entry"):
    st.session_state.study_log.append({
        "Date": study_date,
        "Duration": study_duration,
        "Domain": study_domain,
        "Notes": study_notes
    })
    st.success("Study log entry added!")

# Display Log
if st.session_state.study_log:
    st.subheader("📊 Study Progress Log")
    log_df = pd.DataFrame(st.session_state.study_log)
    log_df = log_df.sort_values(by="Date", ascending=False)
    st.dataframe(log_df, use_container_width=True)

    total_hours = log_df['Duration'].sum()
    st.markdown(f"**Total Hours Studied:** {total_hours:.2f} hours")

    domain_counts = log_df['Domain'].value_counts()
    st.bar_chart(domain_counts)
else:
    st.info("No study logs yet. Start by logging today's progress above.")

# Optional: Export/Import functionality for advanced users
with st.expander("📁 Export/Import Log"):
    if st.button("Download Log as CSV"):
        csv = pd.DataFrame(st.session_state.study_log).to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="ccsp_study_log.csv",
            mime="text/csv"
        )
