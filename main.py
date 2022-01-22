from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests


url = "http://api.openweathermap.org/data/2.5/weather?q={}&lang=ru&appid={}"

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']


def get_weather(city: str):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp = temp_kelvin - 273.15
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['description']
        final = dict(
            city=city,
            country=country,
            temp=temp,
            icon=icon,
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
    print(weather)
    if weather:
        location_lbl['text'] = '{}, {}'.format(weather['city'], weather['country'])
        temp_lbl['text'] = '{:.1f} C'.format(weather['temp'])
        weather_lbl['text'] = weather['weather']
    else:
        messagebox.showerror('Ошибка', "Не могу найти город".format(city))



# entry field
city_text = StringVar()  # object to set/get string
city_entry = Entry(app, textvariable=city_text).pack()

# search button
search_btn: Button = Button(app, text='Поиск', width=12, command=search).pack()

# label
location_lbl = Label(app, text='Город', font=('consolas', 32)).pack()

# image
# URL = "http://openweathermap.org/img/wn/10d@2x.png"
# response = requests.get(URL)
# if response.status_code == 200:
#     with open("sample.png", 'wb') as f:
#         f.write(response.content)

image = Label(app, bitmap='').pack()
# image['bitmap'] = ""

temp_lbl = Label(app, text="").pack()

weather_lbl = Label(app, text="").pack()

if __name__ == '__main__':
    app.mainloop()
