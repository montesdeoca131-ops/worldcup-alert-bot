import os
import time
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
API_KEY = os.getenv("API_FOOTBALL_KEY")

HEADERS = {
    "x-apisports-key": API_KEY
}

seen = {}

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": CHANNEL_ID,
            "text": text
        }
    )

def check_matches():
    url = "https://v3.football.api-sports.io/fixtures"

    params = {
        "league": 1,
        "season": 2026,
        "live": "all"
    }

    r = requests.get(url, headers=HEADERS, params=params)

    if r.status_code != 200:
        print("API ERROR:", r.text)
        return

    data = r.json().get("response", [])

    for match in data:

        fixture_id = match["fixture"]["id"]

        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]

        home_score = match["goals"]["home"] or 0
        away_score = match["goals"]["away"] or 0

        status = match["fixture"]["status"]["short"]

        current_state = f"{status}-{home_score}-{away_score}"

        if fixture_id not in seen:
            seen[fixture_id] = current_state

            if status == "1H":
                send_telegram(
                    f"🟢 LIVE\n\n{home} vs {away}\n\nMatch Started"
                )

            continue

        if seen[fixture_id] != current_state:

            if status in ["1H", "2H"]:
                send_telegram(
                    f"⚽ GOAL\n\n{home} {home_score}-{away_score} {away}"
                )

            elif status == "HT":
                send_telegram(
                    f"⏸ HALFTIME\n\n{home} {home_score}-{away_score} {away}"
                )

            elif status == "FT":
                send_telegram(
                    f"🏁 FINAL\n\n{home} {home_score}-{away_score} {away}"
                )

            seen[fixture_id] = current_state

while True:
    try:
        check_matches()
    except Exception as e:
        print("ERROR:", e)

    time.sleep(900)