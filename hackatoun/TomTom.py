

#Ce script Python utilise l'API Directions de Google Maps pour obtenir les itinéraires entre deux endroits (origine et destination), en tenant compte des conditions de trafic actuelles.
#L'API TomTom



import requests
import time
from json import dumps

# Replace YOUR_API_KEY with your own Google Maps API key
api_key = "your_key_here"

# Set the endpoint URL for the Directions API
endpoint = "https://maps.googleapis.com/maps/api/directions/json?"

# Set the origin and destination for the Directions API request
origin = "Toronto"
destination = "Montreal"

# Set the traffic model to "best_guess"
traffic_model = "best_guess"

departure_time = int(time.time())

# Build the URL for the Directions API request
url = endpoint + f"origin={origin}&destination={destination}&traffic_model={traffic_model}&departure_time={departure_time}&key={api_key}"

print(url)
# Send the request to the Directions API
response = requests.get(url)

# Retrieve the estimated travel time based on current traffic conditions
data = response.json()

dumps(data, indent=2)
# print(data)
# time_in_traffic = data["routes"][0]["legs"][0]["duration_in_traffic"]["text"]

# print(f"The estimated travel time with current traffic is {time_in_traffic}")