import os
import requests
from oura_ring import OuraClient
from datetime import date
from dotenv import load_dotenv


def title() -> str:
    return date.today().strftime("%A")


def subtitle() -> str:
    today = date.today().isoformat()
    dt = date.today().strftime("%b %d %Y")

    weather = "??"
    weather_request = requests.get("https://wttr.in/?format=j1")
    if weather_request.status_code != 200:
        return ""
    weather_data = weather_request.json()["weather"]
    for day in weather_data:
        if day["date"] == today:
            weather = f"{day["maxtempC"]}°/{day["mintempC"]}°"

    _ = load_dotenv()
    OURA_PERSONAL_ACCESS_TOKEN = os.getenv("OURA_PERSONAL_ACCESS_TOKEN") or ""
    oura = OuraClient(OURA_PERSONAL_ACCESS_TOKEN)
    sleep = oura.get_daily_sleep(start_date=today)
    sleep_score = sleep[0]["score"] if len(sleep) > 0 else "N/A"
    readiness = oura.get_daily_readiness(start_date=today)
    readiness_score = readiness[0]["score"] if len(readiness) > 0 else "N/A"

    return f"{dt}\n{weather} • {sleep_score} • {readiness_score}\n"
