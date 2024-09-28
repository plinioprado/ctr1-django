""" settings """

from ledger1.utils.fileio import read_json

def get():
    """ get the settings as a dict """

    settings = read_json("./ledger1/settings.json")

    return settings
