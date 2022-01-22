from tkinter import *
from Api_key import API_KEY

app = Tk()
app.title("Weather app")
app.geometry('700x350')

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()



if __name__ == '__main__':
    app.mainloop()
