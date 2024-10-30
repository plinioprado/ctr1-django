--- reset db for ledger1

-- account

DROP TABLE IF EXISTS account1;
CREATE TABLE account1 (
    num TEXT PRIMARY KEY,
    name TEXT,
    dc INTEGER,
    active INTEGER,
    doc_type TEXT,
    doc_num TEXT
);

DROP TABLE IF EXISTS transaction1;
CREATE TABLE IF NOT EXISTS transaction1 (
    num INTEGER PRIMARY KEY,
    dt REAL,
    descr TEXT
);

-- document

DROP TABLE IF EXISTS document_type;
CREATE TABLE document_type (
    id TEXT PRIMARY KEY,
    name TEXT,
    active INTEGER
);

DROP TABLE IF EXISTS document;
CREATE TABLE document (
    type_id TEXT,
    num TEXT,
    cpart_name TEXT,
    PRIMARY KEY (type_id, num)
    FOREIGN KEY (type_id) REFERENCES document_type(id)
);

-- transaction

DROP TABLE IF EXISTS transaction1_detail;
CREATE TABLE IF NOT EXISTS transaction1_detail (
    num INTEGER,
    seq INTEGER,
    account_num TEXT,
    val real,
    dc BOOL,
    doc_type TEXT,
    doc_num TEXT
);
