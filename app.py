from flask import Flask, request, jsonify
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# --------------------------------
# MOCK FLIGHT DATABASE (DOMESTIC + INTERNATIONAL + CLASS SUPPORT)
# --------------------------------

MOCK_FLIGHTS = [

    # ---------------- DOMESTIC ECONOMY ----------------

    {
        "flight_id": "AI101-E",
        "airline": "Air India",
        "class": "Economy",
        "route": {"source": "HYD", "destination": "DEL"},
        "date": "2026-02-10",
        "timings": {"departure": "08:30", "arrival": "10:45", "duration": "2h 15m"},
        "pricing": {"amount": 5200, "currency": "INR"},
        "baggage": {"cabin": "7 Kg", "checkin": "15 Kg"},
        "seats_available": 20,
        "fare_rules": "Non-refundable",
        "policies": {"cancellation": "₹2000 fee", "reschedule": "₹1500 fee"}
    },

    {
        "flight_id": "AI101-B",
        "airline": "Air India",
        "class": "Business",
        "route": {"source": "HYD", "destination": "DEL"},
        "date": "2026-02-10",
        "timings": {"departure": "08:30", "arrival": "10:45", "duration": "2h 15m"},
        "pricing": {"amount": 11500, "currency": "INR"},
        "baggage": {"cabin": "12 Kg", "checkin": "30 Kg"},
        "seats_available": 6,
        "fare_rules": "Fully refundable",
        "policies": {"cancellation": "Free", "reschedule": "Free"}
    },

    # ---------------- DOMESTIC LOW COST ----------------

    {
        "flight_id": "IN202-E",
        "airline": "Indigo",
        "class": "Economy",
        "route": {"source": "HYD", "destination": "DEL"},
        "date": "2026-02-10",
        "timings": {"departure": "14:00", "arrival": "16:10", "duration": "2h 10m"},
        "pricing": {"amount": 4800, "currency": "INR"},
        "baggage": {"cabin": "7 Kg", "checkin": "20 Kg"},
        "seats_available": 15,
        "fare_rules": "Partially refundable",
        "policies": {"cancellation": "₹1500 fee", "reschedule": "₹1000 fee"}
    },

    # ---------------- INTERNATIONAL ECONOMY ----------------

    {
        "flight_id": "EK501-E",
        "airline": "Emirates",
        "class": "Economy",
        "route": {"source": "DEL", "destination": "DXB"},
        "date": "2026-02-12",
        "timings": {"departure": "21:30", "arrival": "00:45", "duration": "3h 45m"},
        "pricing": {"amount": 28500, "currency": "INR"},
        "baggage": {"cabin": "7 Kg", "checkin": "25 Kg"},
        "seats_available": 30,
        "fare_rules": "Refundable with fee",
        "policies": {"cancellation": "₹5000 fee", "reschedule": "₹3500 fee"}
    },

    # ---------------- INTERNATIONAL BUSINESS ----------------

    {
        "flight_id": "EK501-B",
        "airline": "Emirates",
        "class": "Business",
        "route": {"source": "DEL", "destination": "DXB"},
        "date": "2026-02-12",
        "timings": {"departure": "21:30", "arrival": "00:45", "duration": "3h 45m"},
        "pricing": {"amount": 78000, "currency": "INR"},
        "baggage": {"cabin": "15 Kg", "checkin": "40 Kg"},
        "seats_available": 8,
        "fare_rules": "Fully refundable",
        "policies": {"cancellation": "Free", "reschedule": "Free"}
    },

    # ---------------- USA ROUTE ----------------

    {
        "flight_id": "AI901-E",
        "airline": "Air India",
        "class": "Economy",
        "route": {"source": "DEL", "destination": "JFK"},
        "date": "2026-02-15",
        "timings": {"departure": "02:00", "arrival": "07:30", "duration": "15h 30m"},
        "pricing": {"amount": 62000, "currency": "INR"},
        "baggage": {"cabin": "10 Kg", "checkin": "30 Kg"},
        "seats_available": 40,
        "fare_rules": "Refundable with fee",
        "policies": {"cancellation": "₹8000 fee", "reschedule": "₹6000 fee"}
    }
]

# --------------------------------
# MOCK CUSTOMER PREFERENCES
# --------------------------------

MOCK_CUSTOMERS = [
    {
        "email": "rahul@gmail.com",
        "name": "Rahul Sharma",
        "preferences": {
            "preferred_airline": "Indigo",
            "seat_type": "Window",
            "travel_class": "Economy",
            "meal": "Veg",
            "budget_range": "3000-6000",
            "time_preference": "Morning"
        }
    },
    {
        "email": "pradeep@gmail.com",
        "name": "Pradeep Odela",
        "preferences": {
            "preferred_airline": "Emirates",
            "seat_type": "Aisle",
            "travel_class": "Business",
            "meal": "Non-Veg",
            "budget_range": "60000-90000",
            "time_preference": "Night"
        }
    }
]

# --------------------------------
# HEALTH CHECK
# --------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({"service": "Flight Booking Demo API", "status": "Running 🚀"})


# --------------------------------
# OAUTH TOKEN (MOCK)
# --------------------------------

@app.route("/oauth/token", methods=["POST"])
def oauth_token():
    return jsonify({
        "access_token": "demo-access-token",
        "token_type": "Bearer",
        "expires_in": 3600,
        "scope": "flights.search flights.read"
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
                "class": flight["class"],
                "departure": flight["timings"]["departure"],
                "arrival": flight["timings"]["arrival"],
                "duration": flight["timings"]["duration"],
                "price": flight["pricing"]["amount"],
                "currency": flight["pricing"]["currency"],
                "seats_available": flight["seats_available"]
            })

    return jsonify({"total_results": len(results), "flights": results})


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
            return jsonify(customer)

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
        return jsonify({"error": "flight_id and email required"}), 400

    flight_id = flight_id.upper()

    selected_flight = None

    for flight in MOCK_FLIGHTS:
        if flight["flight_id"] == flight_id:
            selected_flight = flight
            break

    if not selected_flight:
        return jsonify({"error": "Flight not found"}), 404

    pnr = "PNR-" + uuid.uuid4().hex[:8].upper()

    return jsonify({
        "status": "SUCCESS",
        "message": "Flight booked successfully ✈️",
        "booking_details": {
            "pnr": pnr,
            "flight_id": flight_id,
            "airline": selected_flight["airline"],
            "class": selected_flight["class"],
            "route": selected_flight["route"],
            "seat_number": "W" + str(uuid.uuid4().int % 60),
            "booking_time": datetime.utcnow().isoformat(),
            "passenger_email": email
        }
    })


# --------------------------------
# RAILWAY PORT CONFIG
# --------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
