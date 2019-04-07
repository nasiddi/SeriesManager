/* eslint-disable no-param-reassign */
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

function printOutput(child) {
  child.stdout.on('data', (data) => {
    winston.debug(`stdout (PID: ${child.pid}):\n${data}`);
  });

  child.stderr.on('data', (data) => {
    winston.debug(`stderr (PID: ${child.pid}):\n${data}`);
  });

  child.on('close', (code) => {
    const text = `child process (PID: ${child.pid}) exited with code ${code}`;
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

  winston.verbose(`started ${what} with PID ${child.pid}`);
  // winston.verbose(JSON.stringify(args));
  // winston.debug(`temporary config file is located at ${configFile.name}`);
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

async function reloadSeries(body, res) {
  console.log(body);
  await run(
    'series_loader',
    'series_loader',
    '',
    body,
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

async function prepFiles(body, res) {
  const outputFile = path.join(config.directories.storage, 'sync_prep');
  await run(
    'sync_prep',
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

async function batchSync(body, res) {
  const outputFile = path.join(config.directories.storage, 'batch_report');
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
        fs.unlink(outputFile);
        res.json(file);
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
        fs.unlink(outputFile);
        res.json(file);
      });
    },
  );
}

async function saveFileTree(body, res) {
  const outputFile = path.join(config.directories.storage, 'file_tree');
  await run(
    'save_file_tree',
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

async function missingFiles(body, res) {
  const outputFile = path.join(config.directories.storage, 'missing_files');
  const filterFile = path.join(config.directories.storage, 'missing_filter');
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
        if (fs.existsSync(filterFile)) {
          fs.readJson(filterFile, (errFilter, filter) => {
            if (errFilter) {
              winston.error(errFilter);
              res.sendStatus(500).end();
            }
            file.filter = filter;
            fs.unlink(outputFile);
            res.json(file);
          });
        } else {
          fs.writeJSON(filterFile, [], (err2) => {
            if (err2) {
              winston.error(err2);
              res.sendStatus(500).end();
            }
          });
          file.filter = [];
          fs.unlink(outputFile);
          res.json(file);
        }
      });
    },
  );
}

async function wordSearch(body, res) {
  const outputFile = path.join(config.directories.storage, 'word_search');
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
        fs.unlink(outputFile);
        res.json(file);
      });
    },
  );
}

async function saveWords(body, res) {
  const outputFile = path.join(config.directories.storage, 'save_words');
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
        fs.unlink(outputFile);
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
  const outputFile = path.join(config.directories.storage, 'save_exceptionfile');
  await run(
    'save_exceptionfile',
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

async function backUp(res) {
  const outputFile = path.join(config.directories.storage, 'backup');
  await run(
    'backup',
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

async function getBackUp(res) {
  const outputFile = path.join(config.directories.storage, 'get_backups');
  await run(
    'get_backups',
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

async function restoreBackUp(body, res) {
  const outputFile = path.join(config.directories.storage, 'restore_backup');
  await run(
    'restore_backup',
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

async function titleQuiz(body, res) {
  const outputFile = path.join(config.directories.storage, 'title_quiz');
  await run(
    'title_quiz',
    '',
    '',
    body,
    outputFile,
    () => { },
    async (code, signal) => {
      if (code !== 0) {
        res.send('failed');
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

async function titleQuizPrep(res) {
  const outputFile = path.join(config.directories.storage, 'title_quiz_prep');
  await run(
    'title_quiz_prep',
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

async function loadLog(res) {
  const outputFile = path.join(config.directories.storage, 'loadLog');
  await run(
    'load_logs',
    '',
    '',
    '',
    outputFile,
    () => { },
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
  editExceptionFile,
  saveExceptionFile,
  backUp,
  getBackUp,
  restoreBackUp,
  titleQuizPrep,
  titleQuiz,
};
