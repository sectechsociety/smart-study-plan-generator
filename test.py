import pandas as pd
import numpy as np
import math 

from tensorflow.keras import layers, models
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv('data/synthetic_full.csv')

subjects = ['Mathematics','Physics','Chemistry','Computer Science','English']
X = df[['current_gpa','target_gpa','ls0','ls1','ls2','ls3','w_Mathematics','w_Physics','w_Chemistry','w_Computer Science','w_English']].values
y = df[[f'y_{s}' for s in subjects]].values

loaded_model = models.load_model('model/study_model.h5')
x_test, y_test = X[:1000], y[:1000]
loss  = loaded_model.evaluate(x_test, y_test, verbose=2)
print(f'Loaded model loss (MSE): {loss}')
print(f'Loaded model loss (RMSE): {math.sqrt(loss):.2f}')