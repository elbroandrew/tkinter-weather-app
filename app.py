from tkinter import *
from tkinter import messagebox
import requests
from time import strftime
import logging
from countries import countries
import csv


class App(Tk):
    logger = logging.getLogger()

    def __init__(self, url: str, api_key: str):
        super().__init__()
        self._color = "#e3dcde"
        self.url = url
        self.api_key = api_key
        self.cities = self.load_city_from_csv()  # ["moscow", "tomsk", "хабаровск"]
        self.pady = (10, 10)
        self.city_text = StringVar()
        self.img = None
        self.button_text = "Поиск"
        self.temp_lbl = Label(self, text="", font=('arial', 22), bg=self._color)
        self.icon = Label(self, bg=self._color)
        self.weather_lbl = Label(self, text="", font=('calibri', 18), bg=self._color)
        self.search_button = Button(self, text=self.button_text, width=12,
                                    command=lambda: self.search(self.city_entry.get().strip()))
        self.city_entry = Entry(self, textvariable=self.city_text, width=30, font=("calibri", 14), justify="center")
        self.day_night_label = Label(self, bg=self._color, fg="steel blue", font=('calibri', 18))
        self.location_lbl = Message(self, text='Город', font=('consolas', 30),
                                    width=400, justify="center", bg=self._color)
        self.om_default = StringVar()
        self.option_menu = OptionMenu(self, self.om_default, *self.cities,
                                      command=self.option_menu_reset)
        self.title("Погода")
        self.geometry('450x560')
        self.resizable(False, False)
        self.configure(bg=self._color)
        self.kelvin = 273.15
        self.curr_date = strftime("%d-%b-%Y")
        self.string_clock = None
        self.clock_label = Label(self, font=('calibri', 14, 'bold'), bg=self._color, foreground='blue')
        self.bind("<Return>", (lambda event: self.search(self.city_text.get().strip())))
        App.logger.setLevel(logging.DEBUG)

    def get_weather_response(self, city: str) -> requests.Response:
        try:
            resp: requests.Response = requests.get(self.url.format(city, self.api_key))
            if not resp.status_code == 200:
                raise requests.exceptions.RequestException("status code is not OK or city name was not found.")

            return resp
        except requests.exceptions.RequestException as e:
            App.logger.error(str(e), exc_info=True)
            messagebox.showerror('Ошибка', "Не могу найти город '{}'".format(city.capitalize()))

    def get_weather_dict_from_response(self, result) -> dict:

        try:
            if not result:
                raise requests.exceptions.InvalidJSONError("result is None")

            json = result.json()

            return dict(
                city=json['name'],
                country=countries[json['sys']['country']],
                temp=json['main']['temp'] - self.kelvin,
                icon=json['weather'][0]['icon'],
                weather=json['weather'][0]['description']
            )

        except requests.exceptions.InvalidJSONError as e:
            App.logger.error(str(e), exc_info=True)

    def create_info_text(self) -> Text:
        info_text = Text(self,
                         height=2,
                         width=50,
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
        self.option_menu.place(x=390, y=50)
        self.search_button.pack(pady=self.pady)
        self.location_lbl.pack()
        self.clock_label.pack()
        self.day_night_label.pack()
        self.icon.pack()
        self.temp_lbl.pack()
        self.weather_lbl.pack()

    def option_menu_reset(self, value):
        self.city_entry.delete(0, END)
        self.city_entry.insert(0, value)
        self.om_default.set("")

    def update_option_menu(self):
        menu = self.option_menu["menu"]
        menu.delete(0, END)
        for string in self.cities:
            menu.add_command(label=string, command=lambda value=string: self.om_default.set(value))

    def dump_city_to_csv_db(self):
        with open("db.csv", 'w') as csv_file:
            csv.writer(csv_file, delimiter='\n').writerow(self.cities)

    def make_widgets(self, weather):
        self.img = PhotoImage(file=r'img/{}@2x.png'.format(weather['icon']))
        self.location_lbl['text'] = '{}, {}'.format(weather['city'], weather['country'])
        self.temp_lbl['text'] = '+{:.1f}°C'.format(weather['temp']) if weather['temp'] > 0 else '{:.1f}°C'.format(
            weather['temp'])
        self.temp_lbl.configure(relief="groove", pady=5, padx=5)
        self.icon['image'] = self.img
        self.day_night_label.configure(text="День" if "d" in weather['icon'] else "Ночь")
        self.weather_lbl['text'] = weather['weather']

    def search(self, city: str):
        if city is not None:
            resp = self.get_weather_response(city)
            weather = self.get_weather_dict_from_response(resp)
            if weather:
                self.city_entry.insert(END, city)
                if not city.lower() in self.cities:
                    self.cities.insert(0, city.lower())
                    if len(self.cities) > 3:
                        self.cities = self.cities[:3]
                    self.update_option_menu()
                self.make_widgets(weather)

        self.clear_city_text_field()

    def clear_city_text_field(self):
        self.city_entry.delete(0, END)

    @classmethod
    def create_new_cities_list(cls, cities_list: list) -> list:
        return [x[0] for idx, x in enumerate(cities_list) if len(x) > 0 and idx < 3]

    @classmethod
    def load_city_from_csv(cls):

        with open("db.csv") as csv_file:
            csv_reader = csv.reader(csv_file)
            cities = []
            for row in csv_reader:
                cities.append(row)

            return cls.create_new_cities_list(cities)

    def ttime(self):
        self.string_clock = strftime('%H:%M:%S')
        self.clock_label.config(text="{}, {}".format(self.curr_date, self.string_clock))
        self.clock_label.after(1000, self.ttime)

    def __enter__(self):
        self.search(self.cities[0])
        self.pack_all_widgets()
        self.ttime()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dump_city_to_csv_db()
