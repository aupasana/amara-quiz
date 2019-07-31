PRAGMA foreign_keys = 1
GO

CREATE TABLE koshas_mulam (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);
GO

CREATE TABLE koshas_mulam_line (
  kosha_name TEXT,
  line_id INTEGER,
  text_slp1 TEXT,
  text_line TEXT
  -- FOREIGN KEY (kosha_id) REFERENCES koshas_mulam(id)
);
GO

CREATE INDEX ix_line_id ON koshas_mulam_line (line_id);
GO

