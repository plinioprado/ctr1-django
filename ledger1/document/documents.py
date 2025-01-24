"""
This module handles the creation, updating, and deletion of documents.
Also provides options and formats for the front-end.

There are two types of documents with different behaviors:
 - account: Supports detailed Accounts, identified by a type and number stored
   in the Account, complemented by fields in the DocumentField table.
 - transaction: Supports Transactions, identified by a type, dc, and number
   stored in the Transaction (in one of its Seqs), complemented by fields in
   the DocumentField table.
"""

from ledger1.dao.sqlite import dao_document
from ledger1.dao.sqlite import dao_document_field
from ledger1.document.document import Document
from ledger1.document.document_acc import DocumentAccount
from ledger1.document.aux import document_options
from ledger1.document.aux.document_types import DocumentTypes

from ledger1.transaction import transaction_service as transactions
from ledger1.account import account_service as accounts
from ledger1.utils import fileio
from ledger1.admin import entities


# get

def get( # pylint: disable=too-many-locals
        api_key: str,
        doc_dc: bool,
        doc_type: str = None,
        doc_num: str = None
    ) -> dict:

    db_id: str = entities.get_db_id_by_api_key(api_key)

    doc_type_is_tra: bool = _get_doc_type_is_tra(db_id, doc_type)

    if doc_num is None:

        if not doc_type_is_tra and doc_type != "bstat2":

            data: list[dict] = _get_many_acc(
                db_id,
                doc_type=doc_type)

            data_options = {}

        else:
            data = _get_many_tra(
                db_id,
                doc_dc=doc_dc,
                doc_type=doc_type)

            data_options = document_options.get_op_doc_dc(db_id, doc_type)

        data_format: dict = get_format(doc_type, True)

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

        if doc_type_is_tra is False and doc_type != "bstat2":
            doc: Document = _get_document_tra_obj(
                db_id,
                doc_dc=doc_dc,
                doc_type=doc_type,
                doc_num="")
            fields: dict = dao_document_field.get_one(db_id, doc_type, doc_num)
            doc.add_fields_data(fields)
            data = doc.get_to_response_acc()
            data_format: dict = get_format(doc_type, False)
            data_options = []

        else:

            # set primary attributes
            doc: Document = _get_document_tra_obj(
                db_id,
                doc_dc=doc_dc,
                doc_type=doc_type,
                doc_num="")

            op_seq_acc = document_options.get_op_seq_acc(doc_type=doc_type, doc_dc=doc_dc)

            # set terciary attributes
            fields: dict = dao_document_field.get_one(db_id, doc_type, doc_num)
            doc.add_fields_data(fields)

            data = doc.get_to_response()

            data_options = {
                "op_seq_acc": op_seq_acc,
                "doc_dc": document_options.get_op_doc_dc(db_id, doc_type),
            }

        data_format: dict = get_format(doc_type, False)

        response = {
            "data": data,
            "message": "wip",
            "format": data_format,
            "options": data_options,
            "status": 200,
        }

    else:

        if doc_type_is_tra is False and doc_type != "bstat2":
            data: dict = dao_document.get_one_by_doc(db_id, doc_type, doc_num)
            data["fields"] = dao_document_field.get_one(db_id, doc_type, doc_num)
            data_format: dict = get_format(doc_type, False)
            data_options = []

            response = {
                "data": data,
                "format": data_format,
                "message": "ok",
                "options": data_options,
                "status": 200,
            }

        else:

            tra: dict = transactions.get_by_doc(db_id, doc_type, doc_num)
            tra_doc_dc = [seq for seq in tra["seqs"] if seq["doc"]["type"] == doc_type][0]["dc"]
            op_seq_acc = document_options.get_op_seq_acc(doc_type=doc_type, doc_dc=tra_doc_dc)

            # set primary attributes (transaction)
            doc: Document = _get_document_tra_obj(
                db_id,
                doc_dc=tra_doc_dc,
                doc_type=doc_type,
                doc_num=doc_num)

            doc.set_from_transaction(tra, op_seq_acc)

            # set secondary attributes (document)
            res: dict = {}
            doc.add_document_data(res)

            # set terciary attributes (fields)
            fields: dict = dao_document_field.get_one(db_id, doc_type, doc_num)
            doc.add_fields_data(fields)

            data = doc.get_to_response()
            data_format: dict = get_format(doc_type, False)

            response = {
                "data": data,
                "format": data_format,
                "message": "wip",
                "options": {
                    "op_seq_acc": op_seq_acc,
                    "doc_dc": document_options.get_op_doc_dc(db_id, doc_type),
                },
                "status": 200,
            }

    return response


def _get_many_acc(db_id: str, doc_type: str) -> list[dict]:
    accs: list[dict] = accounts.get_many_by_doc(db_id, doc_type)

    data = [{
            "doc_type": acc["doc_type"],
            "doc_num": acc["doc_num"],
            "acc_num": acc["num"],
            "acc_dc": acc["dc"],
            "descr": acc["name"]} for acc in accs]

    return data


def _get_many_tra(db_id: str, doc_dc: bool, doc_type: str) -> list[dict]:

    tras: list[dict] = transactions.get_many_by_doc(db_id, doc_type, doc_dc)

    data: list[dict] = []
    for tra in tras:
        fields: dict = dao_document.get_fields(db_id, doc_type, tra["doc_num"])
        data.append({
                "doc_type": tra["doc_type"],
                "doc_num": tra["doc_num"],
                "doc_dc": tra["doc_dc"],
                "dt": tra["dt"],
                "cpart_name": fields["person"]["name"],
                "descr": tra["descr"],
                "val": tra["val"],
            })

    return data


def get_one(
        db_id: str,
        doc_type: str,
        doc_num: str,
        op_seq_acc: list[dict]
    ) -> dict:

    tra: dict = transactions.get_by_doc(db_id, doc_type, doc_num)
    doc_dc = [seq for seq in tra["seqs"] if seq["doc"]["type"] == doc_type][0]["dc"]

    doc: Document = _get_document_tra_obj(
        db_id,
        doc_dc=doc_dc,
        doc_type=doc_type,
        doc_num=doc_num)
    doc.set_from_transaction(tra, op_seq_acc)

    res: dict = {}
    doc.add_document_data(res)
    data = doc.get_to_response()

    return data


# post

def post(api_key: str, doc_type: str, data) -> dict:

    db_id: str = entities.get_db_id_by_api_key(api_key)

    doc_type_is_tra: bool = _get_doc_type_is_tra(db_id, data["doc_type"])

    if doc_type_is_tra:
        doc_dc: bool = data["doc_dc"] if "doc_dc" in data else None
        op_seq_acc = document_options.get_op_seq_acc(
            doc_dc=doc_dc,
            doc_type=data["doc_type"])
        doc: Document = _get_document_tra_obj(
            db_id,
            doc_dc=doc_dc,
            doc_type=data["doc_type"],
            doc_num=data["doc_num"])
        doc.set_from_request(data, op_seq_acc)
        transactions.post(api_key, doc.get_to_transaction())
    else:
        doc: DocumentAccount = _get_document_acc_obj(
            db_id,
            doc_type=data["doc_type"],
            doc_num=None)
        doc.set_from_request(data)
        accounts.post_data(db_id, doc.get_to_account())

    dao_document.post(db_id, doc.get_to_document())

    return {
        "status": 200,
        "message": f"document {data["doc_type"]} {data["doc_num"]} created"
    }


# put


def put(
        api_key: str,
        doc_type: str,
        doc_num: str,
        data) -> dict:

    db_id: str = entities.get_db_id_by_api_key(api_key)

    doc_type_is_tra: bool = _get_doc_type_is_tra(db_id, doc_type)

    if doc_type_is_tra:
        doc_dc: bool = data["doc_dc"] if "doc_dc" in data else None
        op_seq_acc = document_options.get_op_seq_acc(
            doc_dc=doc_dc,
            doc_type=data["doc_type"])
        tra_num = transactions.get_by_doc(db_id, doc_type, doc_num)["num"]
        doc: Document = _get_document_tra_obj(
            db_id,
            doc_dc=doc_dc,
            doc_type=data["doc_type"],
            doc_num=doc_num,
            tra_num=tra_num)
        doc.set_from_request(data, op_seq_acc)
        transactions.put(api_key, doc.get_to_transaction())
    else:
        doc: DocumentAccount = _get_document_acc_obj(
            db_id,
            doc_type=doc_type,
            doc_num=doc_num)
        doc.set_from_request(data)
        accounts.put_data(db_id, doc.get_to_account())

    dao_document.post(db_id, doc.get_to_document())

    return {
        "status": 200,
        "message": f"document {data["doc_type"]} {data["doc_num"]} created"
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

def _get_doc_type_is_tra(db_id: str, doc_type: str) -> bool:

    doc_types: list[dict] = DocumentTypes(db_id).asdict()
    doc_type_dict: dict = [tp for tp in doc_types if tp["id"] == doc_type][0]
    doc_type_is_tra: bool = doc_type_dict["traacc"]

    return doc_type_is_tra


def _get_document_tra_obj(
        db_id: str,
        doc_dc: bool,
        doc_type: str,
        doc_num: str,
        tra_num: str = None) -> Document:
    document_types: DocumentTypes = DocumentTypes(db_id)
    document_type: dict = document_types.get(doc_type)

    return Document(
        document_type=document_type,
        doc_dc=doc_dc,
        doc_num=doc_num,
        tra_num=tra_num)


def _get_document_acc_obj(
        db_id: str,
        doc_type: str,
        doc_num: str = None) -> DocumentAccount:

    document_types: DocumentTypes = DocumentTypes(db_id)
    document_type: dict = document_types.get(doc_type)

    return DocumentAccount(document_type=document_type)


def get_format(doc_type:str, is_list: bool) -> dict:
    settings_data = fileio.get_file_settings()
    file_format_path = settings_data["file"]["format"]

    if doc_type not in ["eft","inv2","chequing","gic"]:
        raise ValueError(f"invalid document type {doc_type}")

    if is_list:
        data_format: dict = fileio.read_json(f"{file_format_path}/doc_{doc_type}s_format.json")
    else:
        data_format = fileio.read_json(f"{file_format_path}/doc_{doc_type}_format.json")

    return data_format
