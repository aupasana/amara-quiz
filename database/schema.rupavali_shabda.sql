PRAGMA foreign_keys = 1
GO

CREATE TABLE rupavali_shabda (
  id INTEGER PRIMARY KEY,
  anta TEXT,
  anta_slp1 TEXT,
  anta_last TEXT,
  anta_last_slp1 TEXT,
  linga TEXT,
  pratipadika TEXT,
  category TEXT,
  rupavali TEXT
);
GO

CREATE INDEX ix_line_id ON rupavali_shabda (anta_last);
GO
