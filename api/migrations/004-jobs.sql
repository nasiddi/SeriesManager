-- Up

CREATE TABLE IF NOT EXISTS job_statuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    type TEXT,
    bs_variant TEXT
);


CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    uuid TEXT,
    friendly_name TEXT,
    job_status_id INTEGER REFERENCES job_statuses(id) ON DELETE CASCADE ON UPDATE CASCADE,
    best_process INTEGER,
    f1_score_baseline REAL,
    file_id_data INTEGER  REFERENCES files(id) ON DELETE CASCADE ON UPDATE CASCADE,
    file_id_train INTEGER  REFERENCES files(id) ON DELETE CASCADE ON UPDATE CASCADE,
    file_id_test INTEGER  REFERENCES files(id) ON DELETE CASCADE ON UPDATE CASCADE,
    filepath_preprocessed TEXT,
    start_config TEXT DEFAULT NULL,
    classifier_comparison TEXT DEFAULT NULL,
    started_at DATE,
    ended_at DATE
);
INSERT INTO `job_statuses`
    (`name`, `type`, `bs_variant`)
    VALUES
    ('running', 'alive', 'primary'),
    ('completed', 'dead', 'success'),
    ('errored', 'dead', 'danger')
;

-- Down

DROP TABLE jobs;

DROP TABLE job_statuses;
