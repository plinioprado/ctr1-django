from ledger1.document.document_seq import DocumentSeq

class Document:

    # primary
    doc_type: str = ""
    doc_num: str = ""
    tra_num: int = "new"
    dt: str = ""
    descr: str = ""
    doc_dc: bool = None
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
