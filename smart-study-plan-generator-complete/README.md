# 📘 Smart Study Plan Generator

An AI-powered web application that generates a **personalized weekly study timetable** for students using **Neural Networks**, based on their CGPA, target CGPA, subject difficulty, and available time slots.

---

## 🚀 Features

- 🔐 User Authentication (Login & Signup)
- 📊 CGPA-based study hour prediction using Neural Network
- 🧠 AI-driven subject-wise hour allocation
- ✍️ Dynamic subject entry (users can add any subject)
- 🕒 Time-slot based weekly timetable generation
- 💾 Persistent history using SQLite database
- 🏠 Home page shows **last generated timetable even after logout**
- 📜 History view with delete option
- 📄 Exportable & structured study plans
- 🌐 Interactive Streamlit UI

---

## 🧠 How It Works

1. User logs in / signs up
2. Enters:
   - Current CGPA
   - Target CGPA
   - Subjects with difficulty levels
   - Available daily time slots
3. Neural Network predicts **total weekly study hours**
4. Hours are distributed across subjects based on difficulty
5. A **weekly timetable** is generated and stored
6. Latest plan is shown on Home page (even after re-login)

---

## 🛠 Tech Stack

| Layer            | Technology         |
| ---------------- | ------------------ |
| Frontend         | Streamlit          |
| Backend          | Python             |
| Machine Learning | TensorFlow / Keras |
| Database         | SQLite             |
| Data Handling    | Pandas, NumPy      |
| Version Control  | Git & GitHub       |

---

## ▶️ Run the Project Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/smart-study-plan-generator.git
cd smart-study-plan-generator
```

### 2️⃣ Create & activate virtual environment

```
python -m venv venv
venv\Scripts\activate # Windows
```

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Train the Neural Network (optional)

```
python train_and_export_model.py
```

### 5️⃣ Run the application

```
streamlit run app.py
```

### 📊 Neural Network Details

## Input:

Current CGPA

Target CGPA

## Output:

Predicted total weekly study hours

### Architecture:

Fully connected feedforward network

Optimized using Mean Squared Error loss

## 🧪 Database

SQLite database (study_planner.db)

#### Stores:

User details

Study plan history

Timetable & predicted hours (JSON format)

## 📌 Future Enhancements

📈 Progress comparison across multiple plans

📅 Calendar-style timetable UI

🧠 Adaptive learning based on past performance

☁️ Cloud deployment (Streamlit Cloud)

📱 Mobile-friendly UI
