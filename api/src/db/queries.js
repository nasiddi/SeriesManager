const db = require('sqlite');
const os = require('os');
const moment = require('moment');
const _ = require('async-lodash');
const Promise = require('bluebird');

async function getProcessStatusId(name) {
  const row = await db.get('SELECT * FROM process_statuses WHERE `name` = ?', name);
  return row.id;
}

function now() { return (new Date()).toISOString(); }

async function newJob(params) {
  const out = await db.run(`
    INSERT INTO jobs
    (uuid, user_id, friendly_name, started_at, start_config, job_status_id, file_id_data, file_id_train, file_id_test)
    VALUES
    ($uuid, $user_id, $friendly_name, $started_at, $start_config, (SELECT id FROM job_statuses WHERE name = 'running'), (SELECT id FROM files WHERE uuid = $file_uuid_data LIMIT 1), (SELECT id FROM files WHERE uuid = $file_uuid_train LIMIT 1), (SELECT id FROM files WHERE uuid = $file_uuid_test LIMIT 1))
        `, {
    $uuid: params.uuid,
    $user_id: params.user_id,
    $friendly_name: params.friendly_name,
    $start_config: params.start_config,
    $file_uuid_data: params.file_uuid_data,
    $file_uuid_train: params.file_uuid_train,
    $file_uuid_test: params.file_uuid_test,
    $started_at: now(),
  });

  return out.stmt.lastID;
}

async function newProcess(params) {
  const out = await db.run(`
            INSERT INTO processes
            (algorithm_config_id, hostname, started_at, job_id, process_status_id)
            VALUES
            (?, ?, ?, ?, (SELECT id FROM process_statuses WHERE name = 'created'))
        `, params.algorithm_config_id, os.hostname(), now(), params.job_id);
  return out.stmt.lastID;
}

function updateProcessField(processId, col, val) {
  db.run(`UPDATE processes SET ${col} = ? WHERE id = ?`, val, processId);
}

async function updateProcessStatus(processId, status) {
  updateProcessField(processId, 'process_status_id', await getProcessStatusId(status));
}

async function updateProcessF1ScoreMax(processId) {
  db.run('UPDATE processes SET f1_score_max = (SELECT MAX(COALESCE(f1_score_current, 0), COALESCE(f1_score_max, 0), COALESCE(f1_score_final, 0))  FROM processes WHERE id = ?) WHERE id = ?', { 1: processId, 2: processId });
}

async function calculateProcessDuration(processId) {
  const out = await db.get('SELECT started_at, ended_at FROM processes WHERE id = ?', { 1: processId });
  const diffMs = moment(out.ended_at).diff(out.started_at);
  updateProcessField(processId, 'execution_time', diffMs);
}

async function getAlgorithms() {
  return db.all('SELECT * FROM algorithms');
}

async function getAlgorithm(id) {
  return db.get('SELECT * FROM algorithms WHERE id = ?', { 1: id });
}

async function getAlgorithmConfigs() {
  return db.all('SELECT * FROM algorithm_configs');
}

async function getAlgorithmConfig(id) {
  return db.get('SELECT * FROM algorithm_configs WHERE id = ?', { 1: id });
}

async function getJob(uuid) {
  const out = await db.get('SELECT * FROM jobs WHERE uuid = ?', { 1: uuid });
  out.job_status = await db.get('SELECT * FROM job_statuses WHERE id = ?', { 1: out.job_status_id });

  out.classifier_comparison = JSON.parse(out.classifier_comparison);
  out.start_config = JSON.parse(out.start_config);

  if (out.file_id_data) {
    out.file_data = await db.get('SELECT * FROM files WHERE id = $id', { $id: out.file_id_data });
  }

  if (out.file_id_train) {
    out.file_train = await db.get('SELECT * FROM files WHERE id = $id', { $id: out.file_id_train });
  }

  if (out.file_id_test) {
    out.file_test = await db.get('SELECT * FROM files WHERE id = $id', { $id: out.file_id_test });
  }

  return out;
}

async function getProcess(pid) {
  const out = await db.get('SELECT * FROM processes WHERE id = ?', { 1: pid });

  out.details_json = JSON.parse(out.details_json);
  out.confusion_matrix = JSON.parse(out.confusion_matrix);
  out.classification_report = JSON.parse(out.classification_report);

  out.execution_time_human = moment.duration(out.execution_time).humanize();

  out.process_status = await db.get('SELECT * FROM process_statuses WHERE id = ?', { 1: out.process_status_id });
  out.algorithm_config = await db.get('SELECT * FROM algorithm_configs WHERE id = ?', { 1: out.algorithm_config_id });
  out.algorithm = await db.get('SELECT * FROM algorithms WHERE id = ?', { 1: out.algorithm_config.algorithm_id });
  out.job_uuid = (await db.get('SELECT uuid FROM jobs WHERE id = ?', { 1: out.job_id })).uuid;
  out.job_proc = `${out.job_uuid}-${out.id}`;
  out.friendly_name = `${out.algorithm.name}: ${out.algorithm_config.name}`;

  return out;
}

async function getProcesses(uuid) {
  const ids = await db.all('SELECT id FROM processes WHERE job_id = (SELECT id FROM jobs WHERE uuid = ?)', { 1: uuid });
  const out = _.map(ids, async (el) => {
    const proc = await getProcess(el.id);
    return proc;
  });
  return Promise.all(out);
}

async function jobStatusUpdateCheck(uuid) {
  const procs = await getProcesses(uuid);

  const out1 = await db.get('SELECT COUNT(id) AS count FROM processes WHERE job_id = (SELECT id FROM jobs WHERE uuid = ?) AND process_status_id NOT IN (SELECT id FROM process_statuses WHERE type = "dead")', { 1: uuid });
  const out2 = await db.get('SELECT ended_at FROM jobs WHERE uuid = ?', { 1: uuid });

  db.run('UPDATE jobs SET best_process = (SELECT id FROM processes WHERE f1_score_max IS NOT NULL AND job_id = (SELECT id FROM jobs WHERE uuid = ?)  ORDER BY f1_score_max DESC LIMIT 1) WHERE uuid = ?', { 1: uuid, 2: uuid });

  if (parseInt(out1.count, 10) === 0 && procs.length > 0) {
    db.run('UPDATE jobs SET job_status_id = (SELECT id FROM job_statuses WHERE name = "completed"), ended_at = ? WHERE uuid = ?', { 1: out2.ended_at ? out2.ended_at : now(), 2: uuid });
  }
}

function updateJobField(uuid, col, val) {
  db.run(`UPDATE jobs SET ${col} = ? WHERE uuid = ?`, val, uuid);
}

async function getJobs() {
  const jobs = await db.all('SELECT uuid,friendly_name FROM jobs');

  return jobs;
}

async function setJobErrored(uuid) {
  await db.run(
    'UPDATE jobs SET job_status_id = (SELECT id FROM job_statuses WHERE name = "errored"), ended_at = $ended_at WHERE uuid = $uuid',
    {
      $ended_at: now(),
      $uuid: uuid,
    },
  );
}

module.exports = {
  calculateProcessDuration,
  getAlgorithm,
  getAlgorithmConfig,
  getAlgorithmConfigs,
  getAlgorithms,
  getJob,
  getJobs,
  getProcess,
  getProcesses,
  jobStatusUpdateCheck,
  newJob,
  newProcess,
  now,
  updateProcessF1ScoreMax,
  updateProcessField,
  updateJobField,
  updateProcessStatus,
  setJobErrored,
};
