import configparser
from pathlib import Path

def getConfig() -> configparser.ConfigParser:

    filename = 'Config.ini'
    config = configparser.ConfigParser()


    #if config does not exist, create a blank config file
    if not Path(filename).is_file():

        config['General'] = {
            'Token': '-1',
            'Prefix': '.'

        }

        with open(filename, 'w') as file:
            config.write(file)

    config.read(filename)
    return config