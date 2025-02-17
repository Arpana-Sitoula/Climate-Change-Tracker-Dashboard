import pandas as pd
import os

def load_data():
    # Go up one level and resolve to the absolute path of 'Datasets'
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', 'Datasets'))

    # Now, use this base path to reference the datasets
    carbon_emissions = pd.read_csv(os.path.join(base_path, "annual-co2-emissions-per-country/annual-co2-emissions-per-country.csv"))
    annual_temp = pd.read_csv(os.path.join(base_path, "annual-temperature-anomalies/annual-temperature-anomalies.csv"))
    ghg_emissions = pd.read_csv(os.path.join(base_path, "ghg-emissions-by-gas/ghg-emissions-by-gas.csv"))
    data_iso = pd.read_csv(os.path.join(base_path, "Global Primary Forest loss/iso_metadata.csv"))
    energy_subs = pd.read_csv(os.path.join(base_path, "global-energy-substitution/global-energy-substitution.csv"))
    sea_level = pd.read_csv(os.path.join(base_path, "sea-level/sea-level.csv"))
    disaster = pd.read_csv(os.path.join(base_path, "disaster.csv"))

    return carbon_emissions, annual_temp, ghg_emissions, data_iso, energy_subs, sea_level, disaster
