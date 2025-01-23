""" DocumentType

DocumentType is the attribute of a Document that defines its remaining attributes and beavior

Attributes:
    id: str - identifying code
    name: str - user friendly name for selection and display
    at: str - can be "a" if the document is linked to an account or "t" if linked to a transaction
    active: can be attributed to documents being created or updated (default true)

"""
from dataclasses import dataclass

@dataclass
class DocumentType:
    id: str
    name: str
    traacc: bool
    num_on_seq: str
    dc_true_name: str
    dc_false_name: str
    cpart_role_d: str
    cpart_role_c: str
    active: bool

    def __post_init__(self):
        if not self.id:
            raise ValueError('missing document type id')
        if not isinstance(self.id, str) or len(self.id) > 15:
            raise ValueError('invalid document type id')
        if not self.name:
            raise ValueError('missing document type name')
        if not isinstance(self.id, str) or len(self.id) > 30:
            raise ValueError('invalid document type name')
        if self.traacc not in [True, False]:
            raise ValueError('invalid document type traacc')
        if self.num_on_seq not in ["base","tot"]:
            raise ValueError('invalid document type num_on_seq')
        if self.active not in [True, False]:
            self.active = True


    def asdict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "traacc": self.traacc,
            "num_on_seq": self.num_on_seq,
            "dc_true_name": self.dc_true_name,
            "dc_false_name": self.dc_false_name,
            "cpart_role_d": self.cpart_role_d,
            "cpart_role_c": self.cpart_role_c,
            "active": self.active
        }

    @staticmethod
    def asdefault() -> dict:
        return {
            "id": "",
            "name": "",
            "active": True
        }
