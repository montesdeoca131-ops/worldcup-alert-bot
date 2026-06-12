import os
import requests

API_KEY = os.getenv("API_FOOTBALL_KEY")

headers = {
    "x-apisports-key": API_KEY
}

response = requests.get(
    "https://v3.football.api-sports.io/leagues?search=World Cup",
    headers=headers
)

data = response.json()

for league in data["response"]:
    print(
        league["league"]["id"],
        league["league"]["name"]
    )