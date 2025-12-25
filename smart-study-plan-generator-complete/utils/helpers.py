
import os
import numpy as np

SUBJECTS = ['Mathematics', 'Physics', 'Chemistry', 'Computer Science', 'English']

def default_subjects():
    return SUBJECTS

def _make_input_vector(weakness_dict, current_gpa, target_gpa, learning_style):
    style_map = {'Visual':0,'Auditory':1,'Reading/Writing':2,'Kinesthetic':3}
    ls = [0,0,0,0]
    ls[style_map.get(learning_style,0)] = 1
    wk = [weakness_dict.get(s,2) for s in SUBJECTS]
    vec = [float(current_gpa), float(target_gpa)] + ls + wk
    return np.array(vec, dtype=float).reshape(1, -1)

def predict_study_hours(weakness_dict, current_gpa, target_gpa, learning_style):
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model', 'study_model.h5')
    x = _make_input_vector(weakness_dict, current_gpa, target_gpa, learning_style)
    try:
        from tensorflow.keras.models import load_model
        model = load_model(model_path)
        preds = model.predict(x)[0]
        return {SUBJECTS[i]: round(float(max(0.5, preds[i])),1) for i in range(len(SUBJECTS))}
    except Exception as e:
        # fallback deterministic rule
        gap = max(0.0, float(target_gpa) - float(current_gpa))
        base_hours = {}
        for subj, w in weakness_dict.items():
            hours = 1 + (w * 0.9)
            hours *= (1 + 0.1 * gap)
            if learning_style == 'Visual' and subj in ['Mathematics','Computer Science']:
                hours *= 1.05
            if learning_style == 'Reading/Writing' and subj in ['English','Chemistry']:
                hours *= 1.05
            base_hours[subj] = round(hours,1)
        return base_hours
