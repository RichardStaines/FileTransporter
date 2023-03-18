import configparser
from datetime import datetime
import socket
import logging


# also initialises the logging
class ConfigFile:

    def __init__(self, filename):
        self.logging = False
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.config.read(filename)
        self.hostname = socket.gethostname()

        self.logfile = self.read_setting('LogFile', 'Logging', False) + datetime.now().strftime('-%Y%m%d.log')

        loglevel = self.read_setting('LogLevel', 'Logging', False)
        logging.basicConfig(format='%(asctime)s\t%(levelname)s\t%(message)s',
                            filename=self.logfile, encoding='utf-8', level=loglevel, filemode="a+")
        logging.info(f'Logging Level: {loglevel}')

    def read_setting(self, setting_name, section='Main', log_it=True):
        '''
        1st read host section - if not there then read Main
        :param setting_name: name of the setting
        :param section: section of config ini file
        :param log_it: write to log? default True
        :return:
        '''

        if setting_name in self.config[self.hostname].keys():
            value = self.config[self.hostname][setting_name]
            if log_it:
                logging.info(f'{self.hostname}.{setting_name} : {value}')
        else:
            value = self.config[section][setting_name]
            if log_it:
                logging.info(f'{section}.{setting_name} : {value}')

        return value
