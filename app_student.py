# Requirements: Make sure I install these packages
#!pip install streamlit pandas plotly

import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("student_habits_performance.csv")

df = load_data()

# App title
st.title("🎓 Student Habits and Academic Performance Dashboard")

# Sidebar filters
st.sidebar.header("🔍 Filter Students")
gender_filter = st.sidebar.multiselect("Gender", df["gender"])