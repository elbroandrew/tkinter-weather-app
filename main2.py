from app import App
from configparser import ConfigParser
import requests

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

url = "http://api.openweathermap.org/data/2.5/weather?q={}&lang=ru&appid={}"


if __name__ == '__main__':
    app = App(url, api_key)
    app.pack_all_widgets()
    app.title("Погода")
    app.geometry('350x400')
    app.resizable(False, False)
    app.configure(bg=app._color)
    app.mainloop()
