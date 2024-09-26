""" settings """

from ledger1.util.fileio import read_json

def get():
    """ get the settings as a dict """

    settings = read_json("./ledger1/settings.json")

    return settings
