""" settings """

from ctr1.utils.fileio import read_json

def get():
    """ get the settings as a dict """

    settings = read_json("./ctr1/settings.json")

    return settings
