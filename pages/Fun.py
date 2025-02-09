 # Visualization
from sklearn.linear_model import LinearRegression
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from data.data import load_data 



carbon_emissions, annual_temp, ghg_emissions, data_iso, energy_subs, sea_level = load_data()
# data preparation
sea_level['Day'] = pd.to_datetime(sea_level['Day'])
sea_level['Year'] = sea_level['Day'].dt.year
average_sea_level_per_year = sea_level.groupby(['Entity', 'Year'])['Global sea level as an average of Church and White (2011) and UHSLC data'].mean().reset_index()
average_sea_level_per_year.rename(columns={'Global sea level as an average of Church and White (2011) and UHSLC data': 'average_sea_level'}, inplace=True)
merged = carbon_emissions.merge(annual_temp, on=['Entity', 'Year'], how='inner')
merged = merged.merge(average_sea_level_per_year, on=['Entity', 'Year'], how='left')  


def fun():
    st.title("🌍 Climate Timeline Projections")

    # Filter for World data
    world_data = merged[merged['Entity'] == 'World']
    world_data = world_data.dropna(subset=['Annual CO₂ emissions', 'Temperature anomaly'])

   # Models for all three indicators (all linear)
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
        fig_co2.update_layout(showlegend=False)
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
        fig_temp.update_layout(showlegend=False)
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
        fig_sl.update_layout(showlegend=False)
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