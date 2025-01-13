from ledger1.dao.sqlite import dao_document
from ledger1.dao.sqlite import dao_document_field
from ledger1.document.document import Document
from ledger1.document import document_options
from ledger1.transaction import transaction_service as transactions
from ledger1.document.document_types import DocumentTypes
from ledger1.utils import fileio
from ledger1.admin import entities

# get

def get(
        api_key: str,
        doc_dc: bool,
        doc_type: str = None,
        doc_num: str = None
    ) -> dict:

    db_id: str = entities.get_db_id_by_api_key(api_key)

    doc_types: list[dict] = DocumentTypes(db_id).asdict()
    doc_type_dict = [tp for tp in doc_types if tp["id"] == doc_type][0]
    doc_type_is_tra = doc_type_dict["traacc"]

    if doc_num is None:

        if doc_type_is_tra is False and doc_type != "bstat2":
            data: list[dict] = dao_document.get_many_accs(db_id, doc_type)
            data_options = {}

        else:
            data = dao_document.get_many_tra(db_id, doc_dc=doc_dc, doc_type=doc_type)
            data_options = document_options.get_op_doc_dc(db_id, doc_type),

        data_format: dict = get_format(doc_type)

        response = {
            "data": data,
            "format": data_format,
            "message": "wip",
            "status": 200,
            "options": {
                "doc_dc": data_options,
            },
            "filters": {
                "doc_dc": doc_dc
            }
        }

    elif doc_num == "new":

        # set primary attributes
        doc: Document = get_document_obj(db_id, doc_dc=doc_dc, doc_type=doc_type)
        #data = doc.get_new()
        op_seq_acc = document_options.get_op_seq_acc(doc_type=doc_type, doc_dc=doc_dc)

        # set terciary attributes
        fields: dict = dao_document_field.get_one(db_id, doc_type, doc_num)
        doc.add_fields_data(fields)

        data = doc.get_to_response()

        response = {
            "data": data,
            "message": "wip",
            "options": {
                "op_seq_acc": op_seq_acc,
                "doc_dc": document_options.get_op_doc_dc(db_id, doc_type),
            },
            "status": 200,
        }

    else:

        if doc_type_is_tra is False and doc_type != "bstat2":
            data: list[dict] = {}

            response = {
                "data": data,
                "message": "ok",
                "status": 200,
            }

        else:

            tra: dict = transactions.get_by_doc(db_id, doc_type, doc_num)
            tra_doc_dc = [seq for seq in tra["seqs"] if seq["doc"]["type"] == doc_type][0]["dc"]
            op_seq_acc = document_options.get_op_seq_acc(doc_type=doc_type, doc_dc=tra_doc_dc)

            # set primary attributes (transaction)
            doc: Document = get_document_obj(db_id, doc_dc=tra_doc_dc, doc_type=doc_type)
            doc.set_from_transaction(tra, op_seq_acc)

            # set secondary attributes (document)
            res: dict = dao_document.get_one(db_id, doc_type, doc_num)
            doc.add_document_data(res)

            # set terciary attributes (fields)
            fields: dict = dao_document_field.get_one(db_id, doc_type, doc_num)
            doc.add_fields_data(fields)

            data = doc.get_to_response()

            response = {
                "data": data,
                "message": "wip",
                "options": {
                    "op_seq_acc": op_seq_acc,
                    "doc_dc": document_options.get_op_doc_dc(db_id, doc_type),
                },
                "status": 200,
            }

    return response


def get_one(
        db_id: str,
        doc_type: str,
        doc_num: str,
        op_seq_acc: list[dict]
    ) -> dict:

    tra: dict = transactions.get_by_doc(db_id, doc_type, doc_num)
    doc_dc = [seq for seq in tra["seqs"] if seq["doc"]["type"] == doc_type][0]["dc"]

    doc: Document = get_document_obj(db_id, doc_dc=doc_dc, doc_type=doc_type)
    doc.set_from_transaction(tra, op_seq_acc)

    res: dict = dao_document.get_one(db_id, doc_type, doc_num)
    doc.add_document_data(res)
    data = doc.get_to_response()

    return data

# post

def post(api_key: str, data) -> dict:

    db_id: str = entities.get_db_id_by_api_key(api_key)

    # no db_id because is in a csv file
    op_seq_acc = document_options.get_op_seq_acc(doc_dc=data["doc_dc"], doc_type=data["doc_type"])

    doc: Document = get_document_obj(db_id, doc_dc=data["doc_dc"], doc_type=data["doc_type"])
    doc.set_from_request(data, op_seq_acc)
    transactions.post(api_key, doc.get_to_transaction())
    dao_document.post(db_id, doc.get_to_document())
    return {
        "status": 200,
        "message": f"document {data["doc_type"]} {data["doc_num"]} created"
    }


# put


def put(api_key: str, data: dict) -> dict:

    db_id: str = entities.get_db_id_by_api_key(api_key)

    op_seq_acc = document_options.get_op_seq_acc(doc_dc=data["doc_dc"], doc_type=data["doc_type"])
    doc = get_document_obj(db_id, doc_dc=data["doc_dc"], doc_type=data["doc_type"])
    doc.set_from_request(data, op_seq_acc)
    tra = transactions.get_by_doc(db_id, data["doc_type"], data["doc_num"])
    doc.tra_num = tra["num"]
    transactions.put(api_key, doc.get_to_transaction())
    dao_document.put(db_id, doc.get_to_document())

    return {
        "status": 200,
        "message": f"document {data["doc_type"]} {data["doc_num"]} updated"
    }


# delete


def delete(api_key: str, doc_type: str, doc_num: str) -> dict:

    db_id: str = entities.get_db_id_by_api_key(api_key)

    tra: dict = transactions.get_by_doc(db_id, doc_type, doc_num)

    transactions.delete(api_key, tra["num"])
    deleted_type, deleted_num = dao_document.delete(db_id, doc_type, doc_num)

    return {
        "status": 200,
        "message": f"document {deleted_type} {deleted_num} deleted"
    }


## helpers


def get_document_obj(db_id: str, doc_dc: bool, doc_type: str) -> Document:

    document_types: DocumentTypes = DocumentTypes(db_id)
    document_type: dict = document_types.get(doc_type)

    return Document(
        doc_dc=doc_dc,
        document_type=document_type)


def get_format(doc_type:str) -> dict:
    settings_data = fileio.get_file_settings()
    file_format_path = settings_data["file"]["format"]

    if doc_type in ["eft","inv2","chequing","gic"]:
        data_format: dict = fileio.read_json(f"{file_format_path}/doc_{doc_type}s_format.json")
    else:
        raise ValueError(f"invalid document type {doc_type}")

    return data_format
