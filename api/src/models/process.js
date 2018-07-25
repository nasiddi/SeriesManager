const fs = require('fs-extra');
const chokidar = require('chokidar');
const path = require('path');
const winston = require('winston');
const _ = require('lodash');
const db = require('./../db/queries');
const { rawOutputFileName } = require('./../python/helpers');
const queries = require('./../db/queries');

async function onExit(processId, code, ws, watcher) {
  const proc = await db.getProcess(processId);
  const uuid = proc.job_uuid;
  await db.updateProcessField(processId, 'ended_at', db.now());
  await db.updateProcessField(processId, 'exit_code', code);
  await db.updateProcessField(processId, 'progress', 100);
  await db.updateProcessStatus(processId, code === 0 ? 'completed' : 'errored');
  await db.updateProcessField(processId, 'output_text', fs.readFileSync(ws.path, 'utf-8'));
  ws.close();
  await db.jobStatusUpdateCheck(uuid);
  await db.calculateProcessDuration(processId);
  watcher.close();

  await db.updateProcessF1ScoreMax(processId);

  // eslint-disable-next-line global-require
  const python = require('./../python/controller');
  // eslint-disable-next-line global-require
  const config = require('../../config');
  if (code === 0) {
    python.compareClassifiers(uuid, config.directories.classification, (code2, signal, output) => {
      if (code2 === 0) {
        const data = fs.readJsonSync(output);
        queries.updateJobField(uuid, 'classifier_comparison', JSON.stringify(data));
      }
    });
  }
}

function readJsonToDatabase(processId, file) {
  const data = JSON.parse(fs.readFileSync(file, 'utf-8'));

  if (data) {
    db.updateProcessField(processId, 'details_json', JSON.stringify(data));

    if ('final_output' in data) {
      if ('confusion_matrix' in data.final_output) {
        db.updateProcessField(processId, 'confusion_matrix', JSON.stringify(data.final_output.confusion_matrix));
      }

      if ('classification_report' in data.final_output) {
        db.updateProcessField(processId, 'classification_report', JSON.stringify(data.final_output.classification_report));
      }

      if ('f1_score' in data.final_output) {
        db.updateProcessField(processId, 'f1_score_final', data.final_output.f1_score);
        db.updateProcessField(processId, 'f1_score_current', data.final_output.f1_score);
        db.updateProcessF1ScoreMax(processId);
      }
    }

    if (data.has_epochs && _.size(data.epochs) > 0) {
      db.updateProcessField(processId, 'f1_score_current', _.last(data.epochs));
    }

    db.updateProcessF1ScoreMax(processId);
  }
}

function watchJsonOutput(processId, jsonOutput) {
  const watcher = chokidar.watch(path.resolve(jsonOutput, '..'), {
    persistent: true,
  });

  watcher.on('raw', (event, p, details) => {
    if (path.normalize(details.watchedPath) !== path.normalize(jsonOutput)) {
      return;
    }

    try {
      readJsonToDatabase(processId, jsonOutput);
    } catch (e) {
      winston.error(e);
    }
  });

  return watcher;
}

async function tail(uuid, processId) {
  const proc = await db.getProcess(processId);

  if (proc.process_status.type === 'dead') {
    return { status: 200, contents: proc.output_text };
  }

  const outFile = rawOutputFileName(uuid, processId);
  const stat = await fs.stat(outFile);

  if (!stat.isFile()) {
    return { status: 404, contents: null };
  }

  if (stat.size === 0) {
    return { status: 204, contents: null };
  }

  const contents = await fs.readFile(outFile);
  return { status: 206, contents };
}

async function kill(processId) {
  const { pid } = (await db.getProcess(processId));
  try {
    process.kill(pid, 'SIGTERM');
  } catch (e) {
    winston.error(`Failed to kill process ${processId} with PID ${pid}`);
  }
  setTimeout(() => { db.updateProcessStatus(processId, 'killed'); }, 1000);
}
async function getAll(uuid) {
  const processes = await db.getProcesses(uuid);
  return processes;
}


module.exports = {
  getAll,
  kill,
  onExit,
  tail,
  watchJsonOutput,
  readJsonToDatabase,
};
