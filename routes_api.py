from flask import Blueprint, request, jsonify
from models import Property
from lodgify_service import lodgify_service

api_bp = Blueprint('api', __name__)

@api_bp.route('/check-availability', methods=['POST'])
def check_availability():
    data = request.json
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    guests = data.get('guests', 1)

    if not start_date or not end_date:
        return jsonify({"error": "Dates required"}), 400

    # 1. Local Check: Find properties with enough capacity
    # We query our SQLite DB instead of a config file
    suitable_properties = Property.query.filter(Property.capacity >= guests).all()
    
    available_results = []
    
    # 2. External Check: Ask Lodgify if these specific properties are free
    for prop in suitable_properties:
        # We assume property.lodgify_id is what the API expects
        result = lodgify_service.check_availability(prop.lodgify_id, start_date, end_date)
        
        # Simple logic: if we get a result, we assume it's available (optimize later)
        if result:
            available_results.append({
                "id": prop.lodgify_id,
                "name": prop.name,
                "capacity": prop.capacity,
                "description": f"{prop.name} (Max {prop.capacity} guests)"
            })

    return jsonify({
        "available_properties": available_results,
        "count": len(available_results)
    })

@api_bp.route('/create-booking', methods=['POST'])
def create_booking():
    data = request.json
    # Basic validation
    if not data.get('property_id'):
        return jsonify({"error": "Property ID required"}), 400
        
    guest_info = {
        "name": data.get('guest_name'),
        "email": data.get('guest_email')
    }
    dates = {
        "start": data.get('start_date'),
        "end": data.get('end_date')
    }
    
    result = lodgify_service.create_booking(data.get('property_id'), guest_info, dates)
    
    if result:
        return jsonify({"status": "success", "booking": result})
    else:
        return jsonify({"status": "error", "message": "Booking failed"}), 500
