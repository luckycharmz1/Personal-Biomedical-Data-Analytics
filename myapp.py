import streamlit as st
import pandas as pd

# My first app
st.write("Charmaine's Data")

# Read the data
df = pd.read_csv("/Samsung Health")

# Display the line chart
st.line_chart(df)
