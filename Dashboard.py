import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

#Page configuration
st.set_page_config(
    page_title="Climate Change Tracker Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


#Loading the data
carbon_emissions = pd.read_csv(r"C:\Users\arpan\Desktop\datasets\annual-co2-emissions-per-country\annual-co2-emissions-per-country.csv")
annual_temp = pd.read_csv(r"C:\Users\arpan\Desktop\datasets\annual-temperature-anomalies\annual-temperature-anomalies.csv")
ghg_emissions = pd.read_csv(r"C:\Users\arpan\Desktop\datasets\ghg-emissions-by-gas\ghg-emissions-by-gas.csv")
treecover = pd.read_csv(r"C:\Users\arpan\Desktop\datasets\Global Primary Forest loss\treecover_extent_2000_in_primary_forests_2001_tropics_only__ha.csv")
treeloss = pd.read_csv(r"C:\Users\arpan\Desktop\datasets\Global Primary Forest loss\treecover_loss_in_primary_forests_2001_tropics_only__ha.csv")
treecover_loss = pd.read_csv(r"C:\Users\arpan\Desktop\datasets\Global Primary Forest loss\treecover_loss__ha.csv")
data_iso = pd.read_csv(r"C:\Users\arpan\Desktop\datasets\Global Primary Forest loss\iso_metadata.csv")
energy_subs = pd.read_csv(r"C:\Users\arpan\Desktop\datasets\global-energy-substitution\global-energy-substitution.csv")
sea_level = pd.read_csv(r"C:\Users\arpan\Desktop\datasets\sea-level\sea-level.csv")


# Functions
# Define the donut chart function
def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response:.1f} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text



# Main Streamlit app

datasets = {
    "Annual CO2 Emissions": carbon_emissions,
    "Annual Temperature Anomalies": annual_temp,
    "GHG Emissions by Gas": ghg_emissions,
    "Deforestation" : treecover_loss
}

color_mapping = {
    "Annual CO2 Emissions": "Annual CO₂ emissions",
    "Annual Temperature Anomalies": "Temperature anomaly",
    "GHG Emissions by Gas": "Annual CO₂ emissions", 
    "Deforestation":"umd_tree_cover_loss__ha"
}


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


#deforestation calulations
treecover_loss = treecover_loss.merge(data_iso[['iso', 'name']], on="iso", how="left")
treecover_loss.rename(columns={"name": "Entity"}, inplace=True)
treecover_loss.rename(columns={"umd_tree_cover_loss__year":"Year"}, inplace=True)
treecover = treecover.merge(data_iso, on="iso", how="left")
treecover.rename(columns={"name": "Entity"}, inplace=True)
treecover['Tree_Cover_Percentage_2000'] = (treecover['umd_tree_cover_extent_2000__ha'] / treecover['area__ha']) * 100
treecover = treecover[['Entity', 'Tree_Cover_Percentage_2000']]
percentage_of_tree_2000 = treecover['Tree_Cover_Percentage_2000']

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
energy_subs.columns = [col.split('(')[0].strip() for col in energy_subs.columns]
    # Define renewable and non-renewable energy sources
renewable_sources = ['Solar', 'Wind', 'Hydropower', 'Other renewables', 'Biofuels', 'Traditional biomass']
non_renewable_sources = ['Nuclear', 'Gas', 'Oil', 'Coal']
    # Filter the data for the last decade (e.g., from 2012 to 2022)
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


# Main Page
col = st.columns((2, 6), gap='medium')
# Column 1
with col[0]:
    # Surface Temperature Increment
    st.metric(label="Global Surface Temperature (2014 - 2024)", value=f"{absolute_increment:.2f}°C", delta=f"{percentage_increment:.2f}%", delta_color="inverse")
    
    
    st.markdown('Green house gases emissions last decade')
    col1, col2 = st.columns(2)
    # For Nitrous Oxide (NO2)
    with col1:
        st.metric(
            label="Increment (NO2)",
            value=f"{percentage_no2:.2f}%",
            delta_color="inverse"
        )
    
    # For Methane (NH3)
    with col2:
        st.metric(
            label="Increment (NH3)",
            value=f"{percentage_nh3:.2f}%",
            delta_color="inverse"
        )
    st.metric(label="Sea level rise last 5 year", value=f"{total_sea_rise_mm:.2f}mm", delta=f"{sea_level_percentage_change:.2f}%")
    # Create Donut Charts
    renewable_donut = make_donut(renewable_percentage_change, "Renewable Energy", "green")
    non_renewable_donut = make_donut(non_renewable_percentage_change, "Non-Renewable Energy", "red")

    st.write("Renewable Energy Change")
    st.altair_chart(renewable_donut,use_container_width=True)
    st.write("Non-Renewable Energy Change")
    st.altair_chart(non_renewable_donut,use_container_width=True)

    
with col[1]:
      
    col1, col2 = st.columns(2)
    with col1: 
        st.write('Sea level rise trend')
        st.line_chart(sea_level.set_index('Day')['Global sea level as an average of Church and White (2011) and UHSLC data'])
        # Dropdown to choose the dataset (for example: CO2 emissions, temperature anomalies)
        dataset_choice = st.selectbox(
            "Select Dataset to Visualize",
            ["Annual CO2 Emissions", "Annual Temperature Anomalies", "GHG Emissions by Gas", "Deforestation rate"]
        )
        # Filter your data based on the dataset choice (use corresponding DataFrame for selected dataset)
        if dataset_choice == "Annual CO2 Emissions":
            data_to_plot = carbon_emissions  # Use CO2 emissions dataset here
        elif dataset_choice == "Annual Temperature Anomalies":
            data_to_plot = annual_temp  # Use temperature anomaly dataset
        elif dataset_choice == "GHG Emissions by Gas":
            data_to_plot = ghg_emissions  # Use GHG emissions dataset
        elif dataset_choice == "Deforestation rate":
            data_to_plot = treecover_loss
    with col2: 
        st.write('Energy type classification')
        



    st.markdown(f"#### {dataset_choice} by Country (Interactive Map)")
    
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
    if datasets == "Deforestation rate":
        fig = px.choropleth(
        selected_year_data,
        locations="Entity",
        locationmode="country names",
        color="Remaining_Tree_Cover_Percentage",
        color_continuous_scale="greens",
        labels={"Remaining_Tree_Cover_Percentage": "Remaining Tree Cover (%)"},
        title="Global Deforestation Map",
        )
    else:
        fig = px.choropleth(
        selected_year_data,
        locations="Entity",
        locationmode="country names",
        color=color_column,  # Or other relevant column based on dataset
        color_continuous_scale="reds",
        title=f"{dataset_choice} for {year_slider}",
        labels={"Annual CO₂ emissions": "CO₂ Emissions (Tons)", "Temperature anomaly":"Temperature(°C)"},
    )
         
    st.plotly_chart(fig)
