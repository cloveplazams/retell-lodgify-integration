import requests
from config import LODGIFY_API_KEY, PROPERTIES

BASE_URL = "https://api.lodgify.com/v1"
HEADERS = {
    "X-ApiKey": LODGIFY_API_KEY,
    "Accept": "application/json"
}

def test_connection():
    print("Testing Lodgify API Connection...")
    
    # Test 1: Get single property details (to verify key and property ID)
    test_property_id = list(PROPERTIES.keys())[0]
    print(f"\nFetching details for Property ID: {test_property_id}")
    
    url = f"{BASE_URL}/properties/{test_property_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Success! Property details:")
            # Print only keys to avoid flooding console
            print(response.json().keys())
        else:
            print("Failed to get property details.")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

    # Test 2: Check Availability
    print(f"\nChecking Availability for Property ID: {test_property_id}")
    # Using a date range in the future
    import datetime
    start_date = (datetime.date.today() + datetime.timedelta(days=30)).isoformat()
    end_date = (datetime.date.today() + datetime.timedelta(days=35)).isoformat()
    
    url = f"{BASE_URL}/availability"
    params = {
        "propertyId": test_property_id,
        "arrival": start_date,
        "departure": end_date
    }
    
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        print(f"Status Code: {response.status_code}")
        print("Response:", response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connection()
