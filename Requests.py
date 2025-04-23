import requests
import json

# Your endpoint URL
url = 'http://localhost:8000/api/new-ticket/'  # Adjust if your server is running elsewhere

# Data to send
data = {
    "duration": 60,
    "price": 2.50,
    "totem_id": "totem_321",  # Make sure this totem exists in your database
    "plate": "AB123CD"
}

# Headers
headers = {
    'Content-Type': 'application/json',
}

try:
    # Send POST request
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Check if response is successful
    if response.status_code == 200:
        try:
            print("Response:", response.json())
        except ValueError:
            print("Received empty or invalid JSON response")
            print("Raw response:", response.text)
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response:", response.text)

except requests.exceptions.RequestException as e:
    print("Request failed:", e)