import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.set_page_config(page_title="Smart Study Plan Generator", layout="centered")

st.title("Smart Study Plan Generator — Prototype")
st.write("Enter subjects, available hours per day, priorities and we'll generate a personalised weekly study plan. This is a working prototype converted from your notebook.")

with st.form("input_form"):
    name = st.text_input("Student name", value="Student")
    days = st.number_input("Days to plan (1-30)", min_value=1, max_value=30, value=7)
    hours_per_day = st.number_input("Available study hours per day", min_value=1.0, max_value=24.0, value=5.0, step=0.5)
    n_subj = st.number_input("Number of subjects", min_value=1, max_value=10, value=4)
    subjects = []
    st.write("Enter subject details (name, priority 1-5, difficulty 1-5, required hours total)")
    subj_cols = st.columns(4)
    # collect subject inputs dynamically
    for i in range(int(n_subj)):
        with st.expander(f"Subject {i+1}", expanded=(i<3)):
            s_name = st.text_input(f"Subject name {i}", value=f"Subject_{i+1}", key=f"name_{i}")
            priority = st.slider(f"Priority (1 low - 5 high) {i}", min_value=1, max_value=5, value=3, key=f"pri_{i}")
            difficulty = st.slider(f"Difficulty (1 easy - 5 hard) {i}", min_value=1, max_value=5, value=3, key=f"diff_{i}")
            req_hours = st.number_input(f"Total hours needed for {s_name}", min_value=0.0, max_value=500.0, value=10.0, step=0.5, key=f"req_{i}")
            subjects.append({"name": s_name or f"Subject_{i+1}", "priority": priority, "difficulty": difficulty, "req_hours": req_hours})

    submit = st.form_submit_button("Generate Study Plan")

def allocate_hours(subjects, total_hours):
    # Score each subject by priority and difficulty (higher priority and higher difficulty -> more hours)
    # score = priority * (1 + difficulty/5)
    scores = [(s["priority"] * (1 + s["difficulty"]/5.0)) for s in subjects]
    ssum = sum(scores) if sum(scores)>0 else 1.0
    for i, s in enumerate(subjects):
        frac = scores[i]/ssum
        s["assigned_hours"] = round(frac * total_hours, 2)
    return subjects

def build_schedule(subjects, days, hours_per_day):
    total_hours = days * hours_per_day
    subjects = allocate_hours(subjects, total_hours)
    # create schedule dataframe with day and allocated subject chunks (1-hour blocks)
    blocks = []
    subj_iters = []
    for s in subjects:
        # split assigned_hours into integer 1-hour blocks and maybe a remainder
        hours = s["assigned_hours"]
        whole = int(math.floor(hours))
        rem = round(hours - whole, 2)
        blocks.extend([{"subject": s["name"]} for _ in range(whole)])
        if rem >= 0.25:
            # add one fractional block represented as '0.5h' etc.
            blocks.append({"subject": s["name"]})
    # distribute blocks across days sequentially
    schedule = []
    idx = 0
    total_blocks = len(blocks)
    max_blocks_per_day = int(hours_per_day)
    for d in range(days):
        day_blocks = []
        for h in range(max_blocks_per_day):
            if idx < total_blocks:
                day_blocks.append(blocks[idx]["subject"])
                idx += 1
            else:
                day_blocks.append("Rest/Revision")
        schedule.append({"day": d+1, "slots": day_blocks})
    # If leftover blocks remain, append to last days' extra slots (if hours_per_day had fraction)
    return subjects, schedule

if submit:
    subjects_clean = [s for s in subjects if s["name"]]
    if not subjects_clean:
        st.error("Please provide at least one subject.")
    else:
        assigned_subjects, schedule = build_schedule(subjects_clean, int(days), float(hours_per_day))
        st.subheader("Assigned hours per subject")
        df = pd.DataFrame(assigned_subjects)[["name","priority","difficulty","req_hours","assigned_hours"]]
        st.dataframe(df)
        # show a bar chart of assigned hours
        fig, ax = plt.subplots(figsize=(6,3))
        ax.bar(df["name"], df["assigned_hours"])
        ax.set_ylabel("Assigned hours")
        ax.set_xlabel("Subject")
        ax.set_title("Assigned study hours (total)")
        st.pyplot(fig)

        st.subheader("Daily Schedule (first week view)")
        for day in schedule:
            st.markdown(f"**Day {day['day']}**: " + " | ".join(day["slots"]))
        # export option
        csv_rows = []
        for day in schedule:
            for i, slot in enumerate(day["slots"], start=1):
                csv_rows.append({"day": day["day"], "slot": i, "subject": slot})
        export_df = pd.DataFrame(csv_rows)
        st.download_button("Download schedule CSV", export_df.to_csv(index=False), file_name="study_schedule.csv", mime="text/csv")

        st.success("Study plan generated! You can fine-tune priorities or days and regenerate.")

# Footer / credits
st.write("---")
st.write("Prototype created from the uploaded notebook. For advanced features (neural network prediction, explainability, scheduler optimization, calendar export), I can add them next.")
