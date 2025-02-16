# Annual temperature anomalies - Data package

This data package contains the data that powers the chart ["Annual temperature anomalies"](https://ourworldindata.org/grapher/annual-temperature-anomalies?v=1&csvType=full&useColumnShortNames=false) on the Our World in Data website. It was downloaded on January 12, 2025.

### Active Filters

A filtered subset of the full data was downloaded. The following filters were applied:

## CSV Structure

The high level structure of the CSV file is that each row is an observation for an entity (usually a country or region) and a timepoint (usually a year).

The first two columns in the CSV file are "Entity" and "Code". "Entity" is the name of the entity (e.g. "United States"). "Code" is the OWID internal entity code that we use if the entity is a country or region. For normal countries, this is the same as the [iso alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) code of the entity (e.g. "USA") - for non-standard countries like historical countries these are custom codes.

The third column is either "Year" or "Day". If the data is annual, this is "Year" and contains only the year as an integer. If the column is "Day", the column contains a date string in the form "YYYY-MM-DD".

The final column is the data column, which is the time series that powers the chart. If the CSV data is downloaded using the "full data" option, then the column corresponds to the time series below. If the CSV data is downloaded using the "only selected data visible in the chart" option then the data column is transformed depending on the chart type and thus the association with the time series might not be as straightforward.

## Metadata.json structure

The .metadata.json file contains metadata about the data package. The "charts" key contains information to recreate the chart, like the title, subtitle etc.. The "columns" key contains information about each of the columns in the csv, like the unit, timespan covered, citation for the data etc..

## About the data

Our World in Data is almost never the original producer of the data - almost all of the data we use has been compiled by others. If you want to re-use data, it is your responsibility to ensure that you adhere to the sources' license and to credit them correctly. Please note that a single time series may have more than one source - e.g. when we stich together data from different time periods by different producers or when we calculate per capita metrics using population data from a second source.

## Detailed information about the data


## Temperature anomaly
The deviation of a specific year's average surface temperature from the 1991-2020 mean, in degrees Celsius. The 2024 data is incomplete and was last updated 07 January 2025.
Last updated: January 7, 2025  
Date range: 1940–2024  
Unit: °C  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Contains modified Copernicus Climate Change Service information (2025) – with major processing by Our World in Data

#### Full citation
Contains modified Copernicus Climate Change Service information (2025) – with major processing by Our World in Data. “Temperature anomaly” [dataset]. Contains modified Copernicus Climate Change Service information, “ERA5 monthly averaged data on single levels from 1940 to present 2” [original data].
Source: Contains modified Copernicus Climate Change Service information (2025) – with major processing by Our World In Data

### Source

#### Contains modified Copernicus Climate Change Service information – ERA5 monthly averaged data on single levels from 1940 to present
Retrieved on: 2025-01-07  
Retrieved from: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-monthly-means?tab=overview  

#### Notes on our processing step for this indicator
- Temperature measured in kelvin was converted to degrees Celsius (°C) by subtracting 273.15.

- Initially, the temperature dataset is provided with specific coordinates in terms of longitude and latitude. To tailor this data to each country, we utilize geographical boundaries as defined by the World Bank. The method involves trimming the global temperature dataset to match the exact geographical shape of each country. To correct for potential distortions caused by the Earth's curvature on a flat map, we apply a latitude-based weighting. This step is essential for maintaining accuracy, especially in high-latitude regions where distortion is more pronounced. The result of this process is a latitude-weighted average temperature for each nation.

- It's important to note, however, that due to the resolution constraints of the Copernicus dataset, this methodology might not be as effective for countries with very small landmasses. In these cases, the process may not yield reliable data.

- The derived 2-meter temperature readings for each country are calculated based on administrative borders, encompassing all land surface types within these defined areas. As a result, temperatures over oceans and seas are not included in these averages, focusing the data primarily on terrestrial environments.

- Global temperature averages and anomalies are calculated over all land and ocean surfaces.
- The temperature anomaly is calculated by comparing the average surface temperature of a specific time period (e.g., a particular year or month) to the mean surface temperature of the same period from 1991 to 2020.

- When calculating anomalies for each country, the average surface temperature of a given year or month is compared to the 1991-2020 mean temperature for that specific country.

- The reason for using the 1991-2020 period as the reference mean is that it is the standard reference period used by our data source, the Copernicus Climate Change Service. This period is also adopted by the UK Met Office. This approach ensures consistency in identifying climate variations over time.


    