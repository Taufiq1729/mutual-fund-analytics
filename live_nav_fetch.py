import os
import requests
import pandas as pd

def ensure_directory():
    """Makes sure the raw data folder exists before saving files."""
    os.makedirs("data/raw", exist_ok=True)

def fetch_and_save_nav(scheme_code, filename):
    """
    Fetches daily NAV history from mfapi.in for a given scheme code 
    and saves it as a CSV file.
    """
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"Fetching data for scheme code: {scheme_code}...")
    
    try:
        response = requests.get(url, timeout=10)
        
        # Check if the website responded successfully (Status Code 200)
        if response.status_code == 200:
            json_data = response.json()
            
            # Extract the actual historical NAV data list from the JSON response
            if 'data' in json_data and len(json_data['data']) > 0:
                nav_history = json_data['data']
                
                # Convert the list of dicts into a clean Pandas DataFrame
                df = pd.DataFrame(nav_history)
                
                # Save to target raw data folder
                filepath = f"data/raw/{filename}.csv"
                df.to_csv(filepath, index=False)
                print(f"Successfully saved: {filepath} ({len(df)} rows found)\n")
            else:
                print(f"Warning: No historical data found for code {scheme_code}.\n")
        else:
            print(f"Failed to fetch code {scheme_code}. HTTP Status: {response.status_code}\n")
            
    except Exception as e:
        print(f"An error occurred while fetching code {scheme_code}: {e}\n")

def main():
    # Step 1: Ensure directory structure is ready
    ensure_directory()
    
    # Step 2: Fetch the single baseline requirement (HDFC Top 100 Direct)
    print("--- Starting Single Fund Fetch ---")
    fetch_and_save_nav(125497, "hdfc_top_100_live")
    
    # Step 3: Fetch the 5 key bluechip schemes using a loop
    print("--- Starting Bulk Bluechip Fund Fetch ---")
    bluechip_schemes = {
        "SBI_Bluechip": 119551,
        "ICICI_Bluechip": 120503,
        "Nippon_Large_Cap": 118632,
        "Axis_Bluechip": 119092,
        "Kotak_Bluechip": 120841
    }
    
    for name, code in bluechip_schemes.items():
        fetch_and_save_nav(code, f"{name}_live")
        
    print("All API data ingestion tasks completed!")

if __name__ == "__main__":
    main()