/* eslint no-console: 0 */
/* eslint no-undef: 0 */
/* eslint max-len: 0 */
/* eslint no-unused-vars: 0 */
const winston = require('winston');
const db = require('sqlite');
const { spawn } = require('child_process');
const fs = require('fs-extra');
const path = require('path');
const tmp = require('tmp');
const _ = require('lodash');
const config = require('./../../config');
const queries = require('./../db/queries');
const proc = require('./../models/process');
const {
  convertArguments,
  resolveCwd,
  executableMagic,
  replaceConstants,
  doneEvaluationFileName,
  rawOutputFileName,
  evaluationOutputFileName,
} = require('./helpers');

function printOutput(child, uuid) {
  child.stdout.on('data', (data) => {
    winston.debug(`stdout (PID: ${child.pid}, uuid: ${uuid}):\n${data}`);
  });

  child.stderr.on('data', (data) => {
    winston.debug(`stderr (PID: ${child.pid}, uuid: ${uuid}):\n${data}`);
  });

  child.on('close', (code) => {
    const text = `child process (PID: ${child.pid}, ${uuid}) exited with code ${code}`;
    if (code === 0) {
      winston.info(text);
    } else {
      winston.error(text);
    }
  });
}

async function getFromProjectId(id) {
  const project = await db.get('SELECT * FROM projects WHERE id = $id', {
    $id: id,
  });

  const file = await db.get('SELECT * FROM files WHERE id = $id', {
    $id: project.file_id,
  });

  return {
    project,
    file,
  };
}

async function getFromProject(uuid) {
  const id = await db.get('SELECT id FROM projects WHERE uuid = $uuid', {
    $uuid: uuid,
  });

  const { project, file } = await getFromProjectId(id.id);
  return {
    project,
    file,
  };
}

async function getFromJobId(id) {
  const job = await db.get('SELECT * FROM jobs WHERE id = $id', {
    $id: id,
  });

  const jobFiles = {
    data: false,
    train: false,
    test: false,
  };

  if (job.file_id_data) {
    jobFiles.data = await db.get('SELECT * FROM files WHERE id = $id', {
      $id: job.file_id_data,
    });
  }

  if (job.file_id_train) {
    jobFiles.train = await db.get('SELECT * FROM files WHERE id = $id', {
      $id: job.file_id_train,
    });
  }

  if (job.file_id_test) {
    jobFiles.test = await db.get('SELECT * FROM files WHERE id = $id', {
      $id: job.file_id_test,
    });
  }

  return {
    job,
    jobFiles,
  };
}

async function getFromJob(uuid) {
  const id = await db.get('SELECT id FROM jobs WHERE uuid = $uuid', {
    $uuid: uuid,
  });

  const { job, jobFiles } = await getFromJobId(id.id);

  return {
    job,
    jobFiles,
  };
}

async function getFromProcess(processId) {
  const process = await db.get('SELECT * FROM processes WHERE id = $id', {
    $id: processId,
  });

  const algorithmConfig = await db.get('SELECT * FROM algorithm_configs WHERE id = $id', {
    $id: process.algorithm_config_id,
  });

  const algorithm = await db.get('SELECT * FROM algorithms WHERE id = $id', {
    $id: algorithmConfig.algorithm_id,
  });

  const { job, jobFiles } = await getFromJobId(process.job_id);

  return {
    process,
    job,
    algorithm,
    algorithmConfig,
    jobFiles,
  };
}

async function run(
  what,
  uuid,
  dataFile,
  configString,
  outputFile,
  childRunningCallback,
  exitCallback,
) {
  const cwd = resolveCwd('$BACKEND$');
  const executable = executableMagic('python', cwd);

  const configFile = tmp.fileSync();
  let args = '';
  if (_.isObject(dataFile)) {
    args = replaceConstants(
      convertArguments(
        `["${what}.py", "--output=$output$", "--config=$config$", "--train=$train$", "--test=$test$"]`,
      ),
      {
        output: outputFile,
        config: configFile.name,
        train: dataFile.train,
        test: dataFile.test,
      },
    );
  } else if (dataFile) {
    args = replaceConstants(
      convertArguments(`["${what}.py", "--output=$output$", "--config=$config$", "--data=$data$"]`),
      {
        output: outputFile,
        config: configFile.name,
        data: dataFile,
      },
    );
  } else {
    args = replaceConstants(
      convertArguments(`["${what}.py", "--output=$output$", "--config=$config$"]`),
      {
        output: outputFile,
        config: configFile.name,
      },
    );
  }

  fs.writeFileSync(
    configFile.name,
    _.isObject(configString) ? JSON.stringify(configString) : configString,
  );

  const child = spawn(executable, args, {
    cwd,
  });

  winston.verbose(`started ${what} for ${uuid} with PID ${child.pid}`);
  winston.verbose(JSON.stringify(args));
  winston.debug(`temporary config file is located at ${configFile.name}`);
  winston.debug(`output will be written to ${outputFile}`);

  printOutput(child, uuid);

  childRunningCallback(child);

  child.on('exit', async (code, signal) => {
    try {
      if (config.cleanup) {
        configFile.removeCallback();
      }
      exitCallback(code, signal);
      winston.info(`${what} done for ${uuid}`);
    } catch (e) {
      winston.error(e);
    }
  });
}

async function corpusAnalysis(uuid) {
  const { project, file } = await getFromProject(uuid);

  const outputFile = path.join(config.directories.corpusAnalysis, uuid);

  await db.run(
    'UPDATE projects SET filepath_corpus_analysis = $location, is_corpus_analyzed = 0 WHERE uuid = $uuid',
    {
      $uuid: uuid,
      $location: outputFile,
    },
  );

  run(
    'corpus_analysis',
    uuid,
    file.filepath_parsed,
    project.corpus_analysis_config,
    outputFile,
    () => {},
    async (code) => {
      if (code === 0) {
        await db.run('UPDATE projects SET is_corpus_analyzed = 1 WHERE uuid = $uuid', {
          $uuid: uuid,
        });
      }
    },
  );
}

async function reloadSeries(res) {
  await run(
    'series_loader',
    'series_loader',
    '',
    '',
    '',
    () => {},
    async (code, signal) => {
      if (code === 0) {
        result = 'done';
      } else {
        result = 'failed';
      }
      res.send(result);
    },
  );
}

async function unlockShows(res) {
  await run(
    'unlock_shows',
    'unlock_shows',
    '',
    '',
    '',
    () => {},
    async (code, signal) => {
      if (code === 0) {
        result = 'done';
      } else {
        result = 'failed';
      }
      res.send(result);
    },
  );
}

async function prepFiles(res) {
  const outputFile = path.join(config.directories.storage, 'names');
  await run(
    'file_loader',
    '',
    '',
    '',
    outputFile,
    () => {},
    async (code, signal) => {
      if (!fs.existsSync(outputFile)) {
        res.sendStatus(204).end();
        return;
      }

      fs.readJson(outputFile, (err, file) => {
        if (err) {
          winston.error(err);
          res.sendStatus(500).end();
        }
        fs.unlink(outputFile);
        res.json(file);
      });
    },
  );
}

async function getStats(res) {
  const outputFile = path.join(config.directories.storage, 'stats');
  await run(
    'stats',
    '',
    '',
    '',
    outputFile,
    () => {},
    async (code, signal) => {
      if (!fs.existsSync(outputFile)) {
        res.sendStatus(204).end();
        return;
      }

      fs.readJson(outputFile, (err, file) => {
        if (err) {
          winston.error(err);
          res.sendStatus(500).end();
        }
        fs.unlink(outputFile);
        res.json(file);
      });
    },
  );
}

async function batchFiles(res) {
  const outputFile = path.join(config.directories.storage, 'batchFiles');
  console.log('hi there');
  await run(
    'batch_files',
    '',
    '',
    '',
    outputFile,
    () => {},
    async (code, signal) => {
      if (!fs.existsSync(outputFile)) {
        res.sendStatus(204).end();
        return;
      }

      fs.readJson(outputFile, (err, file) => {
        if (err) {
          winston.error(err);
          res.sendStatus(500).end();
        }
        fs.unlink(outputFile);
        res.json(file);
      });
    },
  );
}

async function updatePrep(res) {
  const outputFile = path.join(config.directories.storage, 'update_prep');
  await run(
    'update_prep',
    '',
    '',
    '',
    outputFile,
    () => {},
    async (code, signal) => {
      if (!fs.existsSync(outputFile)) {
        res.sendStatus(204).end();
        return;
      }

      fs.readJson(outputFile, (err, file) => {
        if (err) {
          winston.error(err);
          res.sendStatus(500).end();
        }
        fs.unlink(outputFile);
        res.json(file);
      });
    },
  );
}

async function updateSave(body, res) {
  const outputFile = path.join(config.directories.storage, 'update_save');
  console.log(body[0]);
  await run(
    'update_save',
    '',
    '',
    body,
    outputFile,
    () => {},
    async (code, signal) => {
      if (!fs.existsSync(outputFile)) {
        res.sendStatus(204).end();
        return;
      }

      fs.readJson(outputFile, (err, file) => {
        if (err) {
          winston.error(err);
          res.sendStatus(500).end();
        }
        fs.unlink(outputFile);
        res.json(file);
      });
    },
  );
}

async function syncFiles(body, res) {
  const outputFile = path.join(config.directories.storage, 'synced');
  await run(
    'syncer',
    '',
    '',
    body,
    outputFile,
    () => {},
    async (code, signal) => {
      if (!fs.existsSync(outputFile)) {
        res.sendStatus(204).end();
        return;
      }

      fs.readJson(outputFile, (err, file) => {
        if (err) {
          winston.error(err);
          res.sendStatus(500).end();
        }
        fs.unlink(outputFile);
        fs.unlink(body);
        res.json(file);
      });
    },
  );
}

async function batchMatch(body, res) {
  const outputFile = path.join(config.directories.storage, 'batch_validate');
  await run(
    'batch_match',
    '',
    body,
    '',
    outputFile,
    () => {},
    async (code, signal) => {
      if (!fs.existsSync(outputFile)) {
        res.sendStatus(204).end();
        return;
      }

      fs.readJson(outputFile, (err, file) => {
        if (err) {
          winston.error(err);
          res.sendStatus(500).end();
        }
        res.json(file);
        fs.unlink(outputFile);
      });
    },
  );
}

async function batchSync(body, res) {
  const outputFile = path.join(config.directories.storage, 'batch_report');
  console.log(body[0]);
  await run(
    'batch_sync',
    '',
    '',
    body,
    outputFile,
    () => {},
    async (code, signal) => {
      if (!fs.existsSync(outputFile)) {
        res.sendStatus(204).end();
        return;
      }

      fs.readJson(outputFile, (err, file) => {
        if (err) {
          winston.error(err);
          res.sendStatus(500).end();
        }
        res.json(file);
        fs.unlink(outputFile);
      });
    },
  );
}

async function fileTree(body, res) {
  const outputFile = path.join(config.directories.storage, 'file_tree');
  console.log(body[0]);
  await run(
    'file_tree',
    '',
    '',
    body,
    outputFile,
    () => {},
    async (code, signal) => {
      if (!fs.existsSync(outputFile)) {
        res.sendStatus(204).end();
        return;
      }

      fs.readJson(outputFile, (err, file) => {
        if (err) {
          winston.error(err);
          res.sendStatus(500).end();
        }
        res.json(file);
      });
    },
  );
}

async function preprocess(uuid, exitCallback) {
  const { job, jobFiles } = await getFromJob(uuid);
  const file = jobFiles.data ? jobFiles.data : jobFiles.test;

  const outputFile = path.join(config.directories.models, `${job.uuid}`);
  const data = jobFiles.data
    ? jobFiles.data.filepath_parsed
    : {
      train: jobFiles.train.filepath_parsed,
      test: jobFiles.test.filepath_parsed,
    };
  const startConfig = JSON.parse(job.start_config);

  run(
    'preprocess',
    uuid,
    data,
    {
      columnMapping: JSON.parse(file.corpus_analysis_config).columnMapping,
      header: JSON.parse(file.corpus_analysis_config).header,
      sentence_tokenizer: startConfig.tokenizers.sentence,
      word_tokenizer: startConfig.tokenizers.word,
      single_entry: null,
      evaluate: 0,
    },
    outputFile,
    () => {},
    async (code, signal) => {
      if (code === 0) {
        await db.run(
          'UPDATE jobs SET filepath_preprocessed = $filepath_preprocessed WHERE uuid = $uuid',
          {
            $filepath_preprocessed: outputFile,
            $uuid: job.uuid,
          },
        );
      }
      exitCallback(code, signal);
    },
  );
}

async function preprocessEvaluate(processId, evalId, input, exitCallback) {
  const { job } = await getFromProcess(processId);

  const outputFile = path.join(config.directories.models, `${job.uuid}`);
  const startConfig = JSON.parse(job.start_config);

  const isFile = input.type === 'file';
  let file;
  if (isFile) {
    file = await db.get('SELECT * FROM files WHERE uuid = $uuid', {
      $uuid: input.value,
    });
  }

  run(
    'preprocess',
    evalId,
    isFile ? file.filepath_parsed : null,
    {
      columnMapping: isFile ? JSON.parse(file.corpus_analysis_config).columnMapping : {},
      header: isFile ? JSON.parse(file.corpus_analysis_config).header : {},
      sentence_tokenizer: startConfig.tokenizers.sentence,
      word_tokenizer: startConfig.tokenizers.word,
      single_entry: !isFile ? input.value : null,
      evaluate: 1,
    },
    outputFile,
    () => {},
    async (code, signal) => {
      exitCallback(code, signal);
    },
  );
}

async function classification(processId, exitCallback) {
  const { job, algorithm, jobFiles } = await getFromProcess(processId);
  const file = jobFiles.data ? jobFiles.data : jobFiles.test;

  const ws = fs.createWriteStream(rawOutputFileName(job.uuid, processId), { flags: 'w' });
  const outputFile = path.join(config.directories.classification, `${job.uuid}/${processId}`);
  const watcher = proc.watchJsonOutput(processId, outputFile);

  run(
    'classification',
    job.uuid,
    job.filepath_preprocessed,
    _.merge(JSON.parse(algorithm.config_base), {
      columnMapping: JSON.parse(file.corpus_analysis_config).columnMapping,
      evaluate: 0,
    }),
    outputFile,
    (child) => {
      queries.updateProcessStatus(processId, 'running');
      queries.updateProcessField(processId, 'pid', child.pid);
      child.stdout.pipe(ws);
      child.stderr.pipe(ws);
    },
    (code, signal) => {
      proc.onExit(processId, code, ws, watcher);
      proc.readJsonToDatabase(processId, outputFile);
      exitCallback(code, signal, outputFile);
    },
  );
}

async function classificationEvaluate(processId, evalId, input, exitCallback) {
  const { job, algorithm } = await getFromProcess(processId);

  const doneFile = doneEvaluationFileName(evalId, processId);
  const jsonOutput = evaluationOutputFileName(evalId, processId);

  const outputFile = path.join(config.directories.models, `${job.uuid}`);

  const isFile = input.type === 'file';
  let file;
  if (isFile) {
    file = await db.get('SELECT * FROM files WHERE uuid = $uuid', {
      $uuid: input.value,
    });
  }

  run(
    'classification',
    job.uuid,
    outputFile,
    _.merge(JSON.parse(algorithm.config_base), {
      columnMapping: isFile ? JSON.parse(file.corpus_analysis_config).columnMapping : {},
      evaluate: 1,
    }),
    jsonOutput,
    () => {},
    (code, signal) => {
      fs.closeSync(fs.openSync(doneFile, 'w'));
      exitCallback(code, signal);
    },
  );
}

async function baseline(uuid, exitCallback) {
  const { job, jobFiles } = await getFromJob(uuid);
  const file = jobFiles.data ? jobFiles.data : jobFiles.test;

  const outputFile = path.join(config.directories.classification, `${uuid}/base`);

  run(
    'classification',
    uuid,
    job.filepath_preprocessed,
    {
      columnMapping: JSON.parse(file.corpus_analysis_config).columnMapping,
      evaluate: 0,
      classifier: 'base',
    },
    outputFile,
    () => {},
    (code, signal) => {
      exitCallback(code, signal, outputFile);
    },
  );
}

async function reload(exitCallback) {
  const outputFile = path.join(config.directories.classification, '/base');
  run(
    'classification',
    {
      reload: 0,
    },
    outputFile,
    () => {},
    (code, signal) => {
      exitCallback(code, signal, outputFile);
    },
  );
}

async function compareClassifiers(uuid, baseDir, exitCallback) {
  const dataFile = path.join(baseDir, `${uuid}`);
  const outputFile = path.join(baseDir, `${uuid}/comparison`);

  run(
    'compare_classifiers',
    uuid,
    dataFile,
    null,
    outputFile,
    () => {},
    (code, signal) => {
      exitCallback(code, signal, outputFile);
    },
  );
}

module.exports = {
  corpusAnalysis,
  preprocess,
  preprocessEvaluate,
  classification,
  classificationEvaluate,
  baseline,
  compareClassifiers,
  reloadSeries,
  prepFiles,
  syncFiles,
  updatePrep,
  updateSave,
  batchFiles,
  batchMatch,
  batchSync,
  unlockShows,
  getStats,
  fileTree,
};
