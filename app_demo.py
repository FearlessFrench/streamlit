import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# App title
st.title("📊 Demo Streamlit App")
st.write("This is a mock-up Streamlit app to demonstrate layout and features.")

# Sidebar
st.sidebar.title("Controls")
name = st.sidebar.text_input("Enter your name:", "Guest")
show_chart = st.sidebar.checkbox("Show Chart", value=True)
number = st.sidebar.slider("Pick a number", 1, 100, 25)

# Main body
st.header(f"welcome, {name} 👋")

# Data table
data =pd.DataFrame({
    "A": np.random.rand(10),
    "B": np.random.rand(10)
})
st.subheader("Sample Data")
st.dataframe(data)

# Chart
if show_chart:
    st.subheader("Line Chart Example")
    st.line_chart(data)

# Custom plot
st.subheader("Matplotlib Chart")
fig, ax = plt.subplots()
ax.plot(data["A"], data["B"], "o-", color="orange")
ax.set_title("Random Scatter")
st.pyplot(fig)

# Result from number input
st.subheader("Number Squared")
st.write(f"**{number}² = {number**2}**")

# Open in Integrated Terminal
# PS C:\Users\Christopher French\Downloads\ビニート\Streamlit> streamlit run app_demo.py