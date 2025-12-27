# 📘 Smart Study Plan Generator (AI-Powered)

A Neural Network–based academic planning system developed as part of the **Neural Networks course project**.  
This application intelligently predicts **weekly study hours**, distributes them **subject-wise**, and generates a **personalized weekly timetable** based on student performance and availability.

---

## 📌 Overview

Students often struggle to decide **how much to study**, **what to prioritize**, and **how to manage limited free time**.  
The **Smart Study Plan Generator** solves this by using **Artificial Neural Networks (ANN)** to generate **data-driven, personalized study plans**.

The system:
- Predicts **total weekly study hours** using CGPA data
- Distributes hours based on **subject difficulty**
- Ensures **every subject is scheduled**, even with limited free time
- Stores history so students can revisit previous plans anytime

This project combines **Machine Learning, Scheduling Logic, and Web Application Development** into a single end-to-end solution.

---

## ✨ Features

- 🤖 **Neural Network–based Prediction**
  - ANN model predicts total weekly study hours using Current CGPA & Target CGPA

- 📘 **Dynamic Subject Handling**
  - Users can add **any number of subjects**
  - Difficulty level (1–5) controls time allocation

- 📅 **Smart Timetable Generator**
  - Two-phase scheduling algorithm:
    - Guarantees at least **one slot per subject**
    - Fills remaining slots proportionally

- 👤 **User Authentication**
  - Login & signup system using SQLite
  - Each user has independent study plans

- 🕒 **Time-Slot Based Scheduling**
  - Users select available time slots per day
  - Timetable generated only within selected slots

- 💾 **Persistent History**
  - Study plans are saved in database
  - Latest timetable is shown on Home page after re-login

- 🧠 **Fallback Logic**
  - Rule-based backup if ML model is unavailable

---

## 🚀 Getting Started

Follow these steps to run the project locally.

---

### ✅ Prerequisites

- Python **3.9 – 3.11** (Recommended)
- Git
- Virtual Environment support
- TensorFlow (CPU version is sufficient)

> ⚠️ **Note:** Python 3.13 may cause TensorFlow issues. Python 3.10 is recommended.

---

### 🔧 Installation & Setup

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/smart-study-plan-generator.git
cd smart-study-plan-generator
```
#### 2️⃣ Create Virtual Environment
```
python -m venv venv
```

Activate it:

Windows
```
venv\Scripts\activate
```

macOS / Linux
```
source venv/bin/activate
```
#### 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```
#### 4️⃣ Train the Neural Network Model
```
python train_and_export_model.py
```

This will create:

model/
 ├── total_hours_model.h5
 └── study_model.h5

#### 5️⃣ Run the Application
```
streamlit run app.py
```

Open in browser:

http://localhost:8501

### 🧠 Neural Network Details

Model 1: Total Weekly Hours Predictor

Inputs: Current CGPA, Target CGPA

Output: Total study hours per week

Architecture: Fully Connected ANN

Loss Function: Mean Squared Error (MSE)

Model 2: Subject-wise Hours Predictor (Optional)

Predicts subject-wise distribution when fixed subjects are used

### 🛠️ Project Pipeline
🔹 Stage 1: Data Preparation

Synthetic academic dataset created

Includes CGPA, difficulty levels, learning patterns

🔹 Stage 2: Model Training

ANN trained using TensorFlow/Keras

Evaluated using MSE & RMSE

🔹 Stage 3: Study Plan Generation

Predict total weekly hours

Distribute hours based on difficulty

Schedule timetable using availability

🔹 Stage 4: Application Integration

Streamlit UI

SQLite database

Persistent history & login system

### 📊 Algorithm for Timetable Scheduling

Two-Phase Scheduling Logic

1️⃣ Guarantee Phase

Ensures every subject appears at least once

2️⃣ Optimization Phase

Remaining slots filled based on difficulty

Prevents subject starvation when time is limited

### 🧪 Model Evaluation

Loss (MSE): ~0.03

RMSE: ~0.19

Indicates accurate prediction of study hours

### 🤝 Team & Contributions

This project was developed as a 2-member Team.

Team Member	Responsibilities

Astle Joe A S	- Neural Network design, model training
Mithik Jain G -	UI development, database integration, authentication

### 📌 Conclusion

The Smart Study Plan Generator demonstrates how Neural Networks can be applied to real-world academic planning problems.
By combining ML prediction, optimization logic, and full-stack deployment, the project delivers a practical, intelligent solution for students.
