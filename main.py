import os
import requests

API_KEY = os.getenv("API_FOOTBALL_KEY")

headers = {
    "x-apisports-key": API_KEY
}

response = requests.get(
    "https://v3.football.api-sports.io/fixtures?live=all",
    headers=headers
)

print(response.text)