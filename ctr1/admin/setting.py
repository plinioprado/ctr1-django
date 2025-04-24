from dataclasses import dataclass
from ctr1.admin.aux import Aux

@dataclass
class Setting(Aux):

    def __init__(self) -> None:

        # fields
        self.key = ""
        self.value = ""

        # db
        self.table_name = "setting"
        self.primary_key = "setting_key"
        self.filter_field = "setting_key"
        self.primary_key_form = "key"


    def set_from_db(self, data):
        self.key = data["setting_key"]
        self.value = data["setting_value"]


    def set_from_request(self, data):
        self.key = data["key"]
        self.value = data["value"]


    def get_to_db(self):
        return {
            "setting_key": self.key,
            "setting_value": self.value
        }


    def get_to_response(self):
        return {
            "key": self.key,
            "value": self.value
        }


    def get_to_response_list(self):
        return {
            "key": self.key,
            "value": self.value
        }


    def get_to_response_new(self):
        return {
            "key": self.key,
            "value": self.value
        }


    @classmethod
    def get_db_format(cls):
        return {
            "setting_key": "str",
            "setting_value": "str",
        }
