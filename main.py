from app import App
from configparser import ConfigParser
import locale
locale.setlocale(locale.LC_ALL, "ru")

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

url = "http://api.openweathermap.org/data/2.5/weather?q={}&lang=ru&appid={}"


if __name__ == '__main__':
    with App(url, api_key) as app:
        app.mainloop()

