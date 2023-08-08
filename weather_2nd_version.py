import requests
from datetime import datetime, timedelta
import csv


API_URL = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}"
latitude = 53.331
longitude = -6.2489


class WeatherForecast:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self):
        try:
            with open(self.file_path, "r") as file:
                return dict(csv.reader(file))
        except FileNotFoundError:
            return {}

    def _save_data(self):
        with open(self.file_path, "w", newline="") as file:
            csv_writer = csv.writer(file)
            for date, precipitation_sum in self.data.items():
                csv_writer.writerow([date, precipitation_sum])

    def __setitem__(self, date, weather):
        self.data[date] = weather
        self._save_data()

    def __getitem__(self, date):
        return self.data.get(date)

    def __iter__(self):
        return iter(self.data)

    def items(self):
        return self.data.items()

def get_next_day(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    next_day = date + timedelta(days=1)
    return next_day.strftime("%Y-%m-%d")

searched_date = input("Provide a date to check the weather (YYYY-mm-dd): ")

if not searched_date:
    searched_date = get_next_day(datetime.now().strftime("%Y-%m-%d"))

weather_forecast = WeatherForecast("weather_data.csv")

if searched_date in weather_forecast:
    precipitation_sum = float(weather_forecast[searched_date])
else:
    response = requests.get(API_URL.format(latitude=latitude, longitude=longitude, searched_date=searched_date))
    json_response = response.json()
    if 'daily' in json_response:
        daily_data = json_response['daily']
        precipitation_sum = daily_data['precipitation_sum'][0]
        if precipitation_sum > 0.0:
            weather_forecast[searched_date] = precipitation_sum
    else:
        precipitation_sum = -1

if precipitation_sum > 0.0:
    print(f"It will rain. Precipitation Sum: {precipitation_sum}")
elif precipitation_sum == 0.0:
    print("It will not rain.")
else:
    print("I don't know.")
