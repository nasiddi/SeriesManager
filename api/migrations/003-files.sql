-- Up
CREATE TABLE files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    uuid TEXT,
    friendly_name TEXT DEFAULT NULL,
    filename TEXT DEFAULT NULL,
    is_parsed BOOL DEFAULT 0,
    filepath_original TEXT DEFAULT NULL,
    filepath_parsed TEXT DEFAULT NULL,
    parse_config TEXT DEFAULT NULL,
    corpus_analysis_config TEXT DEFAULT NULL,
    row_count INTEGER DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (uuid)
);


-- Down
DROP TABLE files;
