from dataclasses import dataclass

@dataclass
class DocumentType:
    id: str
    name: str

    def __post_init__(self):
        if not self.id:
            raise ValueError('missing document type id')
        if not isinstance(self.id, str) or len(self.id) > 10:
            raise ValueError('invalid document type id')
        if not self.name:
            raise ValueError('missing document type name')
        if not isinstance(self.id, str) or len(self.id) > 30:
            raise ValueError('invalid document type name')

    def asdict(self):
        return {
            "id": self.id,
            "name": self.name
        }
