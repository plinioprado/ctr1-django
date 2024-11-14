from ledger1.document.document_seq import DocumentSeq

class Payment:
    doc_type: str = ""
    doc_num: str = ""
    doc_dc: bool = True
    dt: str = ""
    cpart_name: str = ""
    descr: str = ""
    tra_num: int = None
    seqs: list[DocumentSeq] = [] # for now only 1 seqs (base and tot)

    def set_from_transaction(self, tra):
        self.doc_type = tra["seqs"][0]["doc"]["type"]
        self.doc_num = tra["seqs"][0]["doc"]["num"]
        self.doc_dc = tra["seqs"][0]["dc"]
        self.dt = tra["date"]
        self.descr = tra["descr"]
        self.tra_num = tra["num"]
        self.seqs = [DocumentSeq(
            type="base",
            text="from acc 003.55555.7777777",
            acc=tra["seqs"][0]["account"],
            val=tra["seqs"][0]["val"]
        )]
        self.seqs.append(DocumentSeq(
            type="tot",
            text="to desp.adm",
            acc=tra["seqs"][1]["account"],
            val=tra["seqs"][1]["val"]
        ))

    def add_document_data(self, data):
        self.cpart_name = data["cpart_name"]


    def get_to_response(self):
        return {
            "doc_type": self.doc_type,
            "doc_num": self.doc_num,
            "doc_dc": self.doc_dc,
            "dt": self.dt,
            "cpart_name": self.cpart_name,
            "descr": self.descr,
            "tra_num": self.tra_num,
            "seqs": [seq.asdict() for seq in self.seqs]
        }
