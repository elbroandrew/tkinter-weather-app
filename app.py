import traceback
from tkinter import *
from tkinter import messagebox
import requests


class App(Tk):

    def __init__(self, url: str, api_key: str):
        super().__init__()
        self.url = url
        self.api_key = api_key

    def get_weather_response(self, city: str) -> requests.Response:
        try:
            result: requests.Response = requests.get(self.url.format(city, self.api_key))
            if not result.status_code == 200:
                raise requests.exceptions.RequestException("status code is not OK or city name was not found.")

            return result

        except requests.exceptions.RequestException as e:
            messagebox.showerror('Ошибка', "Не могу найти город '{}'".format(city.capitalize()))
            print(e)

    def get_weather_dict_from_response(self, result) -> dict:

        json = result.json()

        return dict(
            city=json['name'],
            country=json['sys']['country'],
            temp=json['main']['temp'] - 273.15,
            icon=json['weather'][0]['icon'],
            weather=json['weather'][0]['description']
        )
