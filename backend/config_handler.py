import configparser

config = configparser.ConfigParser()
config.read('config.ini')


class ConfigHandler:
    main_form_file = config['FILES']['main_form_file']

    charset = config['ARGS']['charset']

    enter_key = int(config['KEYS']['Enter'])

    message = config['MESSAGE']['message']
