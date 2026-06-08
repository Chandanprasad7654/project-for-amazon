# EVS_PROJECT/pages/3_Hydro_Calculator.py

import streamlit as st
from pages.constants import (
    SMALL_TURBINE_EFFICIENCY, LARGE_TURBINE_EFFICIENCY, WATER_DENSITY, GRAVITY, LOAD_PROFILES
)

# --- Utility Functions ---

def scale_energy_to_industry(energy_kwh, small_eff, large_eff):
    """ Scales the energy based on the ratio of large vs. small efficiency. """
    scaling_factor = large_eff / small_eff
    scaled_energy = energy_kwh * scaling_factor
    return scaled_energy, scaling_factor

def calculate_hydro_power(flow_rate, effective_head, operational_hours):
    """ Calculates raw energy using a fixed small turbine efficiency. """
    # Power (W) = rho * g * Q * h * eta
    power_watts = WATER_DENSITY * GRAVITY * flow_rate * effective_head * SMALL_TURBINE_EFFICIENCY
    
    # Daily Energy (kWh)
    daily_energy_kwh = (power_watts / 1000) * operational_hours
    return daily_energy_kwh

# --- Page Layout ---

st.title("💧 Hydropower Energy Output & Optimization")
st.markdown(
    f"Simulating a **{SMALL_TURBINE_EFFICIENCY*100:.0f}% efficiency small turbine** and scaling the output to an **{LARGE_TURBINE_EFFICIENCY*100:.0f}% efficiency industrial turbine.**"
)

# --- User Inputs ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Physical Model Measurements")
    flow_rate = st.number_input("Water Flow Rate ($m^3/s$)", min_value=0.01, max_value=10.0, value=1.5, step=0.1)
    effective_head = st.number_input("Effective Head (Vertical Drop in meters)", min_value=1.0, max_value=200.0, value=30.0, step=1.0)
    st.markdown(f"*(Using $\\rho$: **{WATER_DENSITY} kg/$m^3$** and $g$: **{GRAVITY} m/$s^2$**)*")

with col2:
    st.subheader("Operational Inputs & Optimization Goal")
    hydro_operational_hours = st.slider("Operational Hours per Day (h)", min_value=1.0, max_value=24.0, value=24.0, step=1.0)
    
    selected_load_profile = st.selectbox(
        "Select Energy Need to Fulfill:",
        list(LOAD_PROFILES.keys())
    )
    load_kwh = LOAD_PROFILES[selected_load_profile]

# --- Calculations and Display ---
small_turbine_output_h = calculate_hydro_power(flow_rate, effective_head, hydro_operational_hours)
scaled_output_h, scaling_factor_h = scale_energy_to_industry(small_turbine_output_h, SMALL_TURBINE_EFFICIENCY, LARGE_TURBINE_EFFICIENCY)
fulfillment_percent_h = (scaled_output_h / load_kwh) * 100

st.divider()
st.subheader("Results")

col_h1, col_h2, col_h3 = st.columns(3)

with col_h1: 
    st.metric(label="Small Turbine Output", value=f"{small_turbine_output_h:.2f} kWh/day")

with col_h2: 
    st.metric(label="Industrial Turbine Output", 
              value=f"{scaled_output_h:.2f} kWh/day", 
              delta=f"Scaled by {scaling_factor_h:.1f}x")

with col_h3: 
    st.metric(label=f"Fulfillment of {selected_load_profile} Need", 
              value=f"{fulfillment_percent_h:.1f} %",
              delta=("Surplus" if fulfillment_percent_h >= 100 else "Deficit"))

st.markdown("---")
st.subheader("Formula Used:")
st.latex(r'''
    \text{Power} (P) = \rho \times g \times Q \times h \times \eta
    \quad \Rightarrow \quad \text{Energy}_{\text{scaled}} = \frac{P_{\text{meas}}}{1000} \times \text{Hours} \times \frac{\text{Efficiency}_{\text{Industrial}}}{\text{Efficiency}_{\text{Small}}}
''')