from documents.invoice2.invoice2 import Invoice2
from documents.dao.sqlite import dao_invoice2

def get(num: str = None) -> dict:

    if num is None:
        data: list[dict] = get_many()
    else:
        data: dict = get_one(num)

    return {
        "code": 200,
        "data": data,
        "message": "ok"
    }


def get_many() -> list[Invoice2]:
    invoices: list[Invoice2] = dao_invoice2.get_many()
    data = [invoice.asdict() for invoice in invoices]

    return data


def get_one(num: str) -> Invoice2:
    invoice: Invoice2 | None = dao_invoice2.get_one(num)
    if invoice is None:
        data = {}
    else:
        data = invoice.asdict()

    return data


# def post(data) -> dict:
#     invoice = Invoice2(data)

#     return {
#         "code": 200,
#         "message": f"invoice {invoice.num} created"
#     }


# def put(data) -> dict:

#     invoice = Invoice2(data)

#     return {
#         "code": 200,
#         "message": f"invoice {invoice.num} updated"
#     }


# def delete(num) -> dict:

#     return {
#         "code": 200,
#         "message": f"invoice {num} deleted"
#     }
