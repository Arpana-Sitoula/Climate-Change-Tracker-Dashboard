import streamlit as st
import pandas as pd
import plotly.express as px
from functions.donut import make_donut
from data.data import load_data 



#load data
carbon_emissions, annual_temp, ghg_emissions, data_iso, energy_subs, sea_level, disaster = load_data()

# Data preparation
total_disaster = pd.melt(disaster, id_vars=['ISO3'], var_name='Year', value_name='Disaster_Count')
total_disaster = total_disaster[total_disaster['Year'].str.isnumeric()]
total_disaster['Year'] = total_disaster['Year'].astype(int)
total_disaster['Disaster_Count'] = total_disaster['Disaster_Count'].fillna(0)
total_disaster.rename(columns={'ISO3': 'iso'}, inplace=True)
total_disaster = total_disaster.merge(data_iso, on='iso', how='left')
total_disaster.rename(columns={'name': 'Entity'}, inplace=True)


# Main Streamlit app

datasets = {
    "Annual CO2 Emissions": carbon_emissions,
    "Annual Temperature Anomalies": annual_temp,
    "GHG Emissions by Gas": ghg_emissions,
    "Disaster caused by Climate Change": total_disaster,
   
}

color_mapping = {
    "Annual CO2 Emissions": "Annual CO₂ emissions",
    "Annual Temperature Anomalies": "Temperature anomaly",
    "GHG Emissions by Gas": "Annual CO₂ emissions", 
    "Disaster Caused by Climate Change": "Disaster_Count",
}


# Calculations
# surface temperature increment calculations
world_temp = annual_temp[annual_temp['Entity']== 'World']
last_decade_temp = world_temp[(world_temp['Year'] >= 2014) & (world_temp['Year'] <= 2024)]
# Calculate percentage increase and absolute increment
start_temp = last_decade_temp['Temperature anomaly'].iloc[0]
end_temp = last_decade_temp['Temperature anomaly'].iloc[-1]
absolute_increment = end_temp - start_temp
percentage_increment = (absolute_increment / start_temp) * 100

# green house gases emissions
world_ghg = ghg_emissions[ghg_emissions['Entity']== 'World']
last_decade_ghg = world_ghg[(world_ghg['Year'] >= 2013) & (world_ghg['Year'] <= 2023)]
start_no2 = last_decade_ghg['Annual nitrous oxide emissions in CO₂ equivalents'].iloc[0]
end_no2 = last_decade_ghg['Annual nitrous oxide emissions in CO₂ equivalents'].iloc[-1]
start_nh3 = last_decade_ghg['Annual methane emissions in CO₂ equivalents'].iloc[0]
end_nh3 = last_decade_ghg['Annual methane emissions in CO₂ equivalents'].iloc[-1]
inc_no2 = end_no2 - start_no2
inc_nh3 = end_nh3 - start_nh3
percentage_no2 = (inc_no2 / start_no2) * 100
percentage_nh3 = (inc_nh3/ start_nh3) * 100




#sealevel data preparation
sea_level['Day'] = pd.to_datetime(sea_level['Day'])
sea_level = sea_level.sort_values(by='Day')
# Filter data for the last 5 years
last_date = sea_level['Day'].max()
five_years_ago = last_date - pd.DateOffset(years=5)
last_five_years_data = sea_level[sea_level['Day'] >= five_years_ago]
    # Get the earliest and latest values for 'Global sea level'
earliest_value = last_five_years_data['Global sea level as an average of Church and White (2011) and UHSLC data'].iloc[0]
latest_value = last_five_years_data['Global sea level as an average of Church and White (2011) and UHSLC data'].iloc[-1]
    # Calculate the total rise in mm and the percentage change
total_sea_rise_mm = latest_value - earliest_value
sea_level_percentage_change = (total_sea_rise_mm / earliest_value) * 100

#Energy calculations and data preparation
energy_subs = energy_subs.drop(['Entity', 'Code'], axis=1)
energy_subs.columns = [col.split('(')[0].strip() for col in energy_subs.columns]
    # Define renewable and non-renewable energy sources
renewable_sources = ['Solar', 'Wind', 'Hydropower', 'Other renewables', 'Biofuels', 'Traditional biomass']
non_renewable_sources = ['Nuclear', 'Gas', 'Oil', 'Coal']
    # Filter the data for the last half decade (e.g., from 2018 to 2022)
last_decade_data = energy_subs[energy_subs['Year'].between(2018, 2022)]
last_decade_data = energy_subs[energy_subs['Year'].between(2018, 2022)].copy()  # Make a copy of the slice
last_decade_data.loc[:, 'Renewable Energy Total'] = last_decade_data[renewable_sources].sum(axis=1)
last_decade_data.loc[:, 'Non-Renewable Energy Total'] = last_decade_data[non_renewable_sources].sum(axis=1)
renewable_2018 = last_decade_data[last_decade_data['Year'] == 2018]['Renewable Energy Total'].values[0]
renewable_2022 = last_decade_data[last_decade_data['Year'] == 2022]['Renewable Energy Total'].values[0]
non_renewable_2018 = last_decade_data[last_decade_data['Year'] == 2018]['Non-Renewable Energy Total'].values[0]
non_renewable_2022 = last_decade_data[last_decade_data['Year'] == 2022]['Non-Renewable Energy Total'].values[0]

# Calculate the percentage change for renewable and non-renewable energy
renewable_percentage_change = ((renewable_2022 - renewable_2018) / renewable_2018) * 100
non_renewable_percentage_change = ((non_renewable_2022 - non_renewable_2018) / non_renewable_2018) * 100



# Main Page Layout

#st.markdown("## Climate Change Tracker Dashboard")
# Columns Layout
def dash():
    col = st.columns((1.6,0.1, 6.3), gap='small')

    # Column 1
    with col[0]:
        
        
        # Surface Temperature Increment
        with st.container():
            st.metric(
                label="Global Surface Temperature (2014 - 2024)", 
                value=f"{absolute_increment:.2f}°C", 
                delta=f"{percentage_increment:.2f}%", 
                delta_color="inverse"
            )
        
        st.divider()
        st.markdown('#### Greenhouse Gas Emissions (Last Decade)')
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="(NO₂)",
                value=f"↑{percentage_no2:.1f} %",
                delta_color="inverse"
            )
        with col2:
            st.metric(
                label="(NH₃)",
                value=f"↑{percentage_nh3:.1f}%",
                delta_color="inverse"
            )

        st.divider()
        
        # Sea Level Rise
        st.metric(
            label="🌊 Sea Level Rise (Last 5 Years)", 
            value=f"{total_sea_rise_mm:.2f} mm", 
            delta=f"{sea_level_percentage_change:.2f}%"
        )

        st.divider()

        # Custom CSS for left alignment
        st.markdown(
        """
        <style>
        .left-align {
            display: flex;
            justify-content: flex-start;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
        
        # Donut Charts for Energy
        st.markdown('#### ⚡Energy Changes (2018 - 2022)')
        renewable_donut = make_donut(renewable_percentage_change, "Renewable Energy", "green")
        non_renewable_donut = make_donut(non_renewable_percentage_change, "Non-Renewable Energy", "red")

        with st.container():
            st.markdown('<div class="left-align">', unsafe_allow_html=True)
            st.write("**Renewable Energy Change**")
            st.altair_chart(renewable_donut, use_container_width=False)
            st.markdown('</div>', unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="left-align">', unsafe_allow_html=True)
            st.write("**Non-Renewable Energy Change**")
            st.altair_chart(non_renewable_donut, use_container_width=False)
            st.markdown('</div>', unsafe_allow_html=True)
        
        


    with col[1]:
        st.markdown(
            """
            <div style="border-left: 2px solid gray; height: 1500px; margin: auto;"></div>
            """,
            unsafe_allow_html=True
        )

    with col[2]:
        col1, col2 = st.columns(2)
        with col1:
            st.write('Sea level rise trend')
            st.line_chart(sea_level.set_index('Day')['Global sea level as an average of Church and White (2011) and UHSLC data'], height=500)

        with col2:
            # Option to Select Chart Type (Horizontal)
            chart_type = st.radio("Energy type classification", ('Bar Chart', 'Line Chart'), horizontal=True)

            if chart_type == 'Bar Chart':
                # Dropdown for Year Selection
                years = energy_subs['Year'].unique()
                latest_year = years[-1]  # Get the most recent year

                # Convert years to a list to use .index()
                years_list = list(years)
                selected_year = st.selectbox('Select Year:', years_list, index=years_list.index(latest_year))

                # Filter Data for Selected Year
                year_data = energy_subs[energy_subs['Year'] == selected_year].set_index('Year').transpose()
                year_data = year_data.reset_index()
                year_data.columns = ['Energy Source', 'Energy (TWh)']

                # Bar Chart
                fig = px.bar(
                    year_data,
                    x='Energy Source',
                    y='Energy (TWh)',
                    title=f'Energy Substitution in {selected_year} (TWh)',
                    color='Energy (TWh)',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig, use_container_width=True)

            else:
                # Line Chart (Across All Years)
                line_data = energy_subs.set_index('Year').transpose()
                line_data = line_data.reset_index().melt(id_vars='index', var_name='Year', value_name='Energy (TWh)')
                line_data.rename(columns={'index': 'Energy Source'}, inplace=True)

                # Line Chart
                fig = px.line(
                    line_data,
                    x='Year',
                    y='Energy (TWh)',
                    color='Energy Source',
                    title='Energy Substitution Over the Years',
                    markers=False,
                    height=500
                )
                fig.update_layout(
                legend=dict(
                title="Energy Source", 
                tracegroupgap=10  
            )
    )
                st.plotly_chart(fig)
        # Dropdown to choose the dataset (for example: CO2 emissions, temperature anomalies)
        dataset_choice = st.selectbox(
                "Select Dataset to Visualize",
                ["Annual CO2 Emissions", "Annual Temperature Anomalies", "GHG Emissions by Gas","Disaster Caused by Climate Change"]
            )
            
        # Filter your data based on the dataset choice (use corresponding DataFrame for selected dataset)
        if dataset_choice == "Annual CO2 Emissions":
            data_to_plot = carbon_emissions  # Use CO2 emissions dataset here
        elif dataset_choice == "Annual Temperature Anomalies":
            data_to_plot = annual_temp  # Use temperature anomaly dataset
        elif dataset_choice == "GHG Emissions by Gas":
            data_to_plot = ghg_emissions  # Use GHG emissions dataset
        elif dataset_choice == "Disaster Caused by Climate Change":
            data_to_plot = total_disaster # Use disaster dataset
        else:
            data_to_plot = pd.DataFrame()


        st.markdown("")
        st.markdown(f"#### {dataset_choice} by Country")
        
        
        # Get the year slider
        year_slider = st.slider(
            "Select Year",
            min_value=int(data_to_plot["Year"].min()),
            max_value=int(data_to_plot["Year"].max()),
            value=int(data_to_plot["Year"].max()),  # Default to the latest year
            step=1
        )

        # Filter data by the selected year
        selected_year_data = data_to_plot[data_to_plot["Year"] == year_slider]

        # Retrieve the column name for the selected dataset from the mapping
        color_column = color_mapping.get(dataset_choice, None)
        # Map Visualization (Choropleth map)
        lower_bound = data_to_plot[color_column].quantile(0.05)
        upper_bound = data_to_plot[color_column].quantile(0.95)
        
        fig = px.choropleth(
        selected_year_data,
        locations="Entity",
        locationmode="country names",
        color=color_column,
        range_color=[lower_bound, upper_bound],  
        animation_frame="Year",  
        color_continuous_scale="RdBu_r",
        title=f"{dataset_choice} for {year_slider}",
        labels={"Annual CO₂ emissions": "CO₂ Emissions (Tons)", "Temperature anomaly":"Temperature(°C)","Disaster caused by Climate Change":"Disaster Count"},
        height=800

        )
            
        st.plotly_chart(fig)
