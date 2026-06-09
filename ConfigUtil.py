import configparser
from pathlib import Path

filename = 'Config.ini'

def getConfig() -> configparser.ConfigParser:


    config = configparser.ConfigParser(allow_no_value=True)


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

def EnsureAliases(config:configparser.ConfigParser, cmds:list[str]):
    if 'Aliases' not in config:
        config['Aliases'] = {'# cmd = alias1 alias2 alias3': None}

        config['Aliases'].update(dict.fromkeys(cmds, ''))

        with open(filename, 'w') as file:
            config.write(file)
