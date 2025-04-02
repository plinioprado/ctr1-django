from ledger1.document.document_tra_seq import DocumentSeq

class Document:

    doc_type: str = ""
    doc_num: str = ""
    fields: list[dict] = []

    def get_to_document(self):
        return {
            "doc_type": self.doc_type,
            "doc_num": self.doc_num,
            "fields": self.fields,
        }
