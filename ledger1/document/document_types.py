from ledger1.document.document_type import DocumentType

class DocumentTypes:
    types: list

    def __init__(self):
        self.types = [
            DocumentType(id="bstat1", name="bank statement"),
            DocumentType(id="inv1", name="invoice"),
            DocumentType(id="etf1", name="etf"),
        ]


    def asdict(self):
        return [type.asdict() for type in self.types]


    def as_dict_options(self):
        return [{ "value": type.id, "text": type.name} for type in self.types]
