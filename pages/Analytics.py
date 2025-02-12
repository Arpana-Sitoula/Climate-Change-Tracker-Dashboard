import numpy as np
import pandas as pd
import streamlit as st
from data.data import load_data 
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import plotly.express as px


carbon_emissions, annual_temp, ghg_emissions, data_iso, energy_subs, sea_level, disaster = load_data()
# Data preparation
total_disaster = pd.melt(disaster, id_vars=['ISO3'], var_name='Year', value_name='Disaster_Count')
total_disaster = total_disaster[total_disaster['Year'].str.isnumeric()]
total_disaster['Year'] = total_disaster['Year'].astype(int)
total_disaster['Disaster_Count'] = total_disaster['Disaster_Count'].fillna(0)
total_disaster.rename(columns={'ISO3': 'iso'}, inplace=True)
total_disaster = total_disaster.merge(data_iso, on='iso', how='left')
total_disaster.rename(columns={'name': 'Entity'}, inplace=True)

def compare_countries(country1, country2):
    # Filter the data for the selected countries
    country1_data = carbon_emissions[carbon_emissions['Entity'] == country1]
    country2_data = carbon_emissions[carbon_emissions['Entity'] == country2]

    country1_temp = annual_temp[annual_temp['Entity'] == country1]
    country2_temp = annual_temp[annual_temp['Entity'] == country2]

    country1_ghg = ghg_emissions[ghg_emissions['Entity'] == country1]
    country2_ghg = ghg_emissions[ghg_emissions['Entity'] == country2]

    country1_disaster = total_disaster[total_disaster['Entity'] == country1]
    country2_disaster = total_disaster[total_disaster['Entity'] == country2]


    # Get the latest year for temperature anomaly
    latest_year = max(annual_temp['Year'])
    temp1_latest = country1_temp[country1_temp['Year'] == latest_year]['Temperature anomaly'].values
    temp2_latest = country2_temp[country2_temp['Year'] == latest_year]['Temperature anomaly'].values

    temp1_latest = temp1_latest[0] if len(temp1_latest) > 0 else None
    temp2_latest = temp2_latest[0] if len(temp2_latest) > 0 else None

    disaster1_latest = country1_disaster[country1_disaster['Year'] == 2023]['Disaster_Count'].values
    disaster2_latest = country2_disaster[country2_disaster['Year'] == 2023]['Disaster_Count'].values

    disaster1_latest = disaster1_latest[0] if len(disaster1_latest) > 0 else None
    disaster2_latest = disaster2_latest[0] if len(disaster2_latest) > 0 else None
    # Calculate totals
    co2_1 = country1_data['Annual CO₂ emissions'].sum()
    co2_2 = country2_data['Annual CO₂ emissions'].sum()
    ghg_1 = country1_ghg['Annual CO₂ emissions'].sum()
    ghg_2 = country2_ghg['Annual CO₂ emissions'].sum()

    # Calculate percentage difference
    def percentage_diff(a, b):
        if a + b == 0:
            return 0
        return round((abs(a - b) / ((a + b) / 2)) * 100, 2)

    co2_diff = percentage_diff(co2_1, co2_2)
    ghg_diff = percentage_diff(ghg_1, ghg_2)


    # Comparison Data
    comparison_data = {
        'Country': [country1, country2],
        'CO2 Emissions (MtCO2)': [co2_1, co2_2],
        'CO2 % Difference': [f"{co2_diff}%", f"{co2_diff}%"],
        'GHG Emissions (ktCO₂e)': [ghg_1, ghg_2],
        'GHG % Difference': [f"{ghg_diff}%", f"{ghg_diff}%"],
        'Temperature Anomaly (°C)': [temp1_latest, temp2_latest],
        'Total Disaster' : [disaster1_latest, disaster2_latest],
    }

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

carbon_emissions, annual_temp, ghg_emissions, data_iso, energy_subs, sea_level, disaster = load_data()
# data preparation
sea_level['Day'] = pd.to_datetime(sea_level['Day'])
sea_level['Year'] = sea_level['Day'].dt.year
average_sea_level_per_year = sea_level.groupby(['Entity', 'Year'])['Global sea level as an average of Church and White (2011) and UHSLC data'].mean().reset_index()
average_sea_level_per_year.rename(columns={'Global sea level as an average of Church and White (2011) and UHSLC data': 'average_sea_level'}, inplace=True)
merged = carbon_emissions.merge(annual_temp, on=['Entity', 'Year'], how='inner')
merged = merged.merge(average_sea_level_per_year, on=['Entity', 'Year'], how='left') 

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
    
    tab1, tab2 = st.tabs(["Calculator", "Predictive Model"])
    # Title
    with tab1:
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

    with tab2:
        st.title("Timeline Projections")

        # Filter for World data
        world_data = merged[merged['Entity'] == 'World']
        world_data = world_data.dropna(subset=['Annual CO₂ emissions', 'Temperature anomaly'])

        # --------------------------------------------
        # CO2 Model
        X = world_data[['Year']]
        y_co2 = world_data['Annual CO₂ emissions']
        co2_model = LinearRegression().fit(X, y_co2)

        # Temperature Model
        y_temp = world_data['Temperature anomaly']
        temp_model = LinearRegression().fit(X, y_temp)

        # Sea Level Model (use non-missing sea level data)
        world_data_sea = world_data.dropna(subset=['average_sea_level'])
        X_sl = world_data_sea[['Year']]
        y_sl = world_data_sea['average_sea_level']
        sl_model = LinearRegression().fit(X_sl, y_sl)

        # Timeline for projections
        min_year = 1850
        max_year = 2100
        all_years = pd.DataFrame({'Year': np.arange(min_year, max_year + 1)})

        # Predictions
        all_years['CO2'] = co2_model.predict(all_years[['Year']])
        all_years['Temp'] = temp_model.predict(all_years[['Year']])
        all_years['SeaLevel'] = sl_model.predict(all_years[['Year']])

        # Merge historical and projected data
        historical = world_data[['Year', 'Annual CO₂ emissions', 'Temperature anomaly', 'average_sea_level']]
        historical = historical.rename(columns={
            'Annual CO₂ emissions': 'CO2',
            'Temperature anomaly': 'Temp',
            'average_sea_level': 'SeaLevel'
        })

        # Fill missing sea level data with linear predictions
        predicted_sea_levels = pd.Series(
            sl_model.predict(historical[['Year']]), 
            index=historical.index
        )
        historical['SeaLevel'].fillna(predicted_sea_levels, inplace=True)

        full_timeline = pd.concat([historical, all_years[~all_years['Year'].isin(historical['Year'])]])

        # Time slider
        selected_year = st.slider('Select Year', min_year, max_year, 2023)
        current_data = full_timeline[full_timeline['Year'] == selected_year].iloc[0]
        year_2100_data = all_years[all_years['Year'] == 2100].iloc[0]

         # Calculate dynamic y-axis ranges
        co2_min = historical['CO2'].min()  # Historical minimum
        co2_max = year_2100_data['CO2']    # Projected 2100 value

        temp_min = historical['Temp'].min()
        temp_max = year_2100_data['Temp']

        sl_min = historical['SeaLevel'].min()
        sl_max = year_2100_data['SeaLevel']

        # Create three columns for the bar plots
        col1, col2, col3 = st.columns(3)

        # ----------------------------------------------------------
        # CO2 Emissions Plot (Metric Tons)
        # ----------------------------------------------------------
        with col1:
            fig_co2 = px.bar(
                x=['CO₂ Emissions'],
                y=[current_data['CO2']],
                labels={'x': '', 'y': 'Metric Tons (Mt)'},
                title='CO₂ Emissions',
                color_discrete_sequence=['#636EFA'],
                text_auto='.2s'  # Format text on bars
            )
            fig_co2.update_layout(
            showlegend=False,
            yaxis_range=[co2_min, co2_max * 1.05]  # Add 5% padding for readability
            )
            st.plotly_chart(fig_co2, use_container_width=True)

        # ----------------------------------------------------------
        # Temperature Anomaly Plot (°C)
        # ----------------------------------------------------------
        with col2:
            fig_temp = px.bar(
                x=['Temperature Anomaly'],
                y=[current_data['Temp']],
                labels={'x': '', 'y': 'Temperature Anomaly (°C)'},
                title='Temperature',
                color_discrete_sequence=['#EF553B'],
                text_auto='.2f'  # Show 2 decimal places
            )
            fig_temp.update_layout(
            showlegend=False,
            yaxis_range=[temp_min, temp_max * 1.05]
            )
            st.plotly_chart(fig_temp, use_container_width=True)


        # ----------------------------------------------------------
        # Sea Level Plot (mm)
        # ----------------------------------------------------------
        with col3:
            fig_sl = px.bar(
                x=['Sea Level'],
                y=[current_data['SeaLevel']],
                labels={'x': '', 'y': 'Sea Level (mm)'},
                title='Sea Level',
                color_discrete_sequence=['#00CC96'],
                text_auto='.2f'  # Show 2 decimal places
            )
            fig_sl.update_layout(
            showlegend=False,
            yaxis_range=[sl_min, sl_max * 1.05]
            )
            st.plotly_chart(fig_sl, use_container_width=True)

        # ----------------------------------------------------------
        # Debug Plot (Historical Trends with Multiple Y-Axes)
        # ----------------------------------------------------------
        fig_debug = go.Figure()

        # CO2 Emissions (Left Y-Axis)
        fig_debug.add_trace(
            go.Scatter(
                x=world_data['Year'],
                y=world_data['Annual CO₂ emissions'],
                name='CO₂ Emissions (Mt)',
                line=dict(color='#636EFA')
            )
        )

        # Temperature Anomaly (Right Y-Axis)
        fig_debug.add_trace(
            go.Scatter(
                x=world_data['Year'],
                y=world_data['Temperature anomaly'],
                name='Temperature Anomaly (°C)',
                line=dict(color='#EF553B'),
                yaxis='y2'
            )
        )

        # Sea Level (Third Y-Axis)
        fig_debug.add_trace(
            go.Scatter(
                x=world_data.dropna(subset=['average_sea_level'])['Year'],
                y=world_data.dropna(subset=['average_sea_level'])['average_sea_level'],
                name='Sea Level (mm)',
                line=dict(color='#00CC96'),
                yaxis='y3'
            )
        )

        # Configure axes and layout
        fig_debug.update_layout(
            title='Historical Trends',
            xaxis=dict(title='Year'),
            yaxis=dict(title='CO₂ Emissions (Mt)', color='#636EFA'),
            yaxis2=dict(
                title='Temperature Anomaly (°C)',
                color='#EF553B',
                overlaying='y',
                side='right'
            ),
            yaxis3=dict(
                title='Sea Level (mm)',
                color='#00CC96',
                overlaying='y',
                side='right',
                position=0.95  # Adjust position to avoid overlap
            )
        )

        st.plotly_chart(fig_debug, use_container_width=True)