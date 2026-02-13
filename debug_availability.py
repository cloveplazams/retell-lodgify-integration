import requests
from config import LODGIFY_API_KEY, PROPERTIES
import datetime
import json

BASE_URL = "https://api.lodgify.com/v1"
HEADERS = {
    "X-ApiKey": LODGIFY_API_KEY,
    "Accept": "application/json"
}

def debug_availability():
    print("--- DEBUG AVAILABILITY ---")
    
    # Pick the first property
    if not PROPERTIES:
        print("No properties defined in config.py")
        return

    prop_id = list(PROPERTIES.keys())[0]
    print(f"Testing Property ID: {prop_id}")
    
    # Dates: Next month
    start_date = (datetime.date.today() + datetime.timedelta(days=30)).isoformat()
    end_date = (datetime.date.today() + datetime.timedelta(days=35)).isoformat()
    
    print(f"Checking dates: {start_date} to {end_date}")
    
    url = f"{BASE_URL}/availability"
    params = {
        "propertyId": prop_id,
        "arrival": start_date,
        "departure": end_date
    }
    
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        print(f"Response Status: {response.status_code}")
        
        try:
            data = response.json()
            print("Response JSON:")
            print(json.dumps(data, indent=2))
        except:
            print("Response Text (Not JSON):")
            print(response.text)
            
    except Exception as e:
        print(f"Request Error: {e}")

if __name__ == "__main__":
    debug_availability()
