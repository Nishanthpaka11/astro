"""
வ உ சி யின் உறவைத் தேடி — Flask Backend Server
Serves API endpoints for bride/groom profiles and porutham matching.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback

from astrology_engine import calculate_chart
from porutham_engine import calculate_porutham
from db import (
    init_db,
    save_bride, update_bride, delete_bride, get_bride, get_all_brides, search_brides,
    save_groom, update_groom, delete_groom, get_groom, get_all_grooms, search_grooms,
    save_match, get_match, get_all_matches,
)

app = Flask(__name__)

# Allow requests from any origin (GoDaddy frontend)
CORS(app, resources={r"/api/*": {"origins": "*"}})


# ─── Health Check ────────────────────────────────────────────────────────────

@app.route('/')
def health_check():
    """Health check endpoint for Render."""
    return jsonify({"status": "ok", "service": "வ உ சி யின் உறவைத் தேடி API"})


# ─── Helper: Compute Chart ───────────────────────────────────────────────────

def _compute_chart(data):
    """Compute birth chart from profile data. Returns chart dict or None."""
    name = data.get('full_name', '').strip()
    dob = data.get('dob', '').strip()
    time_str = data.get('birth_time', '').strip()
    place = data.get('birth_place', '').strip()

    if not all([name, dob, time_str, place]):
        return None

    return calculate_chart(name, dob, time_str, place)


# ─── Bride API Routes ───────────────────────────────────────────────────────

@app.route('/api/brides', methods=['POST'])
def create_bride():
    """Create a new bride profile with computed birth chart."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate required birth fields
        for field in ['full_name', 'dob', 'birth_time', 'birth_place']:
            if not data.get(field, '').strip():
                return jsonify({"error": f"{field} is required"}), 400

        # Compute chart
        chart = _compute_chart(data)
        if chart is None:
            return jsonify({"error": "Could not compute birth chart. Check birth details."}), 400

        # Save
        if not app.config.get('DB_AVAILABLE', False):
            return jsonify({"error": "Database not available"}), 503

        bride_id = save_bride(data, chart)
        if not bride_id:
            return jsonify({"error": "Failed to save bride record"}), 500

        return jsonify({"success": True, "bride_id": bride_id, "chart": chart}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route('/api/brides', methods=['GET'])
def list_brides():
    """List all bride records with optional search."""
    try:
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '', type=str)
        records, total = get_all_brides(page=page, search=search)
        return jsonify({"success": True, "records": records, "total": total, "page": page})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/api/brides/search', methods=['GET'])
def api_search_brides():
    """Quick search brides for autocomplete."""
    try:
        q = request.args.get('q', '', type=str)
        results = search_brides(q)
        return jsonify({"success": True, "results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/brides/<bride_id>', methods=['GET'])
def get_bride_detail(bride_id):
    """Get a single bride record by ID."""
    try:
        record = get_bride(bride_id)
        if not record:
            return jsonify({"error": "Bride not found"}), 404
        return jsonify({"success": True, "record": record})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/api/brides/<bride_id>', methods=['PUT'])
def update_bride_detail(bride_id):
    """Update bride profile. Re-computes chart if birth details changed."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Re-compute chart if birth details present
        chart = None
        if data.get('dob') and data.get('birth_time') and data.get('birth_place'):
            chart = _compute_chart(data)

        success = update_bride(bride_id, data, chart)
        if not success:
            return jsonify({"error": "Failed to update or record not found"}), 404

        return jsonify({"success": True, "bride_id": bride_id})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route('/api/brides/<bride_id>', methods=['DELETE'])
def delete_bride_record(bride_id):
    """Delete a bride record."""
    try:
        success = delete_bride(bride_id)
        if not success:
            return jsonify({"error": "Failed to delete or record not found"}), 404
        return jsonify({"success": True})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ─── Groom API Routes ───────────────────────────────────────────────────────

@app.route('/api/grooms', methods=['POST'])
def create_groom():
    """Create a new groom profile with computed birth chart."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate required birth fields
        for field in ['full_name', 'dob', 'birth_time', 'birth_place']:
            if not data.get(field, '').strip():
                return jsonify({"error": f"{field} is required"}), 400

        # Compute chart
        chart = _compute_chart(data)
        if chart is None:
            return jsonify({"error": "Could not compute birth chart. Check birth details."}), 400

        # Save
        if not app.config.get('DB_AVAILABLE', False):
            return jsonify({"error": "Database not available"}), 503

        groom_id = save_groom(data, chart)
        if not groom_id:
            return jsonify({"error": "Failed to save groom record"}), 500

        return jsonify({"success": True, "groom_id": groom_id, "chart": chart}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route('/api/grooms', methods=['GET'])
def list_grooms():
    """List all groom records with optional search."""
    try:
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '', type=str)
        records, total = get_all_grooms(page=page, search=search)
        return jsonify({"success": True, "records": records, "total": total, "page": page})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/api/grooms/search', methods=['GET'])
def api_search_grooms():
    """Quick search grooms for autocomplete."""
    try:
        q = request.args.get('q', '', type=str)
        results = search_grooms(q)
        return jsonify({"success": True, "results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/grooms/<groom_id>', methods=['GET'])
def get_groom_detail(groom_id):
    """Get a single groom record by ID."""
    try:
        record = get_groom(groom_id)
        if not record:
            return jsonify({"error": "Groom not found"}), 404
        return jsonify({"success": True, "record": record})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/api/grooms/<groom_id>', methods=['PUT'])
def update_groom_detail(groom_id):
    """Update groom profile. Re-computes chart if birth details changed."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Re-compute chart if birth details present
        chart = None
        if data.get('dob') and data.get('birth_time') and data.get('birth_place'):
            chart = _compute_chart(data)

        success = update_groom(groom_id, data, chart)
        if not success:
            return jsonify({"error": "Failed to update or record not found"}), 404

        return jsonify({"success": True, "groom_id": groom_id})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route('/api/grooms/<groom_id>', methods=['DELETE'])
def delete_groom_record(groom_id):
    """Delete a groom record."""
    try:
        success = delete_groom(groom_id)
        if not success:
            return jsonify({"error": "Failed to delete or record not found"}), 404
        return jsonify({"success": True})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ─── Match API Routes ───────────────────────────────────────────────────────

@app.route('/api/match', methods=['POST'])
def match():
    """Calculate Porutham between a saved bride and groom by their IDs."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        bride_id = data.get('bride_id', '').strip()
        groom_id = data.get('groom_id', '').strip()

        if not bride_id or not groom_id:
            return jsonify({"error": "Both bride_id and groom_id are required"}), 400

        # Fetch profiles
        bride_record = get_bride(bride_id)
        if not bride_record:
            return jsonify({"error": f"Bride '{bride_id}' not found"}), 404

        groom_record = get_groom(groom_id)
        if not groom_record:
            return jsonify({"error": f"Groom '{groom_id}' not found"}), 404

        # Get charts
        bride_chart = bride_record.get("chart")
        groom_chart = groom_record.get("chart")

        if not bride_chart or not groom_chart:
            return jsonify({"error": "Birth charts not available for one or both profiles"}), 400

        # Calculate compatibility
        porutham = calculate_porutham(bride_chart, groom_chart)

        # Save match record
        match_id = None
        if app.config.get('DB_AVAILABLE', False):
            match_id = save_match(bride_id, groom_id, bride_chart, groom_chart, porutham)

        return jsonify({
            "success": True,
            "match_id": match_id,
            "bride_id": bride_id,
            "groom_id": groom_id,
            "bride_chart": bride_chart,
            "groom_chart": groom_chart,
            "porutham": porutham,
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Calculation error: {str(e)}"}), 500


@app.route('/api/matches', methods=['GET'])
def list_matches():
    """List all match records."""
    try:
        page = request.args.get('page', 1, type=int)
        records, total = get_all_matches(page=page)
        return jsonify({"success": True, "records": records, "total": total, "page": page})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/api/matches/<match_id>', methods=['GET'])
def get_match_detail(match_id):
    """Get a single match record by ID."""
    try:
        record = get_match(match_id)
        if not record:
            return jsonify({"error": "Match not found"}), 404
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
