import streamlit as st
import datetime
import pandas as pd
import random

# Initialize session state
if 'study_log' not in st.session_state:
    st.session_state.study_log = []
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'last_entry_date' not in st.session_state:
    st.session_state.last_entry_date = None

# Daily study tips/suggestions rotation
suggestions = [
    "📘 Pete Zerger YouTube: Domain overview video (15–25 min)",
    "📗 Official Guide: Read 1 subchapter (~30 min)",
    "🧠 LearnZapp: Do 20 practice questions (~20 min)",
    "📝 Write 3 key takeaways in your notes or flashcards (~15 min)",
    "🎯 Quizlet Flashcards: Review top 20 terms (~15 min)",
    "📖 NIST 800-145 summary (skim ~10 min)",
    "🎥 Mike Chapple LinkedIn Learning: 1 topic segment (~25–30 min)"
]

# Layout
st.title("📘 CCSP Daily Study Tracker")
st.markdown("Track your CCSP exam prep with a daily mission (max 1.5 hrs/day). Complete all 3 inputs to build your study streak.")

# Suggestion of the day
st.subheader("🎯 Today's Study Suggestion")
st.info(random.choice(suggestions))

# Input Section
st.subheader("📝 Log Today’s Study Progress")
today = datetime.date.today()
study_date = st.date_input("Date", value=today, max_value=today)
study_duration = st.slider("Study duration (hours)", 0.5, 1.5, 1.0, 0.25)
study_domain = st.selectbox("Domain Studied", [
    "",
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

# Semi-strict enforcement
if st.button("Add Entry"):
    if study_domain.strip() == "" or study_notes.strip() == "":
        st.warning("⛔ Please fill in all 3 fields: Duration, Domain, and Notes.")
    else:
        st.session_state.study_log.append({
            "Date": study_date,
            "Duration": study_duration,
            "Domain": study_domain,
            "Notes": study_notes
        })
        # Update streak
        if st.session_state.last_entry_date == today - datetime.timedelta(days=1):
            st.session_state.streak += 1
        elif st.session_state.last_entry_date != today:
            st.session_state.streak = 1
        st.session_state.last_entry_date = today

        st.success("✅ Study log entry added! Keep the streak going!")

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

    st.success(f"🔥 Current Streak: {st.session_state.streak} day(s) in a row!")
else:
    st.info("No study logs yet. Complete your first 3 inputs above to start your streak.")

# Optional: Export Log
with st.expander("📁 Export Log"):
    if st.button("Download Log as CSV"):
        csv = pd.DataFrame(st.session_state.study_log).to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="ccsp_study_log.csv",
            mime="text/csv"
        )
