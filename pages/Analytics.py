import numpy as np
import pandas as pd
import streamlit as st
from data.data import load_data 
import plotly.graph_objects as go



carbon_emissions, annual_temp, ghg_emissions, data_iso, energy_subs, sea_level = load_data()

def compare_countries(country1, country2):
    # Filter the data for the selected countries
    country1_data = carbon_emissions[carbon_emissions['Entity'] == country1]
    country2_data = carbon_emissions[carbon_emissions['Entity'] == country2]

    # You can do this for other datasets as well, such as GHG emissions, temperature, etc.
    country1_temp = annual_temp[annual_temp['Entity'] == country1]
    country2_temp = annual_temp[annual_temp['Entity'] == country2]

    # Comparison: GHG Emissions
    country1_ghg = ghg_emissions[ghg_emissions['Entity'] == country1]
    country2_ghg = ghg_emissions[ghg_emissions['Entity'] == country2]

    comparison_data = {
        'country' : [country1, country2],
        'CO2 Emissions (MtCO2)': [
            country1_data['Annual CO₂ emissions'].sum(),
            country2_data['Annual CO₂ emissions'].sum()
        ],
          'GHG Emissions (ktCO₂e)': [
            country1_ghg['Annual CO₂ emissions'].sum(),
            country2_ghg['Annual CO₂ emissions'].sum()
        ],
          'Temperature Anomaly (°C)': [
            country1_temp['Temperature anomaly'].mean(),
            country2_temp['Temperature anomaly'].mean()
        ]
    }

    # Convert the dictionary into a DataFrame
    comparison_df = pd.DataFrame(comparison_data)

    return comparison_df
    
st.markdown(
    """
    <style>
    .streamlit-table {
        width: 100%; 
        height: 400px;
        margin-left: auto;
        margin-right: auto;
        
    }
    .stTable th, .stTable td {
        text-align: center !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def analytics():
    st.title("Comparision table")
    # Dropdowns for country selection
    country_list = carbon_emissions['Entity'].unique()  # Get unique countries from the dataset
    col = st.columns(2)
    with col[0]:
        country1 = st.selectbox("Select the first country", country_list)
    with col[1]:
        country2 = st.selectbox("Select the second country", country_list)

    # Run the comparison
    if country1 != country2:
        comparison_df = compare_countries(country1, country2)

        # Display the comparison results as a table
        st.subheader("Comparison Results")
        st.table(comparison_df)

    else:
        st.warning("Please select two different countries to compare.")

    # Title
    st.title("🌍 CO₂ Emissions and Temperature Rise Calculator")

    # Slider for CO2 emissions
    emissions = st.slider("Select CO₂ Emissions (GtCO₂)", min_value=0, max_value=3000, value=500, step=50)

    # Fixed or dynamically calculated values (adjust based on your data)
    TCR = 1.65  # Default average value from IPCC reports
    ECS = 3.0   # Default average ECS value

    # TCR Calculation
    TCR_temp_rise = (TCR / 1000) * emissions

    # ECS Calculation
    delta_C = 0.0577 * emissions            # Change in CO2 concentration
    current_CO2 = 420                        # Current CO2 ppm
    new_CO2 = current_CO2 + delta_C          # New CO2 ppm
    delta_F = 5.35 * np.log(new_CO2 / 280)   # Radiative forcing
    lambda_sensitivity = ECS / 3             # Adjusting lambda based on ECS
    ECS_temp_rise = lambda_sensitivity * delta_F

    # Display Results
    st.subheader("🌡️ Temperature Rise Estimates")
    st.write(f"**Transient (Short-Term) Warming:** {TCR_temp_rise:.2f} °C")
    st.write(f"**Equilibrium (Long-Term) Warming:** {ECS_temp_rise:.2f} °C")

    # Plotting with Plotly
    fig = go.Figure(data=[
        go.Bar(name='Transient Warming', x=['TCR'], y=[TCR_temp_rise], marker_color='skyblue'),
        go.Bar(name='Equilibrium Warming', x=['ECS'], y=[ECS_temp_rise], marker_color='salmon')
    ])

    # Customize layout
    fig.update_layout(
        title="🌡️ CO₂ Emissions Impact on Global Temperature",
        yaxis_title="Temperature Rise (°C)",
        barmode='group'
    )

    st.plotly_chart(fig)
