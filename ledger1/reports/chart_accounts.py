""" Finance reports - Chart of accounts """

from ledger1.dao.sqlite.report_dao import get as get_accounts
from ledger1.account.account1 import Account1


def get(
        entity_name: str,
        acc_from: str,
        acc_to: str
    ):
    """
    Creates the report from the data from a DAO query

    Returns:
        Report dict with:
            header:
                entity_name: Name of the entity
                report_title: "chart of accounts"
                date_from: Initial data as tring yyyy-mm-dd,
                date_to: Final data as tring yyyy-mm-dd,
            table: 2d list with the report content
    """

    rows: list[list] = []
    accounts: list[Account1] = get_accounts(acc_from, acc_to)
    rows.append(["num", "name", "Dc"])
    for account in accounts:
        rows.append([
            account.num,
            account.name,
            "D" if account.dc else "C"
            ])

    report = {
        "header": {
            "entity_name": entity_name,
            "title": "chart of accounts"
        },
        "table": rows,
    }

    return report
