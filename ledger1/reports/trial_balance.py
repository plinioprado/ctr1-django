""" Finance reports - Trial Balance """

from ledger1.dao.sqlite import dao_report

def get(
        db_id: str,
        entity_name,
        date_from,
        date_to,
        acc_from: str,
        acc_to: str
    ):
    """
    Creates the report from the data from a DAO query

    Returns:
        Report dict with:
            header:
                entity_name: Name of the entity
                report_title: "ledger"
                date_from: Initial data as tring yyyy-mm-dd,
                date_to: Final data as tring yyyy-mm-dd,
            table: 2d list with the report content
    """

    dao_rows = dao_report.get_trial_balance(db_id, date_from, date_to, acc_from, acc_to)

    rows =[["acc_num", "acc_name", "val_open", "val_db", "val_cr", "val_bal"]]
    for dao_row in dao_rows:
        rows.append([
            dao_row["acc_num"],
            dao_row["acc_name"],
            dao_row["val_open"],
            dao_row["val_db"],
            dao_row["val_cr"],
            dao_row["val_bal"],
        ])

    return {
        "header": {
            "entity_name": entity_name,
            "title": "trial balance",
        },
        "filters": {
            "date": date_from,
            "date_to": date_to,
            "acc": acc_from,
            "acc_to": acc_to,
        },
        "table": rows,
    }
