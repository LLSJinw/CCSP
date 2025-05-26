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

# Define milestone tracker (static for now)
milestones = [
    "✅ Domain 1 Complete",
    "✅ Domain 2 Complete",
    "✅ Domain 3 Complete",
    "✅ Domain 4 Complete",
    "✅ Domain 5 Complete",
    "✅ Domain 6 Complete",
    "🧠 Practice Exam 1 Done",
    "🔁 Mid-Review Week",
    "🧠 Practice Exam 2 Done",
    "🎯 Final Review Week"
]

# Task checklist items
task_items = [
    ("Read Official Guide (1 section)", True),
    ("Complete 15–25 LearnZapp questions", True),
    ("Watch 1 topic video (Pete Zerger / Mike Chapple)", False),
    ("Review 15 Quizlet flashcards", False),
    ("Skim short section of NIST doc", False),
    ("Write 3 takeaways in Notion or journal", False)
]

st.title("📘 CCSP Daily Study Tracker")
st.markdown("Track your CCSP exam prep with daily 3-task missions (at least 1 core task ⭐). Build your streak and hit milestones.")

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

# Task checkboxes
st.markdown("**Select today's completed tasks (at least 3, including 1 ⭐ core):**")
completed_tasks = []
core_count = 0
for task, is_core in task_items:
    checked = st.checkbox(f"{'⭐' if is_core else '•'} {task}")
    if checked:
        completed_tasks.append(task)
        if is_core:
            core_count += 1

# Optional reflection
study_notes = st.text_area("Reflection or notes (optional)")

# Enforce rules
if st.button("Add Entry"):
    if len(completed_tasks) < 3:
        st.warning("⛔ Please complete at least 3 tasks.")
    elif core_count < 1:
        st.warning("⭐ You must complete at least 1 core task (marked with a ⭐).")
    elif study_domain.strip() == "":
        st.warning("⛔ Please select a domain.")
    else:
        st.session_state.study_log.append({
            "Date": study_date,
            "Duration": study_duration,
            "Domain": study_domain,
            "Tasks": ", ".join(completed_tasks),
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
    st.info("No study logs yet. Complete your first 3-task mission above to start your streak.")

# Milestone Checklist (Static for now)
st.subheader("📅 Milestone Tracker")
for milestone in milestones:
    st.markdown(f"- {milestone}")

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
