import pandas as pd
import numpy as np
import math
import warnings

from tensorflow.keras import models

warnings.filterwarnings("ignore")

# ---------------- LOAD DATA ----------------
df = pd.read_csv('data/synthetic_full.csv')

subjects = [
    'Mathematics',
    'Physics',
    'Chemistry',
    'Computer Science',
    'English'
]

X = df[
    [
        'current_gpa', 'target_gpa',
        'ls0', 'ls1', 'ls2', 'ls3',
        'w_Mathematics', 'w_Physics', 'w_Chemistry',
        'w_Computer Science', 'w_English'
    ]
].values

y = df[[f'y_{s}' for s in subjects]].values

# ---------------- LOAD MODEL ----------------
loaded_model = models.load_model(
    "model/study_model.h5",
    compile=False   # skip old compile info
)

# ✅ RE-COMPILE (FIX)
loaded_model.compile(
    optimizer="adam",
    loss="mse"
)

# ---------------- EVALUATE ----------------
x_test, y_test = X[:1000], y[:1000]

loss = loaded_model.evaluate(x_test, y_test, verbose=2)

print(f"Loaded model loss (MSE): {loss:.4f}")
print(f"Loaded model loss (RMSE): {math.sqrt(loss):.2f}")
