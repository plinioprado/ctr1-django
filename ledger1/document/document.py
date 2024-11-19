from ledger1.document.document_seq import DocumentSeq

class Document:

    # primary
    doc_type: str = ""
    doc_num: str = ""
    dt: str = ""
    descr: str = ""
    doc_dc: bool = None
    tra_num: int = "new"
    seqs: list[DocumentSeq] = []

    # secondary
    cpart_name: str = ""

    # options
    doc_types: list[dict] = []

    def __init__(self, doc_type: str, doc_dc: bool):
        self.doc_type = doc_type
        self.doc_dc = doc_dc

    def set_from_transaction(self, tra: dict, op_seq_acc: dict):
        self.doc_type = tra["seqs"][0]["doc"]["type"]
        self.doc_num = tra["seqs"][0]["doc"]["num"]
        self.doc_dc = tra["seqs"][0]["dc"]
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

        self.doc_type = tra["seqs"][0]["doc"]["type"]
        self.doc_num = tra["seqs"][0]["doc"]["num"]
        self.doc_dc = tra["seqs"][0]["dc"]


    def set_from_request(self, data: dict, op_seq_acc: list[dict]):
        self.cpart_name = data["cpart_name"]
        self.doc_type = data["doc_type"]
        self.doc_num = data["doc_num"]
        self.doc_dc = data["doc_dc"]

        self.dt = data["dt"]
        self.descr = data["descr"]
        self.tra_num = None
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


    def add_document_data(self, data):
        self.cpart_name = data["cpart_name"]


    def get_new(self):
        return {
            "doc_type": self.doc_type,
            "doc_num": "",
            "doc_dc": self.doc_dc,
            "dt": "",
            "cpart_name": "",
            "descr": "",
            "tra_num": "new",
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
            dc = self.doc_dc if seq["type"] in ["add","tot"] else not self.doc_dc

            tra_seqs.append({
                "account": seq["acc"],
                "val": seq["val"],
                "dc": dc,
                "doc": {
                    "type": self.doc_type if seq["type"] == "tot" else "",
                    "num": self.doc_num if seq["type"] == "tot" else "",
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
            "cpart_name": self.cpart_name
        }


    def get_to_response(self):
        return {
            "doc_type": self.doc_type,
            "doc_num": self.doc_num,
            "doc_dc": self.doc_dc,
            "dt": self.dt,
            "cpart_name": self.cpart_name,
            "descr": self.descr,
            "seqs": [seq.asdict() for seq in self.seqs]
        }
