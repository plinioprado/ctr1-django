
-- invoice

DROP TABLE IF EXISTS invoice2;
CREATE TABLE IF NOT EXISTS invoice2 (
    num TEXT PRIMARY KEY,
    dt INT,
    "type" TEXT,
    cpart_name TEXT,
    descr TEXT
);

DROP TABLE IF EXISTS banstat2;
CREATE TABLE IF NOT EXISTS banstat2 (
    institution_num INT,
    institution_name TEXT,
    transit_num TEXT,
    account_num TEXT,
    acc_num TEXT,
);
