""" Server Config """

import configparser

config = configparser.ConfigParser()

config['DEFAULT'] = {"Yes":"Yes",
                     "No":"No",
                     "Trial":"Correct",
                     "Hotel?":"Trivago"}

config['sachetallyisual'] = {}
config['sachetallyisual']['Name'] = 'Rob'

config['topsecrets!'] = {}
config['topsecrets!']['File'] = 'Lost'

with open('test.ini', 'w') as configfile:
    config.write(configfile)
