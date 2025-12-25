
# train_and_export_model.py
# Run this script locally to train the model and save model/study_model.h5
import pandas as pd
import numpy as np
from tensorflow.keras import layers, models

df = pd.read_csv('data/synthetic_full.csv')
subjects = ['Mathematics','Physics','Chemistry','Computer Science','English']
X = df[['current_gpa','target_gpa','ls0','ls1','ls2','ls3','w_Mathematics','w_Physics','w_Chemistry','w_Computer Science','w_English']].values
y = df[[f'y_{s}' for s in subjects]].values

model = models.Sequential([
    layers.Input(shape=(X.shape[1],)),
    layers.Dense(128, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(len(subjects), activation='linear')
])
model.compile(optimizer='adam', loss='mse')

model.fit(X, y, epochs=30, batch_size=64, validation_split=0.1)
model.save('model/study_model.h5')
print('Model trained and saved.')
print("Input feature count:", X.shape[1])
