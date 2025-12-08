# 📘 Smart Study Plan Generator

# 🔹 Overview

The Smart Study Plan Generator is an AI-powered project designed to help students create personalized study plans based on their academic profile, learning style, and available free time. The system uses deep learning models to recommend study hours per subject and then maps them into a structured timetable.

This project aims to assist learners in:

Organizing study schedules effectively.

Managing time based on free slots.

Receiving adaptive study hour recommendations.

Visualizing their personalized timetable.

# 🔹 Current Progress (Work Done ✅)

The following phases have been completed:

Problem Definition

Defined the main objective: build an AI system to generate personalized study plans.

Identified inputs: GPA, learning style, available free slots, etc.

Identified outputs: recommended study hours per subject and timetable generation.

Dataset Creation

Created a synthetic dataset of 2000 student profiles with realistic patterns.

Dataset includes fields like:

Student ID

GPA

Learning Style (Visual, Auditory, Kinesthetic)

Available Hours per Day & Free Days per Week

Subject Count

Exam Priority

Weak Subjects Count

Recommended Hours Per Subject (calculated realistically based on GPA and weak subjects)

Model Development

Built a deep neural network using TensorFlow/Keras to predict study hours per subject.

Preprocessing includes standard scaling for numeric features and one-hot encoding for categorical features.

Model trained with early stopping, learning rate reduction, and best model checkpointing.

Scheduler Logic

Developed weekly schedule generation:

Maps predicted study hours into available study days.

Allocates extra hours to weak subjects.

Generates detailed and summary timetables.

Exports schedules to CSV files for further use.

# 🔹 Upcoming Work (Next Steps)

Phase 4: Streamlit integration for a user-friendly interface.

Phase 5: Testing & visualization with interactive charts and timetables.

Phase 6: Documentation & deployment (GitHub + Streamlit Cloud).

Phase 7: Final presentation & demo.

# 🔹 Tech Stack

Language: Python 🐍

Libraries: NumPy, Pandas, TensorFlow/Keras, Streamlit, Matplotlib

Tools: Jupyter/Colab for development, GitHub for version control

# 🔹 Project Status

🚧 In Progress – Currently at Phase 1–3 (Problem Definition + Dataset Creation + Model Training + Weekly Scheduler).
