# EVS_PROJECT/pages/1_Solar_Calculator.py

import streamlit as st
import numpy as np
from pages.constants import (
    SMALL_PANEL_EFFICIENCY, LARGE_PANEL_EFFICIENCY, LOAD_PROFILES
)

# --- Utility Functions (Only the ones needed here) ---

def scale_energy_to_industry(energy_kwh, small_eff, large_eff):
    """ Scales the energy based on the ratio of large vs. small efficiency. """
    scaling_factor = large_eff / small_eff
    scaled_energy = energy_kwh * scaling_factor
    return scaled_energy, scaling_factor

def calculate_solar_power(measured_voltage, measured_current, sun_hours):
    """ Calculates power based on measured V/I and converts to daily energy (kWh). """
    measured_power_watts = measured_voltage * measured_current
    daily_energy_wh = measured_power_watts * sun_hours
    return daily_energy_wh / 1000 # returns kWh/day


# --- Page Layout ---

st.title("🌞 Solar Panel Energy Output & Optimization")
st.markdown(
    f"Simulating a **{SMALL_PANEL_EFFICIENCY*100:.0f}% efficiency small panel** and scaling the output to an **{LARGE_PANEL_EFFICIENCY*100:.0f}% efficiency industrial panel.**"
)

# --- User Inputs ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Physical Model Measurements (from your small panel)")
    measured_voltage = st.number_input("Measured Voltage (V)", min_value=0.1, max_value=30.0, value=15.0, step=0.1)
    measured_current = st.number_input("Measured Current (A)", min_value=0.01, max_value=10.0, value=2.0, step=0.05)

with col2:
    st.subheader("Environmental Inputs & Optimization Goal")
    sun_hours = st.slider("Equivalent Peak Sun Hours per Day (h)", min_value=1.0, max_value=12.0, value=5.0, step=0.5)
    
    selected_load_profile = st.selectbox(
        "Select Energy Need to Fulfill:",
        list(LOAD_PROFILES.keys())
    )
    load_kwh = LOAD_PROFILES[selected_load_profile]


# --- Calculations and Display ---

# 1. Calculate energy from the small panel
small_panel_output = calculate_solar_power(measured_voltage, measured_current, sun_hours)

# 2. Scale the energy to an industry-grade panel
scaled_output_s, scaling_factor_s = scale_energy_to_industry(small_panel_output, SMALL_PANEL_EFFICIENCY, LARGE_PANEL_EFFICIENCY)

# 3. Calculate fulfillment percentage
fulfillment_percent_s = (scaled_output_s / load_kwh) * 100


st.divider()
st.subheader("Results")

col_s1, col_s2, col_s3 = st.columns(3)

with col_s1: 
    st.metric(label="Small Panel (Measured) Output", value=f"{small_panel_output:.2f} kWh/day")

with col_s2: 
    st.metric(label="Industrial Panel (Scaled) Output", 
              value=f"{scaled_output_s:.2f} kWh/day",
              delta=f"Scaled by {scaling_factor_s:.1f}x")

with col_s3: 
    st.metric(label=f"Fulfillment of {selected_load_profile} Need", 
              value=f"{fulfillment_percent_s:.1f} %",
              delta=("Surplus" if fulfillment_percent_s >= 100 else "Deficit"))

st.markdown("---")
st.subheader("Formula Used:")
st.latex(r'''
    \text{Energy}_{\text{scaled}} = (\text{V}_{\text{meas}} \times \text{I}_{\text{meas}} \times \text{Hours}) \times \frac{\text{Efficiency}_{\text{Industrial}}}{\text{Efficiency}_{\text{Small}}}
''')