import configparser

config = configparser.ConfigParser()
config.read('config.ini')


class ConfigHandler:
    main_form_file = config['FILES']['main_form_file']
    main_qss_file = config['FILES']['main_qss_file']
    file_in_mode = config['FILES']['file_in_mode']

    charset = config['ARGS']['charset']
    host_address = config['ARGS']['host']

    enter_key = int(config['KEYS']['Enter'])

    message = config['MESSAGE']['message']
