from documents.util import fileutil
from documents.util import dbutil

def resetdb(settings) -> None:
    query_text: str = fileutil.read_text(settings["sqlite3"]["file_script_reset"])

    dbutil.executescript(query_text)
