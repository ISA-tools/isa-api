from __future__ import absolute_import
from configparser import ConfigParser
import logging
import os

show_pbars = False


# Read a .ini config to set up some global defaults
def read(path):
    global log_level
    global show_pbars
    cparser = ConfigParser()
    cparser.read(path)
    log_level_ini = cparser.get('Logging', 'loglevel')
    if log_level_ini.lower() == 'warning':
        log_level = logging.WARNING
    elif log_level_ini.lower() == 'debug':
        log_level = logging.DEBUG
    elif log_level_ini.lower() == 'error':
        log_level = logging.ERROR
    elif log_level_ini.lower() == 'critical':
        log_level = logging.CRITICAL
    else:
        log_level = logging.INFO
    log_format = "%(asctime)s [%(levelname)s]: %(filename)s(%(funcName)s:%(lineno)s) >> %(message)s"
    logging.basicConfig(format=log_format)
    set_level(log_level=log_level)

    showpbars_ini = cparser.get('Logging', 'showprogressbars')
    if showpbars_ini.lower() == 'yes':
        show_pbars = True
    else:
        show_pbars = False


def set_level(log_level):
    if log_level in (logging.NOTSET, logging.DEBUG, logging.INFO,
                     logging.WARNING, logging.ERROR, logging.CRITICAL):
        logging.getLogger('isatools').setLevel(log_level)

# Load default config from resources/isatools.ini
read(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'resources', 'isatools.ini'))
