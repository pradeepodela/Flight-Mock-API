from flask import Flask, request, jsonify
import os

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
# HEALTH CHECK
# --------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Flight Booking Demo API",
        "status": "Running 🚀"
    })


# --------------------------------
# SEARCH FLIGHTS
# --------------------------------

@app.route("/flight-search", methods=["POST"])
def flight_search():

    data = request.json

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

    for flight in MOCK_FLIGHTS:
        if flight["flight_id"] == flight_id:
            return jsonify(flight)

    return jsonify({"error": "Flight not found"}), 404

@app.route("/oauth/token", methods=["POST"])
def oauth_token():

    return jsonify({
        "access_token": "demo-access-token",
        "token_type": "Bearer",
        "expires_in": 3600,
        "scope": "flights.search flights.read"
    })

# --------------------------------
# RAILWAY PORT CONFIG
# --------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
