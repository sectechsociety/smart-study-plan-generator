import pandas as pd
import numpy as np
from tensorflow.keras import layers, models

df = pd.read_csv('data/synthetic_full.csv')

# INPUT FEATURES
X = df[['current_gpa', 'target_gpa']].values

# CREATE total_hours from old subject outputs
subject_cols = [
    'y_Mathematics',
    'y_Physics',
    'y_Chemistry',
    'y_Computer Science',
    'y_English'
]

df['total_hours'] = df[subject_cols].sum(axis=1)
y = df[['total_hours']].values

# MODEL
model = models.Sequential([
    layers.Input(shape=(X.shape[1],)),
    layers.Dense(64, activation='relu'),
    layers.Dense(32, activation='relu'),
    layers.Dense(1, activation='linear')
])

model.compile(optimizer='adam', loss='mse')

model.fit(X, y, epochs=40, batch_size=32, validation_split=0.1)

model.save('model/total_hours_model.h5')

print("✅ Model trained and saved successfully")
print("Input features:", X.shape[1])
