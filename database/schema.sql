PRAGMA foreign_keys = 1
GO

DROP TABLE IF EXISTS mulam;
DROP TABLE IF EXISTS pada;
GO

CREATE TABLE mula (
  sloka_number TEXT NOT NULL,
  sloka_line TEXT UNIQUE PRIMARY KEY NOT NULL,
  sloka_text TEXT NOT NULL
);
GO

CREATE TABLE pada (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sloka_number TEXT NOT NULL,
  sloka_line TEXT NOT NULL,
  sloka_word TEXT NOT NULL,
  pada TEXT NOT NULL,
  linga TEXT NOT NULL,
  varga TEXT NOT NULL,
  artha TEXT NOT NULL,
  FOREIGN KEY (sloka_number) REFERENCES mulam(sloka_number),
  FOREIGN KEY (sloka_line) REFERENCES mulam(sloka_line)
);
GO

CREATE INDEX ix_mulam_number ON mula(sloka_number)
GO

CREATE INDEX ix_pada_varga ON pada (varga);
GO
