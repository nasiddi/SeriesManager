-- Up
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    uuid TEXT,
    friendly_name TEXT,
    file_id INTEGER REFERENCES files(id) ON DELETE CASCADE ON UPDATE CASCADE,
    is_corpus_analyzed BOOL DEFAULT 0,
    corpus_analysis_config TEXT,
    filepath_corpus_analysis TEXT DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (uuid)
);

-- Down
DROP TABLE projects;
