"""
வ உ சி யின் உறவைத் தேடி — MongoDB Database Module
Handles connection, saving and retrieving customer records.
"""

from pymongo import MongoClient
from datetime import datetime
import pytz
import os


# ─── MongoDB Connection ──────────────────────────────────────────────────────

MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://yisagi868_db_user:47424742@cluster0.knihcws.mongodb.net/")
DB_NAME = "thirukanidham"
COLLECTION_NAME = "customers"

client = None
db = None
collection = None


def init_db():
    """Initialize MongoDB connection."""
    global client, db, collection
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # Test connection
        client.server_info()
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        print(f"  ✔ MongoDB Atlas connected: {DB_NAME}")
        return True
    except Exception as e:
        print(f"  ⚠ MongoDB not available: {e}")
        print(f"    Records will NOT be saved.")
        return False


def _generate_id():
    """Generate a unique customer ID in format TK-YYYYMMDD-NNN."""
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    date_str = now.strftime('%Y%m%d')
    prefix = f"TK-{date_str}"

    if collection is None:
        return f"{prefix}-001"

    # Count today's records to get the next sequence number
    count = collection.count_documents({"_id": {"$regex": f"^{prefix}"}})
    seq = str(count + 1).zfill(3)
    return f"{prefix}-{seq}"


def save_customer(bride_data, groom_data, bride_chart, groom_chart, porutham):
    """Save a customer record to MongoDB."""
    if collection is None:
        return None

    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)

    record = {
        "_id": _generate_id(),
        "created_at": now.isoformat(),
        "bride": {
            "name": bride_data.get("name", ""),
            "dob": bride_data.get("dob", ""),
            "time": bride_data.get("time", ""),
            "place": bride_data.get("place", ""),
            "height": bride_data.get("height", ""),
            "weight": bride_data.get("weight", ""),
            "salary": bride_data.get("salary", "")
        },
        "groom": {
            "name": groom_data.get("name", ""),
            "dob": groom_data.get("dob", ""),
            "time": groom_data.get("time", ""),
            "place": groom_data.get("place", ""),
            "height": groom_data.get("height", ""),
            "weight": groom_data.get("weight", ""),
            "salary": groom_data.get("salary", "")
        },
        "bride_chart": bride_chart,
        "groom_chart": groom_chart,
        "porutham": porutham
    }

    try:
        collection.insert_one(record)
        return record["_id"]
    except Exception as e:
        print(f"  ⚠ Failed to save record: {e}")
        return None


def get_customer(customer_id):
    """Retrieve a single customer record by ID."""
    if collection is None:
        return None
    try:
        return collection.find_one({"_id": customer_id})
    except Exception:
        return None


def get_all_customers(page=1, per_page=50):
    """Retrieve all customer records ordered by newest first."""
    if collection is None:
        return [], 0

    try:
        total = collection.count_documents({})
        skip = (page - 1) * per_page
        records = list(
            collection.find({}, {
                "_id": 1,
                "created_at": 1,
                "bride.name": 1,
                "groom.name": 1,
                "porutham.score": 1,
                "porutham.total": 1
            })
            .sort("created_at", -1)
            .skip(skip)
            .limit(per_page)
        )
        return records, total
    except Exception:
        return [], 0
