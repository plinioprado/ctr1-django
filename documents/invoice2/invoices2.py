from documents.invoice2.invoice2 import Invoice2

def get(num: str = None) -> dict:

    if num is None:
        # for now without  filters
        invoices: list[Invoice2] = get_many()
        data = [invoice.asdict() for invoice in invoices ]

    else:
        invoice: Invoice2 = get_one(num)
        data = invoice.asdict()

    return {
        "code": 200,
        "data": data,
        "message": "ok"
    }


def get_many() -> list[Invoice2]:
    invoices = [Invoice2()]
    return invoices


def get_one(num) -> Invoice2:
    invoice: Invoice2 = Invoice2(num=num)
    return invoice


def post(data) -> dict:
    invoice = Invoice2(data)

    return {
        "code": 200,
        "message": f"invoice {invoice.num} created"
    }


def put(data) -> dict:

    invoice = Invoice2(data)

    return {
        "code": 200,
        "message": f"invoice {invoice.num} updated"
    }


def delete(num) -> dict:

    return {
        "code": 200,
        "message": f"invoice {num} deleted"
    }
