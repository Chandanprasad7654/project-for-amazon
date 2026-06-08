# EVS_PROJECT/pages/2_Wind_Calculator.py

import streamlit as st
import numpy as np
from pages.constants import (
    SMALL_TURBINE_EFFICIENCY, LARGE_TURBINE_EFFICIENCY, AIR_DENSITY, LOAD_PROFILES
)

# --- Utility Functions ---

def scale_energy_to_industry(energy_kwh, small_eff, large_eff):
    """ Scales the energy based on the ratio of large vs. small efficiency. """
    scaling_factor = large_eff / small_eff
    scaled_energy = energy_kwh * scaling_factor
    return scaled_energy, scaling_factor

def calculate_wind_power(diameter, wind_speed, operational_hours):
    """ Calculates raw energy using a fixed small turbine efficiency. """
    radius = diameter / 2
    swept_area = np.pi * (radius ** 2)
    
    # Power (W) = 0.5 * rho * Area * V^3 * Cp 
    power_watts = 0.5 * AIR_DENSITY * swept_area * (wind_speed ** 3) * SMALL_TURBINE_EFFICIENCY
    
    # Daily Energy (kWh)
    daily_energy_kwh = (power_watts / 1000) * operational_hours
    return daily_energy_kwh

# --- Page Layout ---

st.title("💨 Wind Turbine Energy Output & Optimization")
st.markdown(
    f"Simulating a **{SMALL_TURBINE_EFFICIENCY*100:.0f}% efficiency small turbine** and scaling the output to an **{LARGE_TURBINE_EFFICIENCY*100:.0f}% efficiency industrial turbine.**"
)

# --- User Inputs ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Turbine Specifications")
    rotor_diameter = st.number_input("Rotor Diameter (meters)", min_value=0.01, max_value=200.0, value=50.0, step=1.0)
    wind_operational_hours = st.slider("Operational Hours per Day (h)", min_value=1.0, max_value=24.0, value=20.0, step=1.0)

with col2:
    st.subheader("Physical Model Measurement & Optimization Goal")
    avg_wind_speed = st.slider("Average Wind Speed ($m/s$)", min_value=1.0, max_value=25.0, value=8.0, step=0.5)
    
    selected_load_profile = st.selectbox(
        "Select Energy Need to Fulfill:",
        list(LOAD_PROFILES.keys())
    )
    load_kwh = LOAD_PROFILES[selected_load_profile]


# --- Calculations and Display ---
small_turbine_output_w = calculate_wind_power(rotor_diameter, avg_wind_speed, wind_operational_hours)
scaled_output_w, scaling_factor_w = scale_energy_to_industry(small_turbine_output_w, SMALL_TURBINE_EFFICIENCY, LARGE_TURBINE_EFFICIENCY)
fulfillment_percent_w = (scaled_output_w / load_kwh) * 100

st.divider()
st.subheader("Results")

col_w1, col_w2, col_w3 = st.columns(3)

with col_w1: 
    st.metric(label="Small Turbine Output", value=f"{small_turbine_output_w:.2f} kWh/day")

with col_w2: 
    st.metric(label="Industrial Turbine Output", 
              value=f"{scaled_output_w:.2f} kWh/day",
              delta=f"Scaled by {scaling_factor_w:.1f}x")

with col_w3: 
    st.metric(label=f"Fulfillment of {selected_load_profile} Need", 
              value=f"{fulfillment_percent_w:.1f} %",
              delta=("Surplus" if fulfillment_percent_w >= 100 else "Deficit"))

st.markdown("---")
st.subheader("Formula Used:")
st.latex(r'''
    \text{Power} (P) = \frac{1}{2} \times \rho \times A \times V^3 \times C_p
    \quad \Rightarrow \quad \text{Energy}_{\text{scaled}} = \frac{P_{\text{meas}}}{1000} \times \text{Hours} \times \frac{\text{Efficiency}_{\text{Industrial}}}{\text{Efficiency}_{\text{Small}}}
''')