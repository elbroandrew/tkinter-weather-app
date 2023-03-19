from tkinter import *
from tkinter import messagebox
import requests


class App(Tk):
    _bg_color = "#e3dcde"

    def __init__(self, url: str, api_key: str):
        super().__init__()
        self.url = url
        self.api_key = api_key
        self.widgets = []

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

    def create_info_text(self):
        info_text = Text(self,
                         height=2,
                         width=40,
                         bg="light cyan",
                         wrap=WORD)
        info_text.tag_configure("center", justify='center')
        info_text.insert(1.0, "Введите название города и даже страны, пример: \"Рим, IT\" или просто \"Москва\".")
        info_text.tag_add("center", 1.0, "end")
        info_text.config(state='disabled')

        return info_text



    def pack_all_widgets(self):
        """
        Create all widgets here and draw them
        """
        self.widgets.append(self.create_info_text())

        for w in self.widgets:
            w.pack()
