"""
வ உ சி யின் உறவைத் தேடி — MongoDB Database Module
Handles connection, saving and retrieving bride, groom and match records.
Three separate collections: brides, grooms, matches.
"""

from pymongo import MongoClient
from datetime import datetime
import pytz
import os


# ─── MongoDB Connection ──────────────────────────────────────────────────────

MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://yisagi868_db_user:47424742@cluster0.knihcws.mongodb.net/")
DB_NAME = "thirukanidham"

client = None
db = None
brides_col = None
grooms_col = None
matches_col = None


def init_db():
    """Initialize MongoDB connection and collections."""
    global client, db, brides_col, grooms_col, matches_col
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # Test connection
        client.server_info()
        db = client[DB_NAME]
        brides_col = db["brides"]
        grooms_col = db["grooms"]
        matches_col = db["matches"]
        print(f"  ✔ MongoDB Atlas connected: {DB_NAME}")
        return True
    except Exception as e:
        print(f"  ⚠ MongoDB not available: {e}")
        print(f"    Records will NOT be saved.")
        return False


# ─── ID Generators ───────────────────────────────────────────────────────────

def _generate_id(collection, prefix):
    """Generate a unique ID in format PREFIX-YYYYMMDD-NNN."""
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    date_str = now.strftime('%Y%m%d')
    full_prefix = f"{prefix}-{date_str}"

    if collection is None:
        return f"{full_prefix}-001"

    # Count today's records to get the next sequence number
    count = collection.count_documents({"_id": {"$regex": f"^{full_prefix}"}})
    seq = str(count + 1).zfill(3)
    return f"{full_prefix}-{seq}"


def _generate_bride_id():
    return _generate_id(brides_col, "BR")


def _generate_groom_id():
    return _generate_id(grooms_col, "GR")


def _generate_match_id():
    return _generate_id(matches_col, "MT")


# ─── Profile Fields Helper ──────────────────────────────────────────────────

PROFILE_FIELDS = [
    # Personal
    "full_name", "gender", "dob", "birth_time", "birth_place",
    "height", "weight", "marital_status", "mother_tongue",
    "religion", "caste", "profile_created_by",
    # Education & Career
    "highest_qualification", "college_university", "occupation",
    "company_name", "annual_income",
    # Location & Lifestyle
    "current_city", "native_place", "family_deity",
]


def _extract_profile(data):
    """Extract profile fields from request data."""
    profile = {}
    for field in PROFILE_FIELDS:
        profile[field] = data.get(field, "").strip() if isinstance(data.get(field, ""), str) else data.get(field, "")
    return profile


# ─── Bride CRUD ──────────────────────────────────────────────────────────────

def save_bride(data, chart):
    """Save a new bride profile with chart to MongoDB. Returns the new ID."""
    if brides_col is None:
        return None

    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)

    profile = _extract_profile(data)
    record = {
        "_id": _generate_bride_id(),
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        **profile,
        "chart": chart,
    }

    try:
        brides_col.insert_one(record)
        return record["_id"]
    except Exception as e:
        print(f"  ⚠ Failed to save bride: {e}")
        return None


def update_bride(bride_id, data, chart=None):
    """Update an existing bride profile. Optionally update chart."""
    if brides_col is None:
        return False

    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)

    profile = _extract_profile(data)
    update_data = {
        "updated_at": now.isoformat(),
        **profile,
    }
    if chart is not None:
        update_data["chart"] = chart

    try:
        result = brides_col.update_one({"_id": bride_id}, {"$set": update_data})
        return result.modified_count > 0
    except Exception as e:
        print(f"  ⚠ Failed to update bride {bride_id}: {e}")
        return False


def delete_bride(bride_id):
    """Delete a bride record by ID."""
    if brides_col is None:
        return False
    try:
        result = brides_col.delete_one({"_id": bride_id})
        return result.deleted_count > 0
    except Exception as e:
        print(f"  ⚠ Failed to delete bride {bride_id}: {e}")
        return False


def get_bride(bride_id):
    """Retrieve a single bride by ID."""
    if brides_col is None:
        return None
    try:
        return brides_col.find_one({"_id": bride_id})
    except Exception:
        return None


def get_all_brides(page=1, per_page=50, search=""):
    """Retrieve all brides, with optional name search, ordered newest first."""
    if brides_col is None:
        return [], 0

    try:
        query = {}
        if search:
            query["full_name"] = {"$regex": search, "$options": "i"}

        total = brides_col.count_documents(query)
        skip = (page - 1) * per_page
        records = list(
            brides_col.find(query, {
                "_id": 1, "created_at": 1, "full_name": 1, "dob": 1,
                "birth_place": 1, "religion": 1, "caste": 1,
                "current_city": 1, "occupation": 1,
            })
            .sort("created_at", -1)
            .skip(skip)
            .limit(per_page)
        )
        return records, total
    except Exception:
        return [], 0


def search_brides(query_text):
    """Quick search brides by name or ID for autocomplete."""
    if brides_col is None:
        return []
    try:
        results = list(
            brides_col.find(
                {"$or": [
                    {"full_name": {"$regex": query_text, "$options": "i"}},
                    {"_id": {"$regex": query_text, "$options": "i"}},
                ]},
                {"_id": 1, "full_name": 1, "dob": 1, "birth_place": 1}
            ).limit(10)
        )
        return results
    except Exception:
        return []


# ─── Groom CRUD ──────────────────────────────────────────────────────────────

def save_groom(data, chart):
    """Save a new groom profile with chart to MongoDB. Returns the new ID."""
    if grooms_col is None:
        return None

    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)

    profile = _extract_profile(data)
    record = {
        "_id": _generate_groom_id(),
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        **profile,
        "chart": chart,
    }

    try:
        grooms_col.insert_one(record)
        return record["_id"]
    except Exception as e:
        print(f"  ⚠ Failed to save groom: {e}")
        return None


def update_groom(groom_id, data, chart=None):
    """Update an existing groom profile. Optionally update chart."""
    if grooms_col is None:
        return False

    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)

    profile = _extract_profile(data)
    update_data = {
        "updated_at": now.isoformat(),
        **profile,
    }
    if chart is not None:
        update_data["chart"] = chart

    try:
        result = grooms_col.update_one({"_id": groom_id}, {"$set": update_data})
        return result.modified_count > 0
    except Exception as e:
        print(f"  ⚠ Failed to update groom {groom_id}: {e}")
        return False


def delete_groom(groom_id):
    """Delete a groom record by ID."""
    if grooms_col is None:
        return False
    try:
        result = grooms_col.delete_one({"_id": groom_id})
        return result.deleted_count > 0
    except Exception as e:
        print(f"  ⚠ Failed to delete groom {groom_id}: {e}")
        return False


def get_groom(groom_id):
    """Retrieve a single groom by ID."""
    if grooms_col is None:
        return None
    try:
        return grooms_col.find_one({"_id": groom_id})
    except Exception:
        return None


def get_all_grooms(page=1, per_page=50, search=""):
    """Retrieve all grooms, with optional name search, ordered newest first."""
    if grooms_col is None:
        return [], 0

    try:
        query = {}
        if search:
            query["full_name"] = {"$regex": search, "$options": "i"}

        total = grooms_col.count_documents(query)
        skip = (page - 1) * per_page
        records = list(
            grooms_col.find(query, {
                "_id": 1, "created_at": 1, "full_name": 1, "dob": 1,
                "birth_place": 1, "religion": 1, "caste": 1,
                "current_city": 1, "occupation": 1,
            })
            .sort("created_at", -1)
            .skip(skip)
            .limit(per_page)
        )
        return records, total
    except Exception:
        return [], 0


def search_grooms(query_text):
    """Quick search grooms by name or ID for autocomplete."""
    if grooms_col is None:
        return []
    try:
        results = list(
            grooms_col.find(
                {"$or": [
                    {"full_name": {"$regex": query_text, "$options": "i"}},
                    {"_id": {"$regex": query_text, "$options": "i"}},
                ]},
                {"_id": 1, "full_name": 1, "dob": 1, "birth_place": 1}
            ).limit(10)
        )
        return results
    except Exception:
        return []


# ─── Match Records ───────────────────────────────────────────────────────────

def save_match(bride_id, groom_id, bride_chart, groom_chart, porutham):
    """Save a match result referencing bride_id and groom_id."""
    if matches_col is None:
        return None

    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)

    record = {
        "_id": _generate_match_id(),
        "created_at": now.isoformat(),
        "bride_id": bride_id,
        "groom_id": groom_id,
        "bride_name": bride_chart.get("name", ""),
        "groom_name": groom_chart.get("name", ""),
        "bride_chart": bride_chart,
        "groom_chart": groom_chart,
        "porutham": porutham,
    }

    try:
        matches_col.insert_one(record)
        return record["_id"]
    except Exception as e:
        print(f"  ⚠ Failed to save match: {e}")
        return None


def get_match(match_id):
    """Retrieve a single match record by ID."""
    if matches_col is None:
        return None
    try:
        return matches_col.find_one({"_id": match_id})
    except Exception:
        return None


def get_all_matches(page=1, per_page=50):
    """Retrieve all match records ordered by newest first."""
    if matches_col is None:
        return [], 0

    try:
        total = matches_col.count_documents({})
        skip = (page - 1) * per_page
        records = list(
            matches_col.find({}, {
                "_id": 1, "created_at": 1,
                "bride_id": 1, "groom_id": 1,
                "bride_name": 1, "groom_name": 1,
                "porutham.score": 1, "porutham.total": 1,
                "porutham.verdict": 1,
            })
            .sort("created_at", -1)
            .skip(skip)
            .limit(per_page)
        )
        return records, total
    except Exception:
        return [], 0
