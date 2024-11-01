""" responses for calls to /documents/admin"""

def service(op: str) -> dict:
    if op == "reset":
        response: dict = resetdb()
    else:
        raise ValueError("invalid document admin option")

    return response


def resetdb() -> dict:
    # will call dao
    return {
        "code": 200,
        "message": "reset ok"
    }
