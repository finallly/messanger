import configparser

config = configparser.ConfigParser()
config.read('config.ini')


class ConfigHandler:
    main_form_file = config['FILES']['main_form_file']
    main_qss_file = config['FILES']['main_qss_file']
    file_in_mode = config['FILES']['file_in_mode']

    charset = config['ARGS']['charset']

    enter_key = int(config['KEYS']['Enter'])

    host_message = config['MESSAGE']['host_message']
    client_message = config['MESSAGE']['client_message']
    new_connection_message = config['MESSAGE']['new_connection_message']
