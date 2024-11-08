
-- invoice

DROP TABLE IF EXISTS invoice2;
CREATE TABLE IF NOT EXISTS invoice2 (
    num TEXT PRIMARY KEY,
    dt INT,
    "type" TEXT,
    cpart_name TEXT,
    descr TEXT
);
