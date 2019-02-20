PRAGMA foreign_keys = 1
GO

DROP TABLE IF EXISTS sloka;
DROP TABLE IF EXISTS pada;
GO

CREATE TABLE slokas (
  sloka_number TEXT UNIQUE PRIMARY KEY NOT NULL,
  sloka_text TEXT NOT NULL
);
GO

CREATE TABLE pada (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pada TEXT NOT NULL,
  sloka_number TEXT NOT NULL,
  sloka_reference TEXT NOT NULL,
  linga TEXT NOT NULL,
  varga TEXT NOT NULL,
  artha TEXT NOT NULL,
  FOREIGN KEY (sloka_number) REFERENCES slokas(sloka_number)
);
GO

CREATE INDEX ix_pada_varga ON pada (varga);
GO
