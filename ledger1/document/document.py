
class Document:

    # primary
    doc_type: str = ""
    doc_num: str = ""
    tra_seq: int = "new"

    # options
    doc_types: list[dict] = []

    def __init__(self, data):
        print(data)
