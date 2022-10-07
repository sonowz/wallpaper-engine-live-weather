import json
import logging
import subprocess
import requests
import locale
import os
from pathlib import Path


OPENWEATHERMAP_API_URL = "https://api.openweathermap.org/data/2.5/weather"
OS_ENCODING = locale.getpreferredencoding()
BASE_PATH = Path(os.environ["PROGRAMDATA"]) / "WallpaperEngineLiveWeather"


logging.basicConfig(filename=BASE_PATH / "log.log", level=logging.DEBUG)


with open(BASE_PATH / "config.json") as config_file:
    CONFIG = json.load(config_file)


def get_weather(api_key, city, country=None):
    # https://openweathermap.org/find
    if country is None:
        url = "{url}?q={city}&appid={api_key}".format(
            url=OPENWEATHERMAP_API_URL, city=city, api_key=api_key
        )
    else:
        url = "{url}?q={city},{country}&appid={api_key}".format(
            url=OPENWEATHERMAP_API_URL, city=city, country=country, api_key=api_key
        )
    response = requests.get(url).json()
    # https://openweathermap.org/weather-conditions
    weathers = response["weather"]
    min_code = min(map(lambda x: x["id"], weathers))
    weather = list(filter(lambda x: x["id"] == min_code, weathers))[0]
    logging.debug(weather)
    return weather["main"]


def set_playlist(name):
    logging.debug(name)
    result = subprocess.run(
        [CONFIG["wallpaper_engine_bin"], "-control", "openPlaylist", "-playlist", name],
        check=False,
        capture_output=True,
        timeout=30,
    )
    logging.debug("Wallpaper engine returned code: " + str(result.returncode))
    logging.debug(result.stdout.decode(OS_ENCODING))
    if len(result.stderr) > 0:
        logging.error(result.stderr.decode(OS_ENCODING))


def main_loop():
    logging.debug("Start main loop")
    try:
        weather_raw = get_weather(CONFIG["api_key"], CONFIG["city"], CONFIG["country"])
        weather = CONFIG["weather_bindings"][weather_raw]
        playlist_name = CONFIG["playlist_prefix"] + weather
        set_playlist(playlist_name)
    except Exception:
        logging.exception("main loop error")
    logging.debug("End main loop")


if __name__ == "__main__":
    main_loop()
