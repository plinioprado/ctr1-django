from ledger1.document.document_seq import DocumentSeq

class Document:

    # primary
    doc_type: str = ""
    doc_num: str = ""
    dt: str = ""
    descr: str = ""
    doc_dc: bool = True
    num_on_seq: str = "base"
    tra_num: str = "new"
    seqs: list[DocumentSeq] = [
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

    # secondary
    cpart_name: str = ""

    # tertiary
    fields = {}

    # options
    options: dict = {}


    def __init__(self, doc_dc: bool, document_type: dict):
        self.doc_type = document_type["id"]
        self.doc_dc = doc_dc
        self.num_on_seq = document_type["num_on_seq"]


    def set_from_transaction(self, tra: dict, op_seq_acc: dict):

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

        self.dt = tra["date"]
        self.descr = tra["descr"]
        self.tra_num = tra["num"]


    def set_from_request(self, data: dict, op_seq_acc: list[dict]):
        self.cpart_name = data["cpart_name"]
        self.doc_type = data["doc_type"]
        self.doc_num = data["doc_num"]
        self.doc_dc = data["doc_dc"]

        self.dt = data["dt"]
        self.descr = data["descr"]
        self.tra_num = None
        self.fields = data["fields"]

        self.seqs = []
        for op in op_seq_acc:
            doc_seq: list[dict] = [seq for seq in data["seqs"] if seq["acc"] == op["acc"]]

            if not doc_seq:
                continue

            self.seqs.append(DocumentSeq(
                type=str(op["type"]),
                text=str(op["text"]),
                acc=str(op["acc"]),
                val=float(doc_seq[0]["val"])
            ))


    def add_document_data(self, data) -> None:
        self.cpart_name = data["cpart_name"]


    def add_fields_data(self, data: dict) -> None:
        self.fields = data


    def get_new(self):
        return {
            "doc_type": self.doc_type,
            "doc_num": "",
            "doc_dc": self.doc_dc,
            "dt": "",
            "cpart_name": "",
            "descr": "",
            "seqs": [
                {
                    "type": "base",
                    "text": "",
                    "acc": "",
                    "val": 0.0
                },
                {
                    "type": "tot",
                    "text": "",
                    "acc": "",
                    "val": 0.0
                }
            ]
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

        return {
            "num": self.tra_num,
            "date": self.dt,
            "descr": self.descr,
            "seqs": tra_seqs
        }


    def get_to_document(self):
        return {
            "doc_type": self.doc_type,
            "doc_num": self.doc_num,
            "cpart_name": self.cpart_name,
            "fields": self.fields,
        }


    def get_to_response(self):
        return {
            "doc_type": self.doc_type,
            "doc_num": self.doc_num,
            "doc_dc": self.doc_dc,
            "dt": self.dt,
            "cpart_name": self.cpart_name,
            "descr": self.descr,
            "seqs": [seq.asdict() for seq in self.seqs],
            "fields": self.fields,
        }
