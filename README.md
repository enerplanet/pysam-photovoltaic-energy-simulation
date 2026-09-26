# PV Power Generation Simulation Tool

This project, developed for EnerplanET, utilizes the NREL-PySAM library to simulate the power output of photovoltaic (PV) systems based on specific system specifications and local environmental data from the MERRA-2 dataset. The simulation tool is designed to integrate seamlessly into EnerplanET's service offerings, aiming to evaluate potential PV power production for specified geographic locations and PV system configurations. By providing data-driven insights, this tool helps EnerplanET's clients optimize their renewable energy strategies.

## Features

- **Load Environmental Data**: Import and utilize environmental data from the MERRA-2 dataset for accurate simulation inputs.
    
- **PV Power Generation Calculation**: Evaluate the potential power output of PV systems based on key parameters such as:
    
    - **System Capacity**: 10 kW
    - **Azimuth**: 180°
    - **Tilt Angle**: 35°
    - **Inverter Efficiency**: 96%
    - **Losses**: 0.1%
    - **DC to AC Ratio**: 1.1
- **Output Simulation Results**: Export detailed time-series PV capacity-factor data to CSV files for downstream optimization and analysis.
    

## Data Sources

- **Weather Data**: This project uses the MERRA-2 dataset to provide accurate and detailed environmental conditions for the simulations.

## Prerequisites

Ensure the following requirements are met before starting:

- Python 3.10+ installed.

## Installation

Install necessary dependencies with:


```
pip install -r requirements.txt
```

