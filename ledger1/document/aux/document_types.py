from ledger1.document.aux.document_type import DocumentType
from ledger1.dao.sqlite import dao_document_type

class DocumentTypes:
    types: list[DocumentType] = []

    # TODO: In th future, requests to dao should be in the service
    def __init__(self, db_id: str):
        self.types = dao_document_type.get(db_id)


    def asdict(self) -> list[dict]:
        return [type.asdict() for type in self.types]


    def get(self, doc_type) -> dict:
        return [tp.asdict() for tp in self.types if tp.id == doc_type][0]


    def get_dict_options(self) -> list[dict]:
        return [{ "value": type.id, "text": type.name} for type in self.types if type.active]


    @staticmethod
    def get_default_dict() -> dict:
        return DocumentType.asdefault()
