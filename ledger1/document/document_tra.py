"""
Transaction version of Document class
"""

from dataclasses import dataclass
from ledger1.document.document import Document
from ledger1.document.document_tra_seq import DocumentSeq

@dataclass
class DocumentTransaction(Document):

    def __init__(
            self,
            db_id: str,
            doc_type: dict,
            doc_dc: bool,
            tra_num: str,
            document_type: dict,
            op_seq_acc: list[dict]):

        self.db_id = db_id
        self.doc_type = doc_type
        self.doc_dc = doc_dc
        self.num_on_seq = document_type["num_on_seq"]
        self.op_seq_acc = op_seq_acc

        # to be set later
        self.doc_num = None
        self.descr = None
        self.tra_num = None
        self.dt = None

        self.fields = {}
        self.seqs: list[dict] = []


    def set_from_new(self):
        # self.doc_type maintain init
        # self.doc_dc maintain init
        self.doc_num = ""
        self.dt = ""
        self.descr = ""
        self.seqs: list[DocumentSeq] = [
        DocumentSeq(
            type="base",
            text="",
            acc="",
            val=0.0
        ),
        DocumentSeq(
            type="tot",
            text="",
            acc="",
            val=0.0
        ),
    ]


    def set_from_fields(self, fields: dict):
        self.fields = fields


    def set_from_request(self, data, op_seq_acc):
        # self.doc_type maintain init
        # self.doc_dc maintain init
        self.doc_num = data["doc_num"]
        self.dt = data["dt"]
        self.descr = data["descr"]

        self.fields = data["fields"]

        self.seqs = []
        for op in op_seq_acc:
            doc_seq: dict = [seq for seq in data["seqs"] if seq["acc"] == op["acc"]]

            if not doc_seq:
                continue

            self.seqs.append(DocumentSeq(
                type=str(op["type"]),
                text=str(op["text"]),
                acc=str(op["acc"]),
                val=float(doc_seq[0]["val"])
            ))


    def set_from_transaction(self, tra: dict, op_seq_acc: list[dict]):

        self.dt = tra["date"]
        self.descr = tra["descr"]
        self.tra_num = tra["num"]

        self.seqs = []
        for op in op_seq_acc:
            tra_seq: dict = [seq for seq in tra["seqs"] if seq["account"] == op["acc"]]
            if tra_seq == []:
                continue

            self.seqs.append(DocumentSeq(
                type=op["type"],
                text=op["text"],
                acc=tra_seq[0]["account"],
                val=tra_seq[0]["val"]
            ))

            if self.num_on_seq == op["type"]:
                self.doc_type = tra_seq[0]["doc"]["type"]
                self.doc_num = tra_seq[0]["doc"]["num"]
                self.doc_dc = tra_seq[0]["dc"]


    def get_to_response(self):
        return {
            "doc_type": self.doc_type,
            "doc_num": self.doc_num,
            "doc_dc": self.doc_dc,
            "dt": self.dt,
            "descr": self.descr,
            "fields": self.fields,
            "seqs": [seq.asdict() for seq in self.seqs],

        }


    def get_to_transaction(self):

        tra_seqs = []
        for doc_seq in self.seqs:
            seq = doc_seq.asdict()
            if self.num_on_seq == "base":
                dc = self.doc_dc if seq["type"] in ["base","add"] else not self.doc_dc
            else:
                dc = self.doc_dc if seq["type"] in ["sub","tot"] else not self.doc_dc

            tra_seqs.append({
                "account": seq["acc"],
                "val": seq["val"],
                "dc": dc,
                "doc": {
                    "type": self.doc_type if seq["type"] == self.num_on_seq else "",
                    "num": self.doc_num if seq["type"] == self.num_on_seq else "",
                }
            })

        tra: dict = {
            "num": self.tra_num,
            "date": self.dt,
            "descr": self.descr,
            "seqs": tra_seqs[:]
        }

        return tra
