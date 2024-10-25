DROP TABLE IF EXISTS document_type;

CREATE TABLE document_type (
    id TEXT PRIMARY KEY,
    name TEXT,
    at INTEGER,
    active INTEGER
);
