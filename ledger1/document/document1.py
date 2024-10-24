from dataclasses import dataclass
from ledger1.document.document_type import DocumentType

@dataclass
class Document1:
    num: str
    type: DocumentType

