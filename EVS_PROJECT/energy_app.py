import streamlit as st
import pandas as pd
import numpy as np

# --- 1. System Constants (Used for Scaling and Optimization) ---

# Efficiency (Used for Scaling Factor)
SMALL_PANEL_EFFICIENCY = 0.10      # e.g., 10% efficiency for the small solar panel
LARGE_PANEL_EFFICIENCY = 0.22      # e.g., 22% efficiency for industrial solar
SMALL_TURBINE_EFFICIENCY = 0.30    # e.g., 30% for the small wind/hydro turbine
LARGE_TURBINE_EFFICIENCY = 0.45    # e.g., 45% for industrial wind/hydro turbine

# Environmental Constants
AIR_DENSITY = 1.225 # kg/m^3
WATER_DENSITY = 1000 # kg/m^3
GRAVITY = 9.81      # m/s^2

# Energy needs (Optimization Goal)
LOAD_PROFILES = {
    "Small House": 15,    # kWh/day
    "Medium House": 30,   # kWh/day
    "Small Firm": 200,    # kWh/day
    "Large Firm": 5000    # kWh/day
}

# --- 2. Calculation Functions ---

def scale_energy_to_industry(energy_kwh, small_eff, large_eff):
    """ Scales the energy based on the ratio of large vs. small efficiency. """
    scaling_factor = large_eff / small_eff
    scaled_energy = energy_kwh * scaling_factor
    return scaled_energy, scaling_factor

# --- Solar Functions ---
def calculate_solar_power(measured_voltage, measured_current, sun_hours):
    measured_power_watts = measured_voltage * measured_current
    daily_energy_wh = measured_power_watts * sun_hours
    return daily_energy_wh / 1000 # returns kWh/day

# --- Wind Functions ---
def calculate_wind_power(diameter, wind_speed, operational_hours):
    """ Calculates raw energy using a fixed small turbine efficiency (SMALL_TURBINE_EFFICIENCY). """
    radius = diameter / 2
    swept_area = np.pi * (radius ** 2)
    
    # Power (W) = 0.5 * rho * Area * V^3 * Cp 
    power_watts = 0.5 * AIR_DENSITY * swept_area * (wind_speed ** 3) * SMALL_TURBINE_EFFICIENCY
    
    # Daily Energy (kWh)
    daily_energy_kwh = (power_watts / 1000) * operational_hours
    return daily_energy_kwh

# --- Hydro Functions ---
def calculate_hydro_power(flow_rate, effective_head, operational_hours):
    """ Calculates raw energy using a fixed small turbine efficiency (SMALL_TURBINE_EFFICIENCY). """
    # Power (W) = rho * g * Q * h * eta
    power_watts = WATER_DENSITY * GRAVITY * flow_rate * effective_head * SMALL_TURBINE_EFFICIENCY
    
    # Daily Energy (kWh)
    daily_energy_kwh = (power_watts / 1000) * operational_hours
    return daily_energy_kwh


# --- 3. Streamlit App Layout ---

st.set_page_config(page_title="Energy Optimization App", layout="wide")
st.title("⚡ Renewable Energy Optimization & Scaling")

# Initialize results dictionary
results = {}

# --- Optimization Goal Selector (Placed at the top for unified comparison) ---
st.sidebar.header("Optimization Goal")
selected_load_profile = st.sidebar.selectbox(
    "Select Energy Need to Fulfill:",
    list(LOAD_PROFILES.keys())
)
load_kwh = LOAD_PROFILES[selected_load_profile]
st.sidebar.metric(f"{selected_load_profile} Needs", f"{load_kwh} kWh/day")


# --- A. Solar Panel Calculator ---
st.header("🌞 1. Solar Panel Energy Output & Scaling")
st.markdown(
    f"Simulating a **{SMALL_PANEL_EFFICIENCY*100:.0f}% efficiency small panel** and scaling the output to an **{LARGE_PANEL_EFFICIENCY*100:.0f}% efficiency industrial panel.**"
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Physical Model Measurements (from your small panel)")
    measured_voltage = st.number_input("Measured Voltage (V)", min_value=0.1, max_value=30.0, value=15.0, step=0.1, key='s_volt')
    measured_current = st.number_input("Measured Current (A)", min_value=0.01, max_value=10.0, value=2.0, step=0.05, key='s_curr')

with col2:
    st.subheader("Environmental Inputs")
    sun_hours = st.slider("Equivalent Peak Sun Hours per Day (h)", min_value=1.0, max_value=12.0, value=5.0, step=0.5, key='s_hours')


# Calculations and Display (Solar)
small_panel_output = calculate_solar_power(measured_voltage, measured_current, sun_hours)
scaled_output_s, scaling_factor_s = scale_energy_to_industry(small_panel_output, SMALL_PANEL_EFFICIENCY, LARGE_PANEL_EFFICIENCY)
results['Solar'] = scaled_output_s
fulfillment_percent_s = (scaled_output_s / load_kwh) * 100

st.divider()

col_s1, col_s2, col_s3 = st.columns(3)
with col_s1: st.metric(label="Small Panel Output", value=f"{small_panel_output:.2f} kWh/day")
with col_s2: st.metric(label="Industrial Panel Output", value=f"{scaled_output_s:.2f} kWh/day", delta=f"Scaled by {scaling_factor_s:.1f}x")
with col_s3: st.metric(label=f"Fulfillment of {selected_load_profile} Need", value=f"{fulfillment_percent_s:.1f} %")


# --- B. Wind Turbine Calculator ---
st.divider()
st.header("💨 2. Wind Turbine Energy Output & Scaling")
st.markdown(
    f"Simulating a **{SMALL_TURBINE_EFFICIENCY*100:.0f}% efficiency small turbine** and scaling the output to an **{LARGE_TURBINE_EFFICIENCY*100:.0f}% efficiency industrial turbine.**"
)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Turbine Specifications")
    rotor_diameter = st.number_input("Rotor Diameter (meters)", min_value=1.0, max_value=200.0, value=50.0, step=1.0, key='w_diam')
    wind_operational_hours = st.slider("Operational Hours per Day (h)", min_value=1.0, max_value=24.0, value=20.0, step=1.0, key='w_hours')

with col4:
    st.subheader("Physical Model Measurement")
    avg_wind_speed = st.slider("Average Wind Speed ($m/s$)", min_value=1.0, max_value=25.0, value=8.0, step=0.5, key='w_speed')

# Calculations and Display (Wind)
small_turbine_output_w = calculate_wind_power(rotor_diameter, avg_wind_speed, wind_operational_hours)
scaled_output_w, scaling_factor_w = scale_energy_to_industry(small_turbine_output_w, SMALL_TURBINE_EFFICIENCY, LARGE_TURBINE_EFFICIENCY)
results['Wind'] = scaled_output_w
fulfillment_percent_w = (scaled_output_w / load_kwh) * 100

st.divider()

col_w1, col_w2, col_w3 = st.columns(3)
with col_w1: st.metric(label="Small Turbine Output", value=f"{small_turbine_output_w:.2f} kWh/day")
with col_w2: st.metric(label="Industrial Turbine Output", value=f"{scaled_output_w:.2f} kWh/day", delta=f"Scaled by {scaling_factor_w:.1f}x")
with col_w3: st.metric(label=f"Fulfillment of {selected_load_profile} Need", value=f"{fulfillment_percent_w:.1f} %")


# --- C. Hydropower Calculator ---
st.divider()
st.header("💧 3. Hydropower Energy Output & Scaling")
st.markdown(
    f"Simulating a **{SMALL_TURBINE_EFFICIENCY*100:.0f}% efficiency small turbine** and scaling the output to an **{LARGE_TURBINE_EFFICIENCY*100:.0f}% efficiency industrial turbine.**"
)

col5, col6 = st.columns(2)

with col5:
    st.subheader("Physical Model Measurements")
    flow_rate = st.number_input("Water Flow Rate ($m^3/s$)", min_value=0.01, max_value=10.0, value=1.5, step=0.1, key='h_flow')
    effective_head = st.number_input("Effective Head (Vertical Drop in meters)", min_value=1.0, max_value=200.0, value=30.0, step=1.0, key='h_head')

with col6:
    st.subheader("Operational Inputs")
    hydro_operational_hours = st.slider("Operational Hours per Day (h)", min_value=1.0, max_value=24.0, value=24.0, step=1.0, key='h_hours')
    st.markdown(f"*(Using $\\rho$: **{WATER_DENSITY} kg/$m^3$** and $g$: **{GRAVITY} m/$s^2$**)*")

# Calculations and Display (Hydro)
small_turbine_output_h = calculate_hydro_power(flow_rate, effective_head, hydro_operational_hours)
scaled_output_h, scaling_factor_h = scale_energy_to_industry(small_turbine_output_h, SMALL_TURBINE_EFFICIENCY, LARGE_TURBINE_EFFICIENCY)
results['Hydro'] = scaled_output_h
fulfillment_percent_h = (scaled_output_h / load_kwh) * 100

st.divider()

col_h1, col_h2, col_h3 = st.columns(3)
with col_h1: st.metric(label="Small Turbine Output", value=f"{small_turbine_output_h:.2f} kWh/day")
with col_h2: st.metric(label="Industrial Turbine Output", value=f"{scaled_output_h:.2f} kWh/day", delta=f"Scaled by {scaling_factor_h:.1f}x")
with col_h3: st.metric(label=f"Fulfillment of {selected_load_profile} Need", value=f"{fulfillment_percent_h:.1f} %")


# --- D. Final Comparison Chart (Optimization Summary) ---
st.divider()
st.header("📈 4. Optimization Summary: Daily Energy Production Comparison")
st.subheader(f"Industrial-Scale Production vs. {selected_load_profile} Load ({load_kwh} kWh/day)")

results_df = pd.DataFrame(
    list(results.items()), 
    columns=['Source', 'Industrial Output (kWh)']
)
results_df.set_index('Source', inplace=True)

st.bar_chart(results_df)
st.dataframe(results_df.T, use_container_width=True)


# --- E. Circuit Demonstration (Final Requirement) ---
st.divider()
st.header("🔌 5. Electrical Energy Production Demonstration")
st.markdown(
    "This section highlights the essential electrical components required to convert the raw energy into usable AC electricity, a key part of our project demonstration."
)
st.subheader("Key System Components")
st.markdown("""
* **Solar Panel:** Converts light (photons) into **DC** power.
* **Wind/Hydro Turbine + Generator:** Converts mechanical motion into **AC** power.
* **Inverter:** Crucial component for solar, converting DC to AC power usable by the grid or home appliances.
* **Grid Tie/Control Systems:** Manage power flow and voltage synchronization.
""")