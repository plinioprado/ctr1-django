from ledger1.transaction import transaction_service
from documents.invoice2.invoice2 import Invoice2
from documents.dao.sqlite import dao_invoice2
from documents.util import fileutil

def get(num: str = None) -> dict:

    if num is None:
        response: list[dict] = get_many()
    else:
        response: dict = get_one(num)

    return response


def get_many() -> list[Invoice2]:
    invoices: list[Invoice2] = dao_invoice2.get_many()
    data = [invoice.asdict() for invoice in invoices]

    return {
        "code": 200,
        "data": data,
        "message": "ok"
    }


def get_one(num: str) -> Invoice2:
    invoice: Invoice2 | None = dao_invoice2.get_one(num)
    if invoice is None:
        data = {}
    else:
        data = invoice.asdict()

    options = fileutil.read_json("./documents/dao/csv/invoice2_options.json")

    return {
        "code": 200,
        "data": data,
        "message": "ok",
        "options": options
    }


def post(data) -> dict:
    invoice: Invoice2 =  Invoice2(data)
    transaction_service.post(invoice.get_transaction_dict())
    last_num = dao_invoice2.post(invoice)

    return {
        "code": 200,
        "message": f"invoice {last_num} created"
    }


def put(data) -> dict:
    invoice: Invoice2 =  Invoice2(data)
    tra_num = dao_invoice2.get_tra_num(invoice.num)
    invoice.set_tra_num(tra_num)
    transaction_service.put(invoice.get_transaction_dict())
    num = dao_invoice2.put(invoice)

    return {
        "code": 200,
        "message": f"invoice {num} updated"
    }


def delete(num) -> dict:

    tra_num = dao_invoice2.get_tra_num(num)
    transaction_service.delete(tra_num)
    deleted_num: str = dao_invoice2.delete(num)

    return {
        "code": 200,
        "message": f"invoice {deleted_num} deleted"
    }
