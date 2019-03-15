PRAGMA foreign_keys = 1
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
  word TEXT NOT NULL,
  sub_word TEXT
);
GO

CREATE INDEX ix_babylon_word_id ON babylon_word (id);
GO
