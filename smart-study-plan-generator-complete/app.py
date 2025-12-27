import streamlit as st
import numpy as np
import pandas as pd
import os
from database import (
    save_study_history,
    get_user_history,
    delete_user_history,
    get_latest_study_plan   # 👈 ADD THIS
)

# ---------------- DB & AUTH ----------------
from auth import register_user, login_user
from database import save_study_history, get_user_history, delete_user_history

# ---------------- SESSION SETUP ----------------
if "user" not in st.session_state:
    st.session_state["user"] = None

# store last prediction
if "last_subject_hours" not in st.session_state:
    st.session_state["last_subject_hours"] = None

if "last_timetable" not in st.session_state:
    st.session_state["last_timetable"] = None

# ---------------- LOGIN / SIGNUP ----------------
def login_page():
    st.title("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state["user"] = user
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid email or password")

    st.markdown("---")
    st.subheader("🆕 Sign Up")

    name = st.text_input("Name")
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")

    if st.button("Create Account"):
        if register_user(name, new_email, new_password):
            st.success("Account created. Please login.")
        else:
            st.error("Email already exists")

if st.session_state["user"] is None:
    login_page()
    st.stop()

# ---------------- NN: TOTAL HOURS ----------------
def predict_total_hours(current_gpa, target_gpa):
    from tensorflow.keras.models import load_model

    model = load_model("model/total_hours_model.h5", compile=False)

    x = np.array([[current_gpa, target_gpa]])
    hours = model.predict(x)[0][0]

    return round(float(max(10, hours)), 1)

# ---------------- DISTRIBUTE BY DIFFICULTY ----------------
def distribute_hours(subjects, total_hours):
    total_weight = sum(s["difficulty"] for s in subjects)
    allocation = {}

    for s in subjects:
        allocation[s["name"]] = round(
            (s["difficulty"] / total_weight) * total_hours, 1
        )
    return allocation

# ---------------- TIMETABLE ----------------
def generate_time_slot_timetable(subject_hours, availability, time_slots):
    # Collect all available (day, slot) positions
    available_positions = []
    for day in availability:
        for slot in time_slots:
            if availability[day][slot]:
                available_positions.append((day, slot))

    # Create empty timetable
    timetable = {slot: {day: "" for day in availability} for slot in time_slots}

    subjects = list(subject_hours.keys())
    idx = 0

    # 🔹 PHASE 1: Guarantee at least ONE slot per subject
    for subject in subjects:
        if idx >= len(available_positions):
            break
        day, slot = available_positions[idx]
        timetable[slot][day] = subject
        subject_hours[subject] = max(0, subject_hours[subject] - 1)
        idx += 1

    # 🔹 PHASE 2: Fill remaining slots by difficulty
    remaining_blocks = []
    for subject, hrs in subject_hours.items():
        remaining_blocks.extend([subject] * int(round(hrs)))

    for subject in remaining_blocks:
        if idx >= len(available_positions):
            break
        day, slot = available_positions[idx]
        timetable[slot][day] = subject
        idx += 1

    return pd.DataFrame(timetable).T


# ---------------- SIDEBAR ----------------
st.sidebar.title("📘 Smart Study Plan Generator")
st.sidebar.write(f"👤 {st.session_state['user']['name']}")

if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    st.rerun()

page = st.sidebar.radio("Navigation", ["Home", "Input", "Predict", "History"])

# ---------------- HOME ----------------
# ---------------- HOME ----------------
if page == "Home":
    st.title("📚 Smart Study Plan Generator")
    st.write("Welcome,", st.session_state["user"]["name"])

    latest = get_latest_study_plan(
        st.session_state["user"]["user_id"]
    )

    if not latest:
        st.info("No study plan generated yet.")
    else:
        subject_hours, timetable_dict, date = latest

        st.markdown(f"### 🕒 Last Generated On: `{date}`")

        # 📘 Subject-wise hours
        st.subheader("📘 Last Subject-wise Hours")
        hours_df = pd.DataFrame(
            subject_hours.items(),
            columns=["Subject", "Hours / Week"]
        )
        st.table(hours_df)

        # 📅 Timetable
        st.subheader("📅 Last Weekly Timetable")
        timetable_df = pd.DataFrame(timetable_dict)
        st.dataframe(timetable_df, use_container_width=True)


# ---------------- INPUT ----------------
if page == "Input":
    st.title("✍️ Input Details")

    current_gpa = st.number_input("Current CGPA", 0.0, 10.0, 7.5)
    target_gpa = st.number_input("Target CGPA", 0.0, 10.0, 9.0)

    st.subheader("📘 Subjects & Difficulty")
    num_subjects = st.number_input("Number of subjects", 1, 10, 5)

    subjects = []
    for i in range(num_subjects):
        c1, c2 = st.columns([2, 1])
        name = c1.text_input(f"Subject {i+1}", key=f"sub_{i}")
        diff = c2.slider("Difficulty", 1, 5, 3, key=f"diff_{i}")
        if name.strip():
            subjects.append({"name": name, "difficulty": diff})

    st.subheader("🕒 Available Time Slots")

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    time_slots = ["8–10 AM","10–12 AM","1–3 AM","3–5 PM"]

    availability = {}
    for d in days:
        st.markdown(f"**{d}**")
        availability[d] = {}
        cols = st.columns(len(time_slots))
        for i, slot in enumerate(time_slots):
            availability[d][slot] = cols[i].checkbox(slot, key=f"{d}_{slot}")

    st.session_state["inputs"] = {
        "current_gpa": current_gpa,
        "target_gpa": target_gpa,
        "subjects": subjects,
        "availability": availability,
        "time_slots": time_slots
    }

    st.success("Inputs saved. Go to Predict.")

# ---------------- PREDICT ----------------
if page == "Predict":
    st.title("🔮 Prediction")

    if st.button("Generate Study Plan"):
        data = st.session_state.get("inputs")
        if not data or not data["subjects"]:
            st.error("Please enter inputs first.")
            st.stop()

        total_hours = predict_total_hours(
            data["current_gpa"],
            data["target_gpa"]
        )

        subject_hours = distribute_hours(
            data["subjects"],
            total_hours
        )

        timetable_df = generate_time_slot_timetable(
            subject_hours,
            data["availability"],
            data["time_slots"]
        )

        # ✅ SAVE FOR HOME PAGE
        st.session_state["last_subject_hours"] = subject_hours
        st.session_state["last_timetable"] = timetable_df

        st.subheader("📘 Subject-wise Hours")
        st.table(pd.DataFrame(subject_hours.items(),
                              columns=["Subject", "Hours / Week"]))

        st.subheader("📅 Weekly Timetable")
        st.dataframe(timetable_df, width="stretch")

        save_study_history(
            user_id=st.session_state["user"]["user_id"],
            gpa=data["current_gpa"],
            target_gpa=data["target_gpa"],
            learning_style="NA",
            predicted_hours=subject_hours,
            timetable=timetable_df.to_dict()
        )

        st.success("Study plan generated & saved!")

# ---------------- HISTORY ----------------
if page == "History":
    st.title("📜 History")

    history = get_user_history(st.session_state["user"]["user_id"])
    if not history:
        st.info("No history found.")
    else:
        df = pd.DataFrame(
            [{"Date": d, "Predicted": p} for p, _, d in history]
        )
        st.dataframe(df, width="stretch")

        if st.button("🗑️ Delete History"):
            delete_user_history(st.session_state["user"]["user_id"])
            st.success("History deleted.")
            st.rerun()
