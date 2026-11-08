import json
import requests
from typing import Annotated, Optional
import typer
import os
import subprocess

app = typer.Typer(help="Weather app")

@app.command()
def main(zipcode: Annotated[str, typer.Argument()] = 98225):
    # goes to zippopatam to get the lat and long
    zipp_return = requests.get("http://api.zippopotam.us/us/" + zipcode)
    zipp_data = json.loads(zipp_return.text)
    lat = zipp_data["places"][0]["latitude"]
    long = zipp_data["places"][0]["longitude"]

    # got to api weather gov and gets forecast
    weather_return = requests.get("https://api.weather.gov/points/" + lat + "," + long)
    weather_data = json.loads(weather_return.text)
    forecast_url = weather_data["properties"]["forecast"]
    forecast_return = requests.get(forecast_url)
    forecast_data = json.loads(forecast_return.text)
    forecast = forecast_data["properties"]["periods"][0]["detailedForecast"]

    print("-" * 30)
    print(forecast)

    if typer.confirm("\n" + "Would you like the forecast for the week?"):

        # get a high and low for the week and print it
        avg = get_avg_temp(forecast_data)
        days_rain = get_rain_days(forecast_data)
        week_forecast = "\n" + "-" * 30 + "\n"
        week_forecast += "This week's average temp is " + str(round(avg)) + "F. "
        week_forecast +=  "It will likely rain " + str(days_rain) + "/7 days out of the week." + "\n" * 2
        week_forecast += "Today: " + forecast_data["properties"]["periods"][0]["detailedForecast"]

        for i in range(2, 14):
            if "Night" not in forecast_data["properties"]["periods"][i]["name"]:
                week_forecast += "\n" * 2
                week_forecast += forecast_data["properties"]["periods"][i]["name"] + ": "
                week_forecast += forecast_data["properties"]["periods"][i]["detailedForecast"]

        print(week_forecast)

def get_avg_temp(json):

    temp_total = 0

    for i in range(2, 14):
        if "Night" not in json["properties"]["periods"][i]["name"]:
            temp_total += json["properties"]["periods"][i]["temperature"]

    return temp_total / 7


def get_rain_days(json):
    rainy_days = 0

    if (json["properties"]["periods"][0]["probabilityOfPrecipitation"]["value"] > 35):
        rainy_days += 1

    for i in range(2, 14):
        if "Night" not in json["properties"]["periods"][i]["name"]:
            rain_chance = json["properties"]["periods"][i]["probabilityOfPrecipitation"]["value"]
            if (rain_chance > 20):
                rainy_days += 1
    return rainy_days


def clear():
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, shell=True)



if __name__ == "__main__":
    app()