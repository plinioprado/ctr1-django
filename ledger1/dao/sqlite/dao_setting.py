import sqlite3
import csv
from ledger1.utils import dbutil

def restore(file_name) -> None:
    """ Restore from CSV """

    con, cur = dbutil.get_connection()

    try:
        with open(file_name, "r", encoding="UTF-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cur.execute(
                    """
                    INSERT INTO setting (
                        setting_key,
                        setting_value,
                        denied
                    ) VALUES (?, ?, ?);
                    """,
                    (
                        str(row["setting_key"]),
                        str(row["setting_value"]),
                        str(row["denied"])
                    )
                )
                con.commit()

    except sqlite3.DatabaseError as err:
        raise ValueError(f"restoring setting {str(err)}") from err
    finally:
        con.close()
