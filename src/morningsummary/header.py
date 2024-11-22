import os
import requests
from oura_ring import OuraClient
from datetime import datetime, date
from dotenv import load_dotenv


def title() -> str:
    return datetime.now().strftime("%A\n%b %d %Y")


def subtitle() -> str:
    today = date.today().isoformat()

    weather = requests.get("https://wttr.in/?format=j1")
    if weather.status_code != 200:
        return ""
    weather = weather.json()["weather"][0]
    if weather["date"] != today:
        weather = f"??"
    else:
        weather = f"{weather["maxtempC"]}°/{weather["mintempC"]}°"

    _ = load_dotenv()
    OURA_PERSONAL_ACCESS_TOKEN = os.getenv("OURA_PERSONAL_ACCESS_TOKEN") or ""
    oura = OuraClient(OURA_PERSONAL_ACCESS_TOKEN)
    sleep = oura.get_daily_sleep(start_date=today)
    sleep_score = sleep[0]["score"] if len(sleep) > 0 else "N/A"
    readiness = oura.get_daily_readiness(start_date=today)
    readiness_score = readiness[0]["score"] if len(readiness) > 0 else "N/A"

    return f"🌤️ {weather} • 🛏️ {sleep_score} • 🌱 {readiness_score}"
