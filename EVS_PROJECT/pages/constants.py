# EVS_PROJECT/pages/constants.py

# --- System Constants (Used for Scaling and Optimization) ---

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