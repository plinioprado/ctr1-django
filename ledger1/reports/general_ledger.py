""" Finance reports - General ledger """

from ledger1.dao.sqlite import dao_report

def get(
    db_id: str,
    entity_name: str,
    date_from: str,
    date_to: str,
    acc_from: str,
    acc_to: str) -> dict:
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

    dao_rows = dao_report.get_general_ledger(db_id, date_from, date_to, acc_from, acc_to)

    rows: list[list] =[
            ["dt", "num", "descr", "seq", "doc_type", "doc_num", "val_db",
            "val_cr", "val_bal"]
        ]

    last_account_num = ""
    val_bal = 0
    tot_db = 0
    tot_cr = 0

    for count, dao_row in enumerate(dao_rows):

        if dao_row["account_num"] != last_account_num:

            if count > 0:
                # total
                rows.append([
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    tot_db,
                    tot_cr,
                    val_bal
                    ])
                rows.append([])

            tot_db = 0
            tot_cr = 0
            val_bal = 0

            rows.append([
                f"{dao_row["account_num"]} - {dao_row["account_name"]}"
                ])

        if dao_row["dc"]:
            val_db = dao_row["val"]
            val_bal += val_db
            tot_db += dao_row["val"]
            val_cr = 0
        else:
            val_cr = dao_row["val"]
            val_bal -= val_cr
            tot_cr += dao_row["val"]
            val_db = 0

        rows.append([
            dao_row["dt"],
            dao_row["num"] if dao_row["num"] > 0 else "",
            dao_row["descr"],
            dao_row["seq"] if dao_row["num"] > 0 else "",
            dao_row["doc_type"],
            dao_row["doc_num"],
            val_db if dao_row["num"] > 0 else "",
            val_cr if dao_row["num"] > 0 else "",
            val_bal
            ])

        last_account_num = dao_row["account_num"]

    # final total
    rows.append([
        "",
        "",
        "",
        "",
        "",
        "",
        tot_db,
        tot_cr,
        val_bal
        ])

    return {
        "header": {
            "entity_name": entity_name,
            "title": "general ledger",
        },
        "filters": {
            "date": date_from,
            "date_to": date_to,
            "acc": acc_from,
            "acc_to": acc_to,
        },
        "table": rows,
    }
