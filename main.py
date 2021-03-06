from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests

url = "http://api.openweathermap.org/data/2.5/weather?q={}&lang=ru&appid={}"

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

img = None

def get_weather(city: str):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp = temp_kelvin - 273.15
        icon_img = json['weather'][0]['icon']
        weather = json['weather'][0]['description']
        final = dict(
            city=city,
            country=country,
            temp=temp,
            icon=icon_img,
            weather=weather
        )
        return final
    else:
        return None


app = Tk()
app.title("Погода")
app.geometry('350x400')


def search():
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        global img
        img = PhotoImage(file=r'img/{}@2x.png'.format(weather['icon']))
        location_lbl['text'] = '{}, {}'.format(weather['city'], weather['country'])
        temp_lbl['text'] = '{:.1f}°C'.format(weather['temp'])
        icon['image'] = img
        weather_lbl['text'] = weather['weather']
    else:
        messagebox.showerror('Ошибка', "Не могу найти город".format(city))


# info label
info_text = Text(app,
                 height=2,
                 width=40,
                 bg="light cyan",
                 wrap=WORD)
info_text.tag_configure("center", justify='center')
info_text.insert(1.0, "Введите название города и даже страны, пример: \"Рим, IT\" или просто \"Москва\".")
info_text.tag_add("center", 1.0, "end")
info_text.config(state='disabled')
info_text.pack()

# entry field
city_text = StringVar()  # object to set/get string
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

# search button
search_btn: Button = Button(app, text='Поиск', width=12, command=search)
search_btn.pack()

# label
location_lbl = Label(app, text='Город', font=('consolas', 32))
location_lbl.pack()

icon = Label(app, image="")
icon.pack()

temp_lbl = Label(app, text="")
temp_lbl.pack()

weather_lbl = Label(app, text="")
weather_lbl.pack()

if __name__ == '__main__':
    app.mainloop()
