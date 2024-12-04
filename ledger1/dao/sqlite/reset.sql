--- reset db for ledger1

-- admin

DROP TABLE IF EXISTS setting;
CREATE TABLE IF NOT EXISTS setting (
    setting_key TEXT NOT NULL,
    setting_value TEXT NOT NULL,
    PRIMARY KEY (setting_key)
);


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


-- transaction


DROP TABLE IF EXISTS transaction1;
CREATE TABLE IF NOT EXISTS transaction1 (
    num INTEGER PRIMARY KEY,
    dt REAL,
    descr TEXT
);

DROP TABLE IF EXISTS transaction1_detail;
CREATE TABLE IF NOT EXISTS transaction1_detail (
    num INTEGER,
    seq INTEGER,
    account_num TEXT,
    val real,
    dc BOOL,
    doc_type TEXT,
    doc_num TEXT,
    PRIMARY KEY (num, seq)
);

-- document

DROP TABLE IF EXISTS document_type;
CREATE TABLE IF NOT EXISTS document_type (
    id TEXT PRIMARY KEY,
    "name" TEXT,
    traacc INTEGER,
    num_on_seq TEXT,
    dc_true_name TEXT,
    dc_false_name TEXT,
    cpart_role_d TEXT,
    cpart_role_c TEXT,
    active INTEGER
);

DROP TABLE IF EXISTS document;
CREATE TABLE IF NOT EXISTS document (
    doc_type TEXT NOT NULL,
    doc_num TEXT NOT NULL,
    acc_num TEXT,
    cpart_name TEXT,
    PRIMARY KEY (doc_type, doc_num)
);

DROP TABLE IF EXISTS document_field;
CREATE TABLE IF NOT EXISTS document_field (
    doc_type TEXT,
    doc_num TEXT,
    field_group TEXT,
    field_name TEXT,
    field_value TEXT,
    PRIMARY KEY (doc_type, doc_num, field_group, field_name),
    FOREIGN KEY (doc_type, doc_num) REFERENCES document (doc_type, doc_num) ON DELETE CASCADE
);
