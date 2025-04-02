""" Finance reports - Chart of accounts """

from ledger1.dao.sqlite.dao_report import get as get_accounts
from ledger1.account.account import Account


def get(
        api_key: str,
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
    accounts: list[Account] = get_accounts(api_key, acc_from, acc_to)
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
        "filters": {
            "acc": acc_from,
            "acc_to": acc_to,
        },
        "table": rows,
    }

    return report
