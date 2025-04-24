--- reset db for ctr1

-- admin

DROP TABLE IF EXISTS user;
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    "name" TEXT,
    email TEXT,
    "password" TEXT,
    api_key TEXT,
    "role" TEXT,
    expires TEXT,
    active INT);

DROP TABLE IF EXISTS setting;
CREATE TABLE IF NOT EXISTS setting (
    setting_key TEXT NOT NULL,
    setting_value TEXT NOT NULL,
    denied TEXT DEFAULT "",
    PRIMARY KEY (setting_key));
