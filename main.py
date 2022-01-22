from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests

url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

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
        temp_celsius = temp_kelvin - 273.15
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        final = (city, country, temp_celsius, icon, weather)
        return final
    else:
        return None


print(get_weather("London"))

app = Tk()
app.title("Weather app")
app.geometry('700x350')


def search():
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        pass
    else:
        messagebox.showerror('Ошибка', "Не могу найти город".format(city))



# entry field
city_text = StringVar()  # object to set/get string
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

# search button
search_btn: Button = Button(app, text='Search weather', width=12, command=search)
search_btn.pack()

# label
location_lbl = Label(app, text='Location', font=('consolas', 20))
location_lbl.pack()

# image
image = Label(app, bitmap='')
image.pack()

temp_lbl = Label(app, text="")
temp_lbl.pack()

weather_lbl = Label(app, text="")
weather_lbl.pack()

if __name__ == '__main__':
    app.mainloop()
