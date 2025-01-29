"""
Account version of Document class
"""

from dataclasses import dataclass
from ledger1.document.document import Document


@dataclass
class DocumentAccount(Document):

    def __init__(self, db_id, doc_type, doc_num = None) -> None:
        self.db_id = db_id
        self.doc_type = doc_type
        self.doc_num = doc_num
        self.descr = None

        self.acc = {}
        self.fields = {}
        self.seqs: list[dict] = []


    def set_from_account(self, acc: dict) -> None:
        self.acc = {
            "num": acc["num"],
            "name": acc["name"],
            "dc": acc["dc"]
        }

    def set_from_new(self) -> None:
        # self.doc_type maintain init
        self.doc_num = ""

        self.acc = {
            "num": "",
            "name": "",
            "dc": None,
        }
        self.fields = {}
        self.seqs = []


    def set_from_request(self, data: dict) -> None:

        if data["doc_type"] != self.doc_type:
            raise ValueError("Document type does not match")
        self.doc_num = data["doc_num"]

        self.acc = {
            "name": data["descr"],
            "num": data["acc_num"],
            "dc": data["acc_num"][0] == "1"
        }

        if "fields" in data.keys():
            self.fields = data["fields"]


    def set_from_fields(self, fields: dict):
        self.fields = fields


    def get_to_account(self):
        return {
            "num": self.acc["num"],
            "name": self.acc["name"],
            "dc": self.acc["dc"],
            "doc_type": self.doc_type,
            "doc_num": self.doc_num
        }


    def get_to_response(self):
        return {
            "doc_type": self.doc_type,
            "doc_num": self.doc_num,
            "descr": self.acc["name"],
            "acc_num": self.acc["num"],
            "fields": self.fields,
            "seqs": self.seqs
        }
