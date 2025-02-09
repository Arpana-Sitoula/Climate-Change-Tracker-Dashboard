# load_data.py
import pandas as pd

def load_data():
    carbon_emissions = pd.read_csv(r"C:\Users\arpan\Desktop\datasets\annual-co2-emissions-per-country\annual-co2-emissions-per-country.csv")
    annual_temp = pd.read_csv(r"C:\Users\arpan\Desktop\datasets\annual-temperature-anomalies\annual-temperature-anomalies.csv")
    ghg_emissions = pd.read_csv(r"C:\Users\arpan\Desktop\datasets\ghg-emissions-by-gas\ghg-emissions-by-gas.csv")
    data_iso = pd.read_csv(r"C:\Users\arpan\Desktop\datasets\Global Primary Forest loss\iso_metadata.csv")
    energy_subs = pd.read_csv(r"C:\Users\arpan\Desktop\datasets\global-energy-substitution\global-energy-substitution.csv")
    sea_level = pd.read_csv(r"C:\Users\arpan\Desktop\datasets\sea-level\sea-level.csv")

    return carbon_emissions, annual_temp, ghg_emissions, data_iso, energy_subs, sea_level
