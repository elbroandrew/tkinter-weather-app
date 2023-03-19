from app import App
from configparser import ConfigParser

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']


if __name__ == '__main__':
    app = App("url", api_key)
    app.pack_all_widgets()
    app.mainloop()
