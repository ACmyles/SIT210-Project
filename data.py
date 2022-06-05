import requests
import os

access_token = os.getenv('ACCESS_TOKEN')

x = requests.get(f"https://api.particle.io/v1/devices/e00fce68ecb0a7597d865534/soilSensor?access_token={access_token}")

x = x.json()

print(x['result'])
