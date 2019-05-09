DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS quotes;


CREATE TABLE companies (
    ticker VARCHAR(5) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    industry VARCHAR(50) NOT NULL
);


CREATE TABLE quotes (
    quotes_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    ticker VARCHAR(5) NOT NULL,
    date_time TEXT NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL, 
    close REAL NOT NULL,
    volume BIGINT NOT NULL,
    FOREIGN KEY (ticker)
    REFERENCES companies (ticker)
    ON UPDATE CASCADE ON DELETE CASCADE
);
