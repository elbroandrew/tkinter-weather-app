from tkinter import *
from tkinter import messagebox
import requests
from time import strftime
from datetime import date


class App(Tk):

    def __init__(self, url: str, api_key: str):
        super().__init__()
        self._color = "#e3dcde"
        self.url = url
        self.api_key = api_key
        self.pady = (10, 10)
        self.city_text = StringVar()
        self.img = None
        self.button_text = "Поиск"
        self.location_lbl = Label(self, text='Город', font=('consolas', 32), relief="groove", bg=self._color)
        self.temp_lbl = Label(self, text="", font=('arial', 22), bg=self._color)
        self.icon = Label(self, bg=self._color)
        self.weather_lbl = Label(self, text="", bg=self._color)
        self.search_button = Button(self, text=self.button_text, width=12, command=self.search)
        self.city_entry = Entry(self, textvariable=self.city_text, width=30, font=("arial", 12), justify="center")
        self.title("Погода")
        self.geometry('350x400')
        self.resizable(False, False)
        self.configure(bg=self._color)
        self.kelvin = 273.15
        self.curr_date = None
        self.string_clock = None
        self.clock_label = Label(self, font=('calibri', 14, 'bold'), bg=self._color, foreground='blue')

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

        if result:
            json = result.json()

            return dict(
                city=json['name'],
                country=json['sys']['country'],
                temp=json['main']['temp'] - self.kelvin,
                icon=json['weather'][0]['icon'],
                weather=json['weather'][0]['description']
            )

    def create_info_text(self) -> Text:
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
        self.create_info_text().pack()
        self.city_entry.pack(pady=self.pady, ipady=5)
        self.search_button.pack(pady=self.pady)
        self.location_lbl.pack()
        self.clock_label.pack()
        self.icon.pack()
        self.temp_lbl.pack()
        self.weather_lbl.pack()

    def search(self):
        city: str = self.city_text.get()
        res = self.get_weather_response(city)
        weather = self.get_weather_dict_from_response(res)
        if weather:
            self.img = PhotoImage(file=r'img/{}@2x.png'.format(weather['icon']))
            self.location_lbl['text'] = '{}, {}'.format(weather['city'], weather['country'])
            self.temp_lbl['text'] = '+{:.1f}°C'.format(weather['temp']) if weather['temp'] > 0 else '{:.1f}°C'.format(
                weather['temp'])
            self.icon['image'] = self.img
            self.weather_lbl['text'] = weather['weather']

        self.clear_city_text_field()

    def clear_city_text_field(self):
        self.city_entry.delete(0, END)

    def ttime(self):
        self.string_clock = strftime('%H:%M:%S %p')
        self.clock_label.config(text=self.string_clock)
        self.clock_label.after(1000, self.ttime)
