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
  word_slp1 TEXT NOT NULL,
  sub_word TEXT,
  sub_word_slp1 TEXT,
  FOREIGN KEY (id) REFERENCES babylon(id),
  FOREIGN KEY (name) REFERENCES babylon(name)
);
GO

-- CREATE INDEX ix_babylon_word_id ON babylon_word (id);
-- GO

CREATE INDEX ix_babylon_word_slp1 ON babylon_word (word_slp1);
GO

CREATE INDEX ix_babylon_sub_word_slp1 ON babylon_word (sub_word_slp1);
GO

