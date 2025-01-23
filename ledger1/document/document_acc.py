"""
Account version of Document class
"""

from dataclasses import dataclass
from ledger1.document.document import Document


@dataclass
class DocumentAccount(Document):

    def __init__(self, document_type: dict):
        self.doc_type = document_type["id"]
        self.doc_num = None
        self.doc_dc = None
        self.doc_type_name = document_type["name"]
        self.descr = None

        self.acc_num = None
        self.acc_name = None
        self.acc_dc = None

        self.fields = {}


    def set_from_request(self, data: dict):

        if data["doc_type"] != self.doc_type:
            raise ValueError("Document type does not match")
        self.doc_num = data["doc_num"]
        self.descr = data["descr"]

        self.acc_num = data["acc_num"]
        self.acc_name = f"{data['doc_type']} {data['doc_num']}"
        self.acc_dc = data["acc_num"][0] == "1"

        if "fields" in data.keys():
            self.fields = data["fields"]


    def get_to_account(self):
        return {
            "num": self.acc_num,
            "name": self.acc_name,
            "dc": self.acc_dc,
            "doc_type": self.doc_type,
            "doc_num": self.doc_num
        }
