import requests
import json
import pandas as pd
from datetime import datetime
import os
import time

# Get API key from environment variable
API_KEY = os.environ.get('26683874f80593e0924102f73c6529a208fd8f56')

# JCDecaux API endpoint for station information
API_URL = "https://api.jcdecaux.com/vls/v1/stations"

def fetch_data():
    """Fetch current bike station data from JCDecaux API"""
    #params = {
     #   'apiKey': API_KEY,
      #  'contract': 'Dublin'  # Replace with your city (e.g., 'paris', 'lyon', etc.)
    #}
    NAME = "Dublin"
    STATIONS = "https://api.jcdecaux.com/vls/v1/stations"
    APIKEY = "26683874f80593e0924102f73c6529a208fd8f56"

    response = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=" + NAME + "&apiKey=" + APIKEY)
    #response = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract={'dublin'}&apiKey={26683874f80593e0924102f73c6529a208fd8f56}")

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def save_data(data):
    """Save the data to CSV file with timestamp"""
    if not data:
        return
    
    # Create timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Convert to DataFrame
    df = pd.json_normalize(data)
    print(df)
    # Save raw JSON as backup
    with open(f"data/raw/stations_{timestamp}.json", "w") as f:
        json.dump(data, f)
    
    # Save processed data as CSV
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(f"data/processed/stations_{timestamp}.csv", index=False)
    
    # Also update a "latest" file for easy access
    df.to_csv("data/processed/stations_latest.csv", index=False)
    
    print(f"Data saved: {len(df)} stations at {timestamp}")

def main():
    # Create data directories if they don't exist
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    
    # Fetch and save data
    data = fetch_data()
    save_data(data)

if __name__ == "__main__":
    main()
