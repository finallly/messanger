import configparser

config = configparser.ConfigParser()
config.read('config.ini')


class ConfigHandler:
    file_in_mode = config['FILES']['file_in_mode']
    main_qss_file = config['FILES']['main_qss_file']
    main_form_file = config['FILES']['main_form_file']

    key = config['CONSTS']['key']
    digest = config['CONSTS']['digest']
    charset = config['CONSTS']['charset']
    host_address = config['CONSTS']['host']
    delimiter = config['CONSTS']['delimiter']
    super_key = config['CONSTS']['super_key']
    basic_port = int(config['CONSTS']['basic_port'])

    message = config['MESSAGE']['message']

    enter_key = int(config['KEYS']['Enter'])
