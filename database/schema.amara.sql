PRAGMA foreign_keys = 1
GO

DROP TABLE IF EXISTS mulam;
DROP TABLE IF EXISTS pada;
GO

CREATE TABLE varga (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  varga TEXT,
  varga_english TEXT
);
GO

CREATE TABLE mula (
  id INTEGER UNIQUE,
  varga_number TEXT NOT NULL,
  sloka_number TEXT NOT NULL,
  sloka_line TEXT UNIQUE PRIMARY KEY NOT NULL,
  varga TEXT,
  audio_filename TEXT,
  audio_seconds TEXT,
  sloka_text TEXT NOT NULL
);
GO

CREATE INDEX ix_mulam_number ON mula(sloka_number)
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
  artha_telugu TEXT,
  artha TEXT NOT NULL,
  FOREIGN KEY (sloka_number) REFERENCES mulam(sloka_number),
  FOREIGN KEY (sloka_line) REFERENCES mulam(sloka_line)
);
GO

CREATE INDEX ix_pada_varga ON pada (varga);
GO

CREATE TABLE staging_translation (
  pada_uid INTEGER PRIMARY KEY,
  translation TEXT
);
GO

CREATE TABLE audio (
  filename TEXT,
  sloka_number TEXT NOT NULL,
  sloka_line TEXT NOT NULL,
  seconds TEXT NOT NULL
);
GO

CREATE INDEX ix_audio_sloka_line ON audio(sloka_number);
GO
