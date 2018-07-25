-- Up
CREATE TABLE settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    key TEXT,
    value TEXT,
    UNIQUE (user_id, key)
);

INSERT INTO settings
    (key, value)
    VALUES
    ('navbar.type', '"dark"'),
    ('navbar.variant', '"dark"'),
    ('parse.header', 'true'),
    ('parse.smartCsv', 'true'),
    ('parse.smartHeader', 'true'),
    ('parse.previewLines', '50')
;
-- Down
DROP TABLE settings;
