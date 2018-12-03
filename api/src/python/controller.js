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
  const outputFile = path.join(config.directories.storage, 'sync_prep');
  await run(
    'sync_prep',
    '',
    '',
    '',
    outputFile,
    () => {},
    async (code, signal) => {
      if (code !== 0) {
        res.send('failed');
        return;
      }
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
      if (code !== 0) {
        res.send('failed');
        return;
      }
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
      if (code !== 0) {
        res.send('failed');
        return;
      }
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
      if (code !== 0) {
        res.send('failed');
        return;
      }
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
      if (code !== 0) {
        res.send('failed');
        return;
      }
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
      if (code !== 0) {
        res.send('failed');
        return;
      }
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
      if (code !== 0) {
        res.send('failed');
        return;
      }
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
      if (code !== 0) {
        res.send('failed');
        return;
      }
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
  await run(
    'file_tree',
    '',
    '',
    body,
    outputFile,
    () => {},
    async (code, signal) => {
      if (code !== 0) {
        res.send('failed');
        return;
      }
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

async function saveFileTree(body, res) {
  const outputFile = path.join(config.directories.storage, 'file_tree');
  fs.writeJSON(outputFile, body.tree, (err) => {
    if (err) {
      winston.error(err);
    }
  });
  await run(
    'save_file_tree',
    '',
    '',
    body.error,
    outputFile,
    () => {},
    async (code, signal) => {
      if (code !== 0) {
        res.send('failed');
        return;
      }
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

async function missingFiles(body, res) {
  const outputFile = path.join(config.directories.storage, 'missing_files');
  console.log(body[0]);
  await run(
    'missing_files',
    '',
    '',
    '',
    outputFile,
    () => {},
    async (code, signal) => {
      if (code !== 0) {
        res.send('failed');
        return;
      }
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

async function wordSearch(body, res) {
  const outputFile = path.join(config.directories.storage, 'word_search');
  console.log(body[0]);
  await run(
    'word_search',
    '',
    '',
    '',
    outputFile,
    () => {},
    async (code, signal) => {
      if (code !== 0) {
        res.send('failed');
        return;
      }
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

async function saveWords(body, res) {
  const outputFile = path.join(config.directories.storage, 'save_words');
  console.log(body[0]);
  await run(
    'save_words',
    '',
    '',
    body,
    outputFile,
    () => {},
    async (code, signal) => {
      if (code !== 0) {
        res.send('failed');
        return;
      }
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

async function errorSearch(body, res) {
  const outputFile = path.join(config.directories.storage, 'errors');
  console.log(body[0]);
  await run(
    'error_search',
    '',
    '',
    body,
    outputFile,
    () => {},
    async (code, signal) => {
      if (code !== 0) {
        res.send('failed');
        return;
      }
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

async function editExceptionFile(res) {
  const outputFile = path.join(config.directories.storage, 'edit_exceptionfile');
  await run(
    'edit_exceptionfile',
    '',
    '',
    '',
    outputFile,
    () => {},
    async (code, signal) => {
      if (code !== 0) {
        res.send('failed');
        return;
      }
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

async function saveExceptionFile(body, res) {
  await run(
    'save_exceptionfile',
    '',
    '',
    body,
    '',
    () => {},
    async (code, signal) => {
      if (code !== 0) {
        res.send('failed');
        return;
      }

      res.send('done');
    },
  );
}

module.exports = {
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
  saveFileTree,
  missingFiles,
  wordSearch,
  saveWords,
  errorSearch,
  editExceptionFile,
  saveExceptionFile,
};
