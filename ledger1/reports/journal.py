""" Finance reports - Journal """

import ledger1.dao.sqlite.dao_report as dao

def get(
        db_id: str,
        entity_name: str,
        date_from: str,
        date_to: str
    ):
    """
    Creates the report from the data from a DAO query

    Returns:
        Report dict with:
            header:
                entity_name: Name of the entity
                report_title: "journal"
                date_from: Initial data as tring yyyy-mm-dd,
                date_to: Final data as tring yyyy-mm-dd,
            table: 2d list with the report content
    """

    dao_rows = dao.get_journal(db_id, date_from, date_to)

    rows = [["dt", "num", "descr", "seq",
        "acc_num", "acc_name", "doc_type", "doc_num", "val", "dc"]
    ]
    for dao_row in dao_rows:

        seq = dao_row["seq"]
        rows.append([
            dao_row["dt"] if seq == 1 else "",
            dao_row["num"] if seq == 1 else "",
            dao_row["descr"] if seq == 1 else "",
            seq,
            dao_row["acc_num"],
            dao_row["acc_name"],
            dao_row["doc_type"],
            dao_row["doc_num"],
            dao_row["val"],
            dao_row["dc"]
        ])

    return {
        "header": {
            "entity_name": entity_name,
            "title": "journal",
        },
        "filters": {
            "date": date_from,
            "date_to": date_to,
        },
        "table": rows,
    }
