PRAGMA foreign_keys = 1
GO

DROP TABLE IF EXISTS mulam;
DROP TABLE IF EXISTS pada;
GO

CREATE TABLE mula (
  id INTEGER UNIQUE,
  varga_number TEXT NOT NULL,
  sloka_number TEXT NOT NULL,
  sloka_line TEXT UNIQUE PRIMARY KEY NOT NULL,
  varga TEXT,
  sloka_text TEXT NOT NULL
);
GO

CREATE TABLE pada (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pada_uid INTEGER NOT NULL,
  varga_number TEXT NOT NULL,
  sloka_number TEXT NOT NULL,
  sloka_line TEXT NOT NULL,
  sloka_word TEXT NOT NULL,
  pada TEXT NOT NULL,
  linga TEXT NOT NULL,
  varga TEXT NOT NULL,
  artha_english TEXT,
  artha TEXT NOT NULL,
  FOREIGN KEY (sloka_number) REFERENCES mulam(sloka_number),
  FOREIGN KEY (sloka_line) REFERENCES mulam(sloka_line)
);
GO

-- CREATE TABLE jnu (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   sloka_number TEXT NOT NULL,
--   pada TEXT NOT NULL,
--   artha_english TEXT NOT NULL,
--   artha_hindi TEXT NOT NULL,
--   artha_kannada TEXT NOT NULL,
--   artha_bangla TEXT NOT NULL,
--   artha_oriya TEXT NOT NULL,
--   artha_punjabi TEXT NOT NULL,
--   artha_assamese TEXT NOT NULL,
--   artha_maithili TEXT NOT NULL
-- );
-- GO

CREATE TABLE staging_translation (
  pada_uid INTEGER PRIMARY KEY,
  translation TEXT
);
GO

CREATE INDEX ix_mulam_number ON mula(sloka_number)
GO

CREATE INDEX ix_pada_varga ON pada (varga);
GO

CREATE TABLE babylon (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  head TEXT NOT NULL,
  body TEXT NOT NULL
);
GO

CREATE TABLE babylon_word (
  id INTEGER,
  name TEXT NOT NULL,
  word TEXT NOT NULL
);
GO
