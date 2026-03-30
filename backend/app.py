"""
வ உ சி யின் உறவைத் தேடி — Flask Backend Server
Serves API endpoints. Deployed on Render.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback

from astrology_engine import calculate_chart
from porutham_engine import calculate_porutham
from db import init_db, save_customer, get_customer, get_all_customers

app = Flask(__name__)

# Allow requests from any origin (GoDaddy frontend)
CORS(app, resources={r"/api/*": {"origins": "*"}})



# ─── API Routes ──────────────────────────────────────────────────────────────

@app.route('/')
def health_check():
    """Health check endpoint for Render."""
    return jsonify({"status": "ok", "service": "வ உ சி யின் உறவைத் தேடி API"})


@app.route('/api/generate-chart', methods=['POST'])
def generate_chart():
    """Generate birth chart for a single person."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        name = data.get('name', '').strip()
        dob = data.get('dob', '').strip()
        time_str = data.get('time', '').strip()
        place = data.get('place', '').strip()

        if not all([name, dob, time_str, place]):
            return jsonify({"error": "All fields are required: name, dob, time, place"}), 400

        chart = calculate_chart(name, dob, time_str, place)
        return jsonify({"success": True, "chart": chart})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Calculation error: {str(e)}"}), 500


@app.route('/api/match', methods=['POST'])
def match():
    """Calculate Porutham between bride and groom."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        bride = data.get('bride', {})
        groom = data.get('groom', {})

        # Validate required fields
        for field in ['name', 'dob', 'time', 'place']:
            if not bride.get(field, '').strip():
                return jsonify({"error": f"Bride's {field} is required"}), 400
            if not groom.get(field, '').strip():
                return jsonify({"error": f"Groom's {field} is required"}), 400

        # Calculate both charts
        bride_chart = calculate_chart(
            bride['name'], bride['dob'], bride['time'], bride['place']
        )
        groom_chart = calculate_chart(
            groom['name'], groom['dob'], groom['time'], groom['place']
        )

        # Calculate compatibility
        porutham = calculate_porutham(bride_chart, groom_chart)

        # Save to MongoDB (if available)
        customer_id = None
        if app.config.get('DB_AVAILABLE', False):
            customer_id = save_customer(bride, groom, bride_chart, groom_chart, porutham)

        return jsonify({
            "success": True,
            "customer_id": customer_id,
            "bride_chart": bride_chart,
            "groom_chart": groom_chart,
            "porutham": porutham
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Calculation error: {str(e)}"}), 500


# ─── Customer API Routes ────────────────────────────────────────────────────

@app.route('/api/customers', methods=['GET'])
def list_customers():
    """List all customer records."""
    try:
        page = request.args.get('page', 1, type=int)
        records, total = get_all_customers(page=page)
        return jsonify({
            "success": True,
            "records": records,
            "total": total,
            "page": page
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/api/customers/<customer_id>', methods=['GET'])
def get_customer_detail(customer_id):
    """Get a single customer record by ID."""
    try:
        record = get_customer(customer_id)
        if not record:
            return jsonify({"error": "Record not found"}), 404
        return jsonify({"success": True, "record": record})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ─── Run Server ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("\n✦ வ உ சி யின் உறவைத் தேடி API Server")
    app.config['DB_AVAILABLE'] = init_db()
    port = int(os.environ.get("PORT", 5000))
    print(f"  http://localhost:{port}\n")
    app.run(debug=True, host='0.0.0.0', port=port)
