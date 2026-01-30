from flask import Flask, request, jsonify
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# --------------------------------
# MOCK FLIGHT DATABASE
# --------------------------------

MOCK_FLIGHTS = [
    {
        "flight_id": "AI101",
        "airline": "Air India",
        "route": {"source": "HYD", "destination": "DEL"},
        "date": "2026-02-10",
        "timings": {"departure": "08:30", "arrival": "10:45", "duration": "2h 15m"},
        "pricing": {"amount": 5200, "currency": "INR"},
        "baggage": {"cabin": "7 Kg", "checkin": "15 Kg"},
        "seats_available": 12,
        "fare_rules": "Non-refundable",
        "policies": {"cancellation": "₹2000 fee", "reschedule": "₹1500 fee"}
    },
    {
        "flight_id": "IN202",
        "airline": "Indigo",
        "route": {"source": "HYD", "destination": "DEL"},
        "date": "2026-02-10",
        "timings": {"departure": "14:00", "arrival": "16:10", "duration": "2h 10m"},
        "pricing": {"amount": 4800, "currency": "INR"},
        "baggage": {"cabin": "7 Kg", "checkin": "20 Kg"},
        "seats_available": 5,
        "fare_rules": "Partially refundable",
        "policies": {"cancellation": "₹1500 fee", "reschedule": "₹1000 fee"}
    }
]

# --------------------------------
# MOCK CUSTOMER PREFERENCES DB
# --------------------------------

MOCK_CUSTOMERS = [
    {
        "email": "rahul@gmail.com",
        "name": "Rahul Sharma",
        "preferences": {
            "preferred_airline": "Indigo",
            "seat_type": "Window",
            "meal": "Veg",
            "budget_range": "3000-6000",
            "time_preference": "Morning"
        }
    },
    {
        "email": "pradeep@gmail.com",
        "name": "Pradeep Odela",
        "preferences": {
            "preferred_airline": "Vistara",
            "seat_type": "Aisle",
            "meal": "Non-Veg",
            "budget_range": "4000-8000",
            "time_preference": "Evening"
        }
    }
]

# --------------------------------
# HEALTH CHECK
# --------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Flight Booking Demo API",
        "status": "Running 🚀"
    })


# --------------------------------
# OAUTH TOKEN (MOCK)
# --------------------------------

@app.route("/oauth/token", methods=["POST"])
def oauth_token():

    return jsonify({
        "access_token": "demo-access-token",
        "token_type": "Bearer",
        "expires_in": 3600,
        "scope": "flights.search flights.read flights.book customers.read"
    })


# --------------------------------
# SEARCH FLIGHTS
# --------------------------------

@app.route("/flight-search", methods=["POST"])
def flight_search():

    data = request.get_json(force=True)

    source = data.get("source")
    destination = data.get("destination")
    date = data.get("date")

    if not source or not destination or not date:
        return jsonify({"error": "source, destination and date required"}), 400

    results = []

    for flight in MOCK_FLIGHTS:
        if (
            flight["route"]["source"] == source.upper()
            and flight["route"]["destination"] == destination.upper()
            and flight["date"] == date
        ):
            results.append({
                "flight_id": flight["flight_id"],
                "airline": flight["airline"],
                "departure": flight["timings"]["departure"],
                "arrival": flight["timings"]["arrival"],
                "duration": flight["timings"]["duration"],
                "price": flight["pricing"]["amount"],
                "currency": flight["pricing"]["currency"],
                "seats_available": flight["seats_available"]
            })

    return jsonify({
        "total_results": len(results),
        "flights": results
    })


# --------------------------------
# FLIGHT DETAILS
# --------------------------------

@app.route("/flight-details/<flight_id>", methods=["GET"])
def flight_details(flight_id):

    flight_id = flight_id.upper()

    for flight in MOCK_FLIGHTS:
        if flight["flight_id"] == flight_id:
            return jsonify(flight)

    return jsonify({"error": "Flight not found"}), 404


# --------------------------------
# CUSTOMER PREFERENCES
# --------------------------------

@app.route("/customer-preferences", methods=["GET"])
def customer_preferences():

    email = request.args.get("email")

    if not email:
        return jsonify({"error": "email is required"}), 400

    for customer in MOCK_CUSTOMERS:
        if customer["email"].lower() == email.lower():
            return jsonify({
                "email": customer["email"],
                "name": customer["name"],
                "preferences": customer["preferences"]
            })

    return jsonify({"error": "Customer not found"}), 404


# --------------------------------
# BOOK FLIGHT (DUMMY)
# --------------------------------

@app.route("/book-flight", methods=["POST"])
def book_flight():

    data = request.get_json(force=True)

    flight_id = data.get("flight_id")
    email = data.get("email")

    if not flight_id or not email:
        return jsonify({"error": "flight_id and email are required"}), 400

    flight_id = flight_id.upper()

    selected_flight = None

    for flight in MOCK_FLIGHTS:
        if flight["flight_id"] == flight_id:
            selected_flight = flight
            break

    if not selected_flight:
        return jsonify({"error": "Flight not found"}), 404

    booking_reference = "PNR-" + uuid.uuid4().hex[:8].upper()

    booking_response = {
        "status": "SUCCESS",
        "message": "Flight booked successfully ✈️",
        "booking_details": {
            "pnr": booking_reference,
            "flight_id": flight_id,
            "airline": selected_flight["airline"],
            "route": selected_flight["route"],
            "departure": selected_flight["timings"]["departure"],
            "arrival": selected_flight["timings"]["arrival"],
            "date": selected_flight["date"],
            "passenger_email": email,
            "seat_number": "W" + str(uuid.uuid4().int % 60),
            "booking_time": datetime.utcnow().isoformat()
        }
    }

    return jsonify(booking_response)


# --------------------------------
# RAILWAY PORT CONFIG
# --------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
