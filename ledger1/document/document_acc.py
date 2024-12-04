"""
Hold the options per document tyoe and dc that can be held in doc.seqs[n].acc
"""
from dataclasses import dataclass

@dataclass
class DocumentAcc:
    doc_type: str
    doc_dc: bool
    type: str
    acc: str
    text: str


