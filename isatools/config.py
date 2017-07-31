from __future__ import absolute_import
from configparser import ConfigParser
import logging
import os

log_level = logging.INFO
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

    showpbars_ini = cparser.get('Logging', 'showprogressbars')
    if showpbars_ini.lower() == 'yes':
        show_pbars = True
    else:
        show_pbars = False

# Load default config from resources/isatools.ini
read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'isatools.ini'))
