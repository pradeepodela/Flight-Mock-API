from flask import Flask, request, jsonify
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# --------------------------------
# MOCK FLIGHT DATABASE (DOMESTIC + INTERNATIONAL + CLASS SUPPORT)
# --------------------------------

MOCK_FLIGHTS = [

# ===================== FEB 10 =====================

# -------- MAA → DXB --------

{"flight_id":"EK210E","airline":"Emirates","class":"Economy","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-10","timings":{"departure":"01:50","arrival":"05:05","duration":"4h 15m"},"pricing":{"amount":28000,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"25 Kg"},"seats_available":48,"fare_rules":"Refundable with fee","policies":{"cancellation":"₹5000 fee","reschedule":"₹3500 fee"}},

{"flight_id":"EK211B","airline":"Emirates","class":"Business","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-10","timings":{"departure":"03:30","arrival":"06:45","duration":"4h 15m"},"pricing":{"amount":79000,"currency":"INR"},"baggage":{"cabin":"15 Kg","checkin":"40 Kg"},"seats_available":8,"fare_rules":"Fully refundable","policies":{"cancellation":"Free","reschedule":"Free"}},

{"flight_id":"AI210E","airline":"Air India","class":"Economy","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-10","timings":{"departure":"07:00","arrival":"11:20","duration":"4h 20m"},"pricing":{"amount":29500,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"23 Kg"},"seats_available":40,"fare_rules":"Partially refundable","policies":{"cancellation":"₹4500 fee","reschedule":"₹3000 fee"}},

{"flight_id":"QR210E","airline":"Qatar Airways","class":"Economy","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-10","timings":{"departure":"17:10","arrival":"21:30","duration":"4h 20m"},"pricing":{"amount":30500,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"30 Kg"},"seats_available":30,"fare_rules":"Refundable","policies":{"cancellation":"₹6000 fee","reschedule":"₹4000 fee"}},

{"flight_id":"EK212E","airline":"Emirates","class":"Economy","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-10","timings":{"departure":"12:30","arrival":"15:45","duration":"4h 15m"},"pricing":{"amount":28800,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"25 Kg"},"seats_available":36,"fare_rules":"Refundable with fee","policies":{"cancellation":"₹5000 fee","reschedule":"₹3500 fee"}},

{"flight_id":"EK213B","airline":"Emirates","class":"Business","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-10","timings":{"departure":"22:00","arrival":"01:15","duration":"4h 15m"},"pricing":{"amount":82000,"currency":"INR"},"baggage":{"cabin":"15 Kg","checkin":"40 Kg"},"seats_available":6,"fare_rules":"Fully refundable","policies":{"cancellation":"Free","reschedule":"Free"}},


# -------- MAA → DEL --------

{"flight_id":"AI401E","airline":"Air India","class":"Economy","route":{"source":"MAA","destination":"DEL"},"date":"2026-04-10","timings":{"departure":"05:50","arrival":"08:40","duration":"2h 50m"},"pricing":{"amount":6200,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"15 Kg"},"seats_available":42,"fare_rules":"Non-refundable","policies":{"cancellation":"₹2000 fee","reschedule":"₹1500 fee"}},

{"flight_id":"6E501E","airline":"Indigo","class":"Economy","route":{"source":"MAA","destination":"DEL"},"date":"2026-04-10","timings":{"departure":"08:30","arrival":"11:20","duration":"2h 50m"},"pricing":{"amount":6100,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"20 Kg"},"seats_available":38,"fare_rules":"Partially refundable","policies":{"cancellation":"₹1500 fee","reschedule":"₹1000 fee"}},

{"flight_id":"VJ601B","airline":"Vistara","class":"Business","route":{"source":"MAA","destination":"DEL"},"date":"2026-04-10","timings":{"departure":"11:00","arrival":"13:50","duration":"2h 50m"},"pricing":{"amount":14800,"currency":"INR"},"baggage":{"cabin":"12 Kg","checkin":"30 Kg"},"seats_available":10,"fare_rules":"Fully refundable","policies":{"cancellation":"Free","reschedule":"Free"}},

{"flight_id":"AI402E","airline":"Air India","class":"Economy","route":{"source":"MAA","destination":"DEL"},"date":"2026-04-10","timings":{"departure":"14:00","arrival":"16:50","duration":"2h 50m"},"pricing":{"amount":6400,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"15 Kg"},"seats_available":36,"fare_rules":"Non-refundable","policies":{"cancellation":"₹2000 fee","reschedule":"₹1500 fee"}},

{"flight_id":"6E502E","airline":"Indigo","class":"Economy","route":{"source":"MAA","destination":"DEL"},"date":"2026-04-10","timings":{"departure":"17:30","arrival":"20:20","duration":"2h 50m"},"pricing":{"amount":5900,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"20 Kg"},"seats_available":40,"fare_rules":"Partially refundable","policies":{"cancellation":"₹1800 fee","reschedule":"₹1200 fee"}},

{"flight_id":"AI403B","airline":"Air India","class":"Business","route":{"source":"MAA","destination":"DEL"},"date":"2026-04-10","timings":{"departure":"20:45","arrival":"23:35","duration":"2h 50m"},"pricing":{"amount":15500,"currency":"INR"},"baggage":{"cabin":"12 Kg","checkin":"35 Kg"},"seats_available":6,"fare_rules":"Fully refundable","policies":{"cancellation":"Free","reschedule":"Free"}},


# ===================== FEB 11 =====================

# -------- MAA → DXB --------

{"flight_id":"EK220E","airline":"Emirates","class":"Economy","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-11","timings":{"departure":"02:00","arrival":"05:15","duration":"4h 15m"},"pricing":{"amount":29000,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"25 Kg"},"seats_available":44,"fare_rules":"Refundable with fee","policies":{"cancellation":"₹5000 fee","reschedule":"₹3500 fee"}},

{"flight_id":"EK221B","airline":"Emirates","class":"Business","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-11","timings":{"departure":"04:00","arrival":"07:15","duration":"4h 15m"},"pricing":{"amount":80500,"currency":"INR"},"baggage":{"cabin":"15 Kg","checkin":"40 Kg"},"seats_available":9,"fare_rules":"Fully refundable","policies":{"cancellation":"Free","reschedule":"Free"}},

{"flight_id":"AI220E","airline":"Air India","class":"Economy","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-11","timings":{"departure":"09:00","arrival":"13:20","duration":"4h 20m"},"pricing":{"amount":30000,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"23 Kg"},"seats_available":38,"fare_rules":"Partially refundable","policies":{"cancellation":"₹4500 fee","reschedule":"₹3000 fee"}},

{"flight_id":"QR220E","airline":"Qatar Airways","class":"Economy","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-11","timings":{"departure":"14:00","arrival":"18:20","duration":"4h 20m"},"pricing":{"amount":31200,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"30 Kg"},"seats_available":32,"fare_rules":"Refundable","policies":{"cancellation":"₹6000 fee","reschedule":"₹4000 fee"}},

{"flight_id":"EK222E","airline":"Emirates","class":"Economy","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-11","timings":{"departure":"18:30","arrival":"21:45","duration":"4h 15m"},"pricing":{"amount":29500,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"25 Kg"},"seats_available":35,"fare_rules":"Refundable with fee","policies":{"cancellation":"₹5000 fee","reschedule":"₹3500 fee"}},

{"flight_id":"EK223B","airline":"Emirates","class":"Business","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-11","timings":{"departure":"23:30","arrival":"02:45","duration":"4h 15m"},"pricing":{"amount":83500,"currency":"INR"},"baggage":{"cabin":"15 Kg","checkin":"40 Kg"},"seats_available":7,"fare_rules":"Fully refundable","policies":{"cancellation":"Free","reschedule":"Free"}},


# -------- MAA → DEL --------

{"flight_id":"AI410E","airline":"Air India","class":"Economy","route":{"source":"MAA","destination":"DEL"},"date":"2026-04-11","timings":{"departure":"05:40","arrival":"08:30","duration":"2h 50m"},"pricing":{"amount":6300,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"15 Kg"},"seats_available":40,"fare_rules":"Non-refundable","policies":{"cancellation":"₹2000 fee","reschedule":"₹1500 fee"}},

{"flight_id":"6E510E","airline":"Indigo","class":"Economy","route":{"source":"MAA","destination":"DEL"},"date":"2026-04-11","timings":{"departure":"08:20","arrival":"11:10","duration":"2h 50m"},"pricing":{"amount":6150,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"20 Kg"},"seats_available":36,"fare_rules":"Partially refundable","policies":{"cancellation":"₹1500 fee","reschedule":"₹1000 fee"}},

{"flight_id":"VJ610B","airline":"Vistara","class":"Business","route":{"source":"MAA","destination":"DEL"},"date":"2026-04-11","timings":{"departure":"11:10","arrival":"14:00","duration":"2h 50m"},"pricing":{"amount":15000,"currency":"INR"},"baggage":{"cabin":"12 Kg","checkin":"30 Kg"},"seats_available":9,"fare_rules":"Fully refundable","policies":{"cancellation":"Free","reschedule":"Free"}},

{"flight_id":"AI412E","airline":"Air India","class":"Economy","route":{"source":"MAA","destination":"DEL"},"date":"2026-04-11","timings":{"departure":"14:10","arrival":"17:00","duration":"2h 50m"},"pricing":{"amount":6450,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"15 Kg"},"seats_available":34,"fare_rules":"Non-refundable","policies":{"cancellation":"₹2000 fee","reschedule":"₹1500 fee"}},

{"flight_id":"6E512E","airline":"Indigo","class":"Economy","route":{"source":"MAA","destination":"DEL"},"date":"2026-04-11","timings":{"departure":"17:20","arrival":"20:10","duration":"2h 50m"},"pricing":{"amount":6000,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"20 Kg"},"seats_available":38,"fare_rules":"Partially refundable","policies":{"cancellation":"₹1800 fee","reschedule":"₹1200 fee"}},

{"flight_id":"AI413B","airline":"Air India","class":"Business","route":{"source":"MAA","destination":"DEL"},"date":"2026-04-11","timings":{"departure":"21:30","arrival":"00:20","duration":"2h 50m"},"pricing":{"amount":15800,"currency":"INR"},"baggage":{"cabin":"12 Kg","checkin":"35 Kg"},"seats_available":7,"fare_rules":"Fully refundable","policies":{"cancellation":"Free","reschedule":"Free"}},


# ===================== FEB 12 =====================

# -------- MAA → DXB --------

{"flight_id":"EK230E","airline":"Emirates","class":"Economy","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-12","timings":{"departure":"02:20","arrival":"05:35","duration":"4h 15m"},"pricing":{"amount":30000,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"25 Kg"},"seats_available":42,"fare_rules":"Refundable with fee","policies":{"cancellation":"₹5000 fee","reschedule":"₹3500 fee"}},

{"flight_id":"EK231B","airline":"Emirates","class":"Business","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-12","timings":{"departure":"04:40","arrival":"07:55","duration":"4h 15m"},"pricing":{"amount":81500,"currency":"INR"},"baggage":{"cabin":"15 Kg","checkin":"40 Kg"},"seats_available":8,"fare_rules":"Fully refundable","policies":{"cancellation":"Free","reschedule":"Free"}},

{"flight_id":"AI230E","airline":"Air India","class":"Economy","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-12","timings":{"departure":"08:40","arrival":"13:00","duration":"4h 20m"},"pricing":{"amount":30500,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"23 Kg"},"seats_available":36,"fare_rules":"Partially refundable","policies":{"cancellation":"₹4500 fee","reschedule":"₹3000 fee"}},

{"flight_id":"QR230E","airline":"Qatar Airways","class":"Economy","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-12","timings":{"departure":"13:00","arrival":"17:20","duration":"4h 20m"},"pricing":{"amount":31800,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"30 Kg"},"seats_available":30,"fare_rules":"Refundable","policies":{"cancellation":"₹6000 fee","reschedule":"₹4000 fee"}},

{"flight_id":"EK232E","airline":"Emirates","class":"Economy","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-12","timings":{"departure":"18:10","arrival":"21:25","duration":"4h 15m"},"pricing":{"amount":30200,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"25 Kg"},"seats_available":34,"fare_rules":"Refundable with fee","policies":{"cancellation":"₹5000 fee","reschedule":"₹3500 fee"}},

{"flight_id":"EK233B","airline":"Emirates","class":"Business","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-12","timings":{"departure":"23:10","arrival":"02:25","duration":"4h 15m"},"pricing":{"amount":84500,"currency":"INR"},"baggage":{"cabin":"15 Kg","checkin":"40 Kg"},"seats_available":6,"fare_rules":"Fully refundable","policies":{"cancellation":"Free","reschedule":"Free"}},


# -------- MAA → DEL --------

{"flight_id":"AI420E","airline":"Air India","class":"Economy","route":{"source":"MAA","destination":"DEL"},"date":"2026-04-12","timings":{"departure":"06:10","arrival":"09:00","duration":"2h 50m"},"pricing":{"amount":6500,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"15 Kg"},"seats_available":38,"fare_rules":"Non-refundable","policies":{"cancellation":"₹2000 fee","reschedule":"₹1500 fee"}},

{"flight_id":"6E520E","airline":"Indigo","class":"Economy","route":{"source":"MAA","destination":"DEL"},"date":"2026-04-12","timings":{"departure":"09:00","arrival":"11:50","duration":"2h 50m"},"pricing":{"amount":6200,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"20 Kg"},"seats_available":36,"fare_rules":"Partially refundable","policies":{"cancellation":"₹1500 fee","reschedule":"₹1000 fee"}},

{"flight_id":"VJ620B","airline":"Vistara","class":"Business","route":{"source":"MAA","destination":"DEL"},"date":"2026-04-12","timings":{"departure":"11:40","arrival":"14:30","duration":"2h 50m"},"pricing":{"amount":15200,"currency":"INR"},"baggage":{"cabin":"12 Kg","checkin":"30 Kg"},"seats_available":8,"fare_rules":"Fully refundable","policies":{"cancellation":"Free","reschedule":"Free"}},

{"flight_id":"AI422E","airline":"Air India","class":"Economy","route":{"source":"MAA","destination":"DEL"},"date":"2026-04-12","timings":{"departure":"14:20","arrival":"17:10","duration":"2h 50m"},"pricing":{"amount":6600,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"15 Kg"},"seats_available":35,"fare_rules":"Non-refundable","policies":{"cancellation":"₹2000 fee","reschedule":"₹1500 fee"}},

{"flight_id":"6E522E","airline":"Indigo","class":"Economy","route":{"source":"MAA","destination":"DEL"},"date":"2026-04-12","timings":{"departure":"18:00","arrival":"20:50","duration":"2h 50m"},"pricing":{"amount":6100,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"20 Kg"},"seats_available":37,"fare_rules":"Partially refundable","policies":{"cancellation":"₹1800 fee","reschedule":"₹1200 fee"}},

{"flight_id":"AI423B","airline":"Air India","class":"Business","route":{"source":"MAA","destination":"DEL"},"date":"2026-04-12","timings":{"departure":"21:40","arrival":"00:30","duration":"2h 50m"},"pricing":{"amount":15800,"currency":"INR"},"baggage":{"cabin":"12 Kg","checkin":"35 Kg"},"seats_available":6,"fare_rules":"Fully refundable","policies":{"cancellation":"Free","reschedule":"Free"}},

# ========================= FEB 13 =========================

{"flight_id":"EK231E","airline":"Emirates","class":"Economy","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-13","timings":{"departure":"02:15","arrival":"05:30","duration":"4h 15m"},"pricing":{"amount":30000,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"25 Kg"},"seats_available":32,"fare_rules":"Refundable with fee","policies":{"cancellation":"₹5000 fee","reschedule":"₹3500 fee"}},

{"flight_id":"SQ331E","airline":"Singapore Airlines","class":"Economy","route":{"source":"MAA","destination":"SIN"},"date":"2026-04-13","timings":{"departure":"09:45","arrival":"16:30","duration":"4h 45m"},"pricing":{"amount":34000,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"30 Kg"},"seats_available":27,"fare_rules":"Refundable","policies":{"cancellation":"₹4000 fee","reschedule":"₹3000 fee"}},

{"flight_id":"AI431E","airline":"Air India","class":"Economy","route":{"source":"MAA","destination":"BOM"},"date":"2026-04-13","timings":{"departure":"08:00","arrival":"10:00","duration":"2h"},"pricing":{"amount":5500,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"15 Kg"},"seats_available":35,"fare_rules":"Non-refundable","policies":{"cancellation":"₹2000 fee","reschedule":"₹1500 fee"}},


# ========================= FEB 14 =========================

{"flight_id":"EK241E","airline":"Emirates","class":"Economy","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-14","timings":{"departure":"03:30","arrival":"06:45","duration":"4h 15m"},"pricing":{"amount":30500,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"25 Kg"},"seats_available":30,"fare_rules":"Refundable with fee","policies":{"cancellation":"₹5000 fee","reschedule":"₹3500 fee"}},

{"flight_id":"SQ341E","airline":"Singapore Airlines","class":"Economy","route":{"source":"MAA","destination":"SIN"},"date":"2026-04-14","timings":{"departure":"11:30","arrival":"18:15","duration":"4h 45m"},"pricing":{"amount":34500,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"30 Kg"},"seats_available":24,"fare_rules":"Refundable","policies":{"cancellation":"₹4000 fee","reschedule":"₹3000 fee"}},

{"flight_id":"AI441E","airline":"Air India","class":"Economy","route":{"source":"MAA","destination":"DEL"},"date":"2026-04-14","timings":{"departure":"07:30","arrival":"10:20","duration":"2h 50m"},"pricing":{"amount":6500,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"15 Kg"},"seats_available":34,"fare_rules":"Non-refundable","policies":{"cancellation":"₹2000 fee","reschedule":"₹1500 fee"}},


# ========================= FEB 15 =========================

{"flight_id":"EK251E","airline":"Emirates","class":"Economy","route":{"source":"MAA","destination":"DXB"},"date":"2026-04-15","timings":{"departure":"02:45","arrival":"06:00","duration":"4h 15m"},"pricing":{"amount":31000,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"25 Kg"},"seats_available":28,"fare_rules":"Refundable with fee","policies":{"cancellation":"₹5000 fee","reschedule":"₹3500 fee"}},

{"flight_id":"SQ351E","airline":"Singapore Airlines","class":"Economy","route":{"source":"MAA","destination":"SIN"},"date":"2026-04-15","timings":{"departure":"10:15","arrival":"17:00","duration":"4h 45m"},"pricing":{"amount":35000,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"30 Kg"},"seats_available":22,"fare_rules":"Refundable","policies":{"cancellation":"₹4000 fee","reschedule":"₹3000 fee"}},

{"flight_id":"AI451E","airline":"Air India","class":"Economy","route":{"source":"MAA","destination":"BOM"},"date":"2026-04-15","timings":{"departure":"08:30","arrival":"10:30","duration":"2h"},"pricing":{"amount":5600,"currency":"INR"},"baggage":{"cabin":"7 Kg","checkin":"15 Kg"},"seats_available":33,"fare_rules":"Non-refundable","policies":{"cancellation":"₹2000 fee","reschedule":"₹1500 fee"}}

]


# --------------------------------
# MOCK CUSTOMER PREFERENCES
# --------------------------------

MOCK_CUSTOMERS = [

{"email": "rahul@gmail.com", "name": "Rahul Sharma", "preferences": {"preferred_airline": "Indigo", "seat_type": "Window", "travel_class": "Economy", "budget_range": "4000-7000", "time_preference": "Morning"}},

{"email": "pradeep@gmail.com", "name": "Pradeep Odela", "preferences": {"preferred_airline": "Emirates", "seat_type": "Aisle", "travel_class": "Business", "budget_range": "70000-100000", "time_preference": "Night"}},

{"email": "anita@gmail.com", "name": "Anita Rao", "preferences": {"preferred_airline": "Singapore Airlines", "seat_type": "Window", "travel_class": "Economy", "budget_range": "25000-40000", "time_preference": "Evening"}},

{"email": "rohit@gmail.com", "name": "Rohit Verma", "preferences": {"preferred_airline": "Air India", "seat_type": "Middle", "travel_class": "Economy", "budget_range": "5000-9000", "time_preference": "Morning"}},

{"email": "sneha@gmail.com", "name": "Sneha Patel", "preferences": {"preferred_airline": "Vistara", "seat_type": "Window", "travel_class": "Business", "budget_range": "12000-20000", "time_preference": "Afternoon"}},

{"email": "arjun@gmail.com", "name": "Arjun Mehta", "preferences": {"preferred_airline": "Indigo", "seat_type": "Aisle", "travel_class": "Economy", "budget_range": "4500-8000", "time_preference": "Evening"}},

{"email": "neha@gmail.com", "name": "Neha Singh", "preferences": {"preferred_airline": "Emirates", "seat_type": "Window", "travel_class": "Business", "budget_range": "75000-110000", "time_preference": "Night"}},

{"email": "vikram@gmail.com", "name": "Vikram Iyer", "preferences": {"preferred_airline": "Air India", "seat_type": "Aisle", "travel_class": "Economy", "budget_range": "6000-10000", "time_preference": "Morning"}},

{"email": "pooja@gmail.com", "name": "Pooja Nair", "preferences": {"preferred_airline": "Singapore Airlines", "seat_type": "Window", "travel_class": "Economy", "budget_range": "28000-45000", "time_preference": "Evening"}},

{"email": "aman@gmail.com", "name": "Aman Khan", "preferences": {"preferred_airline": "Vistara", "seat_type": "Aisle", "travel_class": "Business", "budget_range": "15000-25000", "time_preference": "Afternoon"}}

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
