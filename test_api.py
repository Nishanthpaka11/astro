import requests
import json

url = "http://localhost:5000/api/generate-chart"
data = {
    "name": "Test User",
    "dob": "1990-01-01",
    "time": "12:00",
    "place": "Chennai"
}

try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
