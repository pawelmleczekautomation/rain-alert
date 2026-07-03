import os
import requests
from twilio.rest import Client

OWM_API_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
FORECAST_COUNT = 4
LAST_RAIN_ID = 531

OWM_API_KEY = os.environ.get("OWM_API_KEY")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

TARGET_LOCATION = os.environ.get("TARGET_LOCATION")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
TARGET_NUMBER = os.environ.get("TARGET_NUMBER")

params = {
    "q": TARGET_LOCATION,
    "appid": OWM_API_KEY,
    "cnt": FORECAST_COUNT,
}

response = requests.get(OWM_API_ENDPOINT, params=params)
response.raise_for_status()

data = response.json()
forecast_list = data["list"]

f_will_rain = False
for forecast_dict_entry in forecast_list:
    weather_id = forecast_dict_entry["weather"][0]["id"]
    if int(weather_id) <= LAST_RAIN_ID:
        f_will_rain = True

if f_will_rain:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella!.",
        from_=TWILIO_PHONE_NUMBER,
        to=TARGET_NUMBER,
    )
    print(message.sid)
    print(message.status)
    
