import requests
from config import LODGIFY_API_KEY

BASE_URL = "https://api.lodgify.com/v1"

class LodgifyService:
    def __init__(self):
        self.headers = {
            "X-ApiKey": LODGIFY_API_KEY,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def check_availability(self, property_id, start_date, end_date):
        url = f"{BASE_URL}/availability"
        params = {
            "propertyId": property_id,
            "arrival": start_date,
            "departure": end_date
        }
        try:
            response = requests.get(url, headers=self.headers, params=params)
            # If 200, it implies some level of success/availability logic
            # We assume for now that a successful response means we can check details.
            # Real integration often requires parsing the specific availability object.
            # For simplicity, if it returns 200 and no error, we consider it 'available'
            # or return the raw data for the caller to decide.
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error checking availability: {e}")
            return None

    def create_booking(self, property_id, guest, dates):
        url = f"{BASE_URL}/reservation"
        payload = {
            "property_id": property_id,
            "arrival": dates['start'],
            "departure": dates['end'],
            "guest": guest, # {name, email}
            "status": "Quote" 
        }
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"Booking failed: {response.text}")
                return None
        except Exception as e:
            print(f"Error creating booking: {e}")
            return None

lodgify_service = LodgifyService()
