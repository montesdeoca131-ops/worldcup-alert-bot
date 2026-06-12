import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
API_KEY = os.getenv("API_FOOTBALL_KEY")

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

params = {
    "league": 1,
    "season": 2026
}

r = requests.get(url, headers=headers, params=params)

message = f"⚽ FIFA World Cup Check\n\nStatus: {r.status_code}"

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

response = requests.post(
    telegram_url,
    json={
        "chat_id": CHANNEL_ID,
        "text": message
    }
)

print(response.text)