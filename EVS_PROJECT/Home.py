# EVS_PROJECT/Home.py

import streamlit as st
import pandas as pd
from pages.constants import LOAD_PROFILES # Import constants from the new utility file

st.set_page_config(
    page_title="Renewable Energy Optimization", 
    layout="wide"
)

# --- Main Page Content ---
st.title("⚡ Renewable Energy Optimization & Scaling Project")
st.markdown("A demonstration combining a **Physical Working Model** with a **Computational Scaling Application**.")

st.header("Project Goal")
st.markdown("""
Our objective is to compare the estimated power output from Solar, Wind, and Hydropower sources. We use **measured data** from small-scale physical models, **scale** that output up to industrial standards, and then evaluate its efficiency in fulfilling real-world energy demands (Optimization).
""")

st.subheader("Optimization Goal")
st.info(f"The energy needs for different load profiles are defined in the app:")
st.dataframe(pd.DataFrame(list(LOAD_PROFILES.items()), columns=['Load Profile', 'Daily Need (kWh)']).set_index('Load Profile'))

st.markdown("---")
st.subheader("Start Calculation")
st.markdown("Please select a calculator from the **sidebar** to begin the simulation.")

# --- Sidebar Note ---
st.sidebar.success("Select a Calculator above.")