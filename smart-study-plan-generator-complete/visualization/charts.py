
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd

def plot_bar_chart(predicted):
    subjects = list(predicted.keys())
    hours = [predicted[s] for s in subjects]
    fig, ax = plt.subplots(figsize=(6,3))
    ax.bar(subjects, hours)
    ax.set_ylabel("Hours per week")
    ax.set_title("Predicted Study Hours")
    plt.xticks(rotation=30, ha='right')
    st.pyplot(fig)

def plot_timetable_heatmap(timetable_df):
    df = timetable_df.fillna("")
    subjects = sorted({s for s in df.values.flatten() if s!=""})
    if not subjects:
        st.info("No subjects scheduled yet.")
        return
    heat = pd.DataFrame(0, index=subjects, columns=df.columns)
    for col in df.columns:
        for val in df[col].values:
            if val in subjects:
                heat.loc[val, col] += 1
    fig, ax = plt.subplots(figsize=(8, len(subjects)*0.4 + 1))
    cax = ax.imshow(heat.values, aspect='auto')
    ax.set_yticks(range(len(subjects)))
    ax.set_yticklabels(subjects)
    ax.set_xticks(range(len(heat.columns)))
    ax.set_xticklabels(heat.columns)
    ax.set_title("Timetable heatmap (counts of slots per subject per day)")
    for (i, j), val in np.ndenumerate(heat.values):
        if val>0:
            ax.text(j, i, int(val), ha='center', va='center', color='white')
    plt.colorbar(cax, ax=ax)
    st.pyplot(fig)
