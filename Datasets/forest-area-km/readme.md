# Forest area - Data package

This data package contains the data that powers the chart ["Forest area"](https://ourworldindata.org/grapher/forest-area-km?v=1&csvType=full&useColumnShortNames=false) on the Our World in Data website. It was downloaded on February 06, 2025.

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


## Forest area
A forest is defined as Land spanning more than 0.5 hectares with trees higher than 5 meters and a canopy cover of more than 10 percent, or trees able to reach these thresholds in situ. It does not include land that is predominantly
under agricultural or urban land use.

Forest is determined both by the presence of trees and the absence of other predominant land uses. The trees
should be able to reach a minimum height of 5 meters in situ.
Unit conversion factor: 1000  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
UN Food and Agriculture Organization (FAO). Forest Resources Assessment. – processed by Our World in Data

#### Full citation
UN Food and Agriculture Organization (FAO). Forest Resources Assessment. – processed by Our World in Data. “Forest area” [dataset]. UN Food and Agriculture Organization (FAO). Forest Resources Assessment. [original data].
Source: UN Food and Agriculture Organization (FAO). Forest Resources Assessment. – processed by Our World In Data

### Additional information about this data
Raw data for forest area, deforestation, afforestation and expansion is sourced from the UN FAO Forest Resources Assessment.

Our World in Data have calculated several metrics based on this raw data including:
– Net change in forest area (afforestation minus deforestation)
– Net conversion rate (net change as a percentage of forest area)
– Each country's share of global forest area, deforestation, afforestation, and net change in forests
– Each country's share of regional forest area, deforestation, afforestation, and net change in forests

The UN FAO publish forest area and forest change data as the annual average on 10- or 5-year timescales. Therefore the following year allocation applies:
– 1990: the annual average over the period from 1990 to 2000.
– 2000: the annual average over the period from 2000 to 2010.
– 2010: the annual average over the period from 2010 to 2015.
– 2015: the annual average over the period from 2015 to 2020.

Data on forest cover by country pre-1990 is sourced from a variety sources which are documented here: https://docs.google.com/spreadsheets/d/1nYpao4e8Ai-P86jIUZ3r7X6-5MjZ7ZbG7TJQSO729Bg/edit?usp=sharing


    