-- Up

CREATE TABLE IF NOT EXISTS process_statuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    type TEXT,
    bs_variant TEXT
);

CREATE TABLE IF NOT EXISTS processes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE ON UPDATE CASCADE,
    process_status_id INTEGER REFERENCES process_statuses(id) ON DELETE CASCADE ON UPDATE CASCADE,
    algorithm_config_id INTEGER REFERENCES algorithm_configs(id) ON DELETE CASCADE ON UPDATE CASCADE,
    progress INTEGER DEFAULT 0,
    pid INTEGER,
    hostname TEXT,
    execution_time REAL,
    exit_code INTEGER,
    f1_score_current REAL,
    f1_score_max REAL,
    f1_score_final REAL,
    confusion_matrix TEXT,
    classification_report TEXT,
    details_json TEXT,
    output_text TEXT,
    started_at DATE,
    ended_at DATE
);

INSERT INTO `process_statuses`
    (`name`, `type`, `bs_variant`)
    VALUES
    ('created', 'alive', 'secondary'),
    ('running', 'alive', 'primary'),
    ('killed', 'dead', 'info'),
    ('errored', 'dead', 'danger'),
    ('completed', 'dead', 'success')
;

-- Down

DROP TABLE processes;

DROP TABLE process_statuses;
