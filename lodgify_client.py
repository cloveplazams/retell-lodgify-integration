import requests
import datetime
from config import LODGIFY_API_KEY

BASE_URL = "https://api.lodgify.com/v1"

class LodgifyClient:
    def __init__(self):
        self.headers = {
            "X-ApiKey": LODGIFY_API_KEY,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def check_availability(self, property_id, start_date, end_date):
        """
        Check availability for a specific property.
        dates should be in 'YYYY-MM-DD' format.
        """
        url = f"{BASE_URL}/availability"
        params = {
            "propertyId": property_id,
            "arrival": start_date,
            "departure": end_date
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            # Lodgify availability API structure might vary, but generally returning the data 
            # or processing it to boolean is needed.
            # Assuming endpoint returns availability periods or status.
            # Use 'GET /v1/availability' or 'GET /v2/availability' depending on precise Lodgify docs.
            # A common pattern is querying calendar for the property.
            
            # For robustness, we might want to check the calendar endpoint for period
            # GET /v1/availability?propertyId=...&arrival=...&departure=...
            # If it returns 200 and says available, then true.
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Error checking availability for {property_id}: {e}")
            return None

    def get_property_availability(self, property_id, start_date, end_date):
        """
        More specific check using availability endpoint if needed.
        Start_date and end_date are datetime objects or strings YYYY-MM-DD.
        """
        # Alternative implementation using /v2/availability/check specific endpoint if it exists
        # Or iterating over the calendar. 
        # For now, let's assume the basic availability endpoint works as a filter.
        pass

    def create_booking(self, property_id, guest_info, arrival, departure):
        """
        Create a booking.
        guest_info: dict with name, email, etc.
        """
        url = f"{BASE_URL}/reservation"
        
        payload = {
            "property_id": property_id,
            "arrival": arrival,
            "departure": departure,
            "guest": {
                "name": guest_info.get("name"),
                "email": guest_info.get("email"),
                # Add other fields as required by Lodgify
            },
            "status": "Quote" # or 'Booked', 'Tentative'. Quote is safer for "tentative"
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating booking: {e}")
            if response is not None:
                print(response.text)
            return None
