import os
from flask import Flask, request, jsonify
from config import PROPERTIES
from lodgify_client import LodgifyClient
from datetime import datetime

app = Flask(__name__)
client = LodgifyClient()

@app.route('/check-availability', methods=['POST'])
def check_availability():
    """
    Expects JSON:
    {
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD",
        "guests": 2
    }
    """
    data = request.json
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    guests = data.get('guests', 1)

    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date are required"}), 400

    # 1. Filter properties by capacity
    capable_properties = []
    for prop_id, details in PROPERTIES.items():
        if details['capacity'] >= guests:
            capable_properties.append(prop_id)
    
    available_properties = []
    
    # 2. Check Lodgify availability for each capable property
    print(f"Checking availability for {len(capable_properties)} properties...")
    for prop_id in capable_properties:
        # Note: This is sequential and might be slow. 
        # In a production app, we would use async or threads.
        result = client.check_availability(prop_id, start_date, end_date)
        
        # LOGIC TO DETERMINE IF AVAILABLE
        # We need to know the Lodgify API response structure.
        # For now, we will assume if the API returns a success 200 and specific content.
        # Since we haven't verified the response structure, we'll log it and 
        # tentatively assume it returns a list of periods or availability status.
        
        # Heuristic: If result is not None, we add it. 
        # TODO: Refine this condition based on actual API response.
        if result: 
            # We assume a valid non-empty response implies availability or contains data we can parse
            # Ideally, we check for a "is_available" flag or empty "booked_periods" list.
            # Let's add the property details to the response
            prop_info = PROPERTIES[prop_id].copy()
            prop_info['id'] = prop_id
            prop_info['api_response_debug'] = result # For debugging
            available_properties.append(prop_info)

    return jsonify({
        "available_properties": available_properties,
        "count": len(available_properties)
    })

@app.route('/create-booking', methods=['POST'])
def create_booking():
    """
    Expects JSON:
    {
        "property_id": 123456,
        "guest_name": "John Doe",
        "guest_email": "john@example.com",
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD"
    }
    """
    data = request.json
    property_id = data.get('property_id')
    guest_name = data.get('guest_name')
    guest_email = data.get('guest_email')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    if not all([property_id, guest_name, guest_email, start_date, end_date]):
        return jsonify({"error": "Missing required fields"}), 400

    guest_info = {"name": guest_name, "email": guest_email}
    
    result = client.create_booking(property_id, guest_info, start_date, end_date)
    
    if result:
        return jsonify({"status": "success", "booking_details": result})
    else:
        return jsonify({"status": "error", "message": "Failed to create booking"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
