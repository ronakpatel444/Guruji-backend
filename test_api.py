import time
import requests
import json
import sys

# Ensure UTF-8 output encoding for Gujarati characters on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

url = "http://127.0.0.1:8000/api/v1/kundli/calculate"
payload = {
    "name": "Test User",
    "dob": "22/01/2006",
    "birth_place": "Surat, Gujarat",
    "birth_time": "07:05 AM",
    "language": "gu"
}
headers = {'Content-Type': 'application/json'}

print(f"Sending request to {url}...")
start_time = time.time()
try:
    response = requests.post(url, json=payload, headers=headers)
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"Status Code: {response.status_code}")
    print(f"Time Taken: {elapsed:.2f} seconds")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Request failed: {e}")
