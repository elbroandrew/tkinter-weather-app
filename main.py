from tkinter import *

url = 'api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}'

app = Tk()
app.title("Weather app")
app.geometry('700x350')


def search():
    pass

# entry field
city_text = StringVar() # object to set/get string
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
