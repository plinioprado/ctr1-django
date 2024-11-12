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

DROP TABLE IF EXISTS document_type;
CREATE TABLE IF NOT EXISTS document_type (
    id TEXT PRIMARY KEY,
    "name" TEXT,
    traacc INTEGER,
    active INTEGER
);

DROP TABLE IF EXISTS transaction1;
CREATE TABLE IF NOT EXISTS transaction1 (
    num INTEGER PRIMARY KEY,
    dt REAL,
    descr TEXT
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

-- invoice

DROP TABLE IF EXISTS document;
CREATE TABLE IF NOT EXISTS document (
    doc_type TEXT NOT NULL,
    doc_num TEXT NOT NULL,
    acc_num TEXT,
    PRIMARY KEY (doc_type, doc_num)
);

DROP TABLE IF EXISTS invoice2;
CREATE TABLE IF NOT EXISTS invoice2 (
    num TEXT PRIMARY KEY,
    dt INT,
    "type" TEXT,
    cpart_name TEXT,
    descr TEXT
);
