from ledger1.transaction import transaction_service
from ledger1.utils import fileio
from ledger1.dao.sqlite import dao_invoice2
from ledger1.document.invoice2 import Invoice2


def get(num: str = None) -> dict:

    if num is None:
        response: list[dict] = get_many()
    else:
        response: dict = get_one(num)

    return response


def get_many() -> list[dict]:
    """ get a list of dicts representing documents """

    data: list[dict] = dao_invoice2.get_many()

    return {
        "code": 200,
        "data": data,
        "message": "ok"
    }


def get_one(num: str) -> dict:
    """
    Args:
        num: valid invoice num or 'new' to get just the defaults for a new one

    Returns:
        dict with data for the REST response
    """

    if num is not None and num != "new":
        invoice: Invoice2 | None = dao_invoice2.get_one(num)
    else:
        invoice = None

    if invoice is None:
        data = {}
    else:
        data = invoice.asdict()

    seq_types = fileio.read_csv("./ledger1/dao/csv/document_seq_type.csv")

    return {
        "code": 200,
        "data": data,
        "message": "ok",
        "options": {
            "seq_types": seq_types
        }
    }


def post(data) -> dict:
    """ create new invoice """

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
