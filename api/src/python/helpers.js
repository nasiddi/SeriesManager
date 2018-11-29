const path = require('path');
const fs = require('fs-extra');
const _ = require('lodash');
const config = require('../../config');

function convertArguments(call, ...args) {
  const obj = JSON.parse(call);
  let arr = Object.keys(obj).map(k => obj[k]);
  arr = _.flatten([arr, ...args]);
  return arr;
}

function replaceConstants(args, mapping) {
  const x = _.map(args, (arg) => {
    const str = arg;
    const re = /\$([a-z]+)\$/;
    const found = str.match(re);

    if (found === null) {
      return arg;
    }

    return arg.replace(found[0], mapping[found[1]]);
  });
  return x;
}

function resolveCwd(cwd) {
  return path.resolve(cwd.replace('$BACKEND$', config.directories.backend));
}

function executableMagic(command, cwd) {
  if (command === 'python3.7') {
    const venv = path.join(cwd, 'venv');
    const venvPythonNix = path.join(venv, 'bin', 'python3.7');
    const venvPythonWin = path.join(venv, 'Scripts', 'python3.7.exe');
    const venvAnaconda = path.join(venv, 'python3.7.exe');

    if (fs.pathExistsSync(venvPythonNix)) {
      return path.resolve(venvPythonNix);
    }

    if (fs.pathExistsSync(venvPythonWin)) {
      return path.resolve(venvPythonWin);
    }

    if (fs.pathExistsSync(venvAnaconda)) {
      return path.resolve(venvAnaconda);
    }
    return command;
  }
  return command;
}

function rawOutputFileName(job, pc) {
  return path.join(config.directories.output, `${job}_${pc}`);
}

function doneEvaluationFileName(ev, pc) {
  return path.join(config.directories.evaluation, `${ev}/${pc}.done`);
}

function evaluationOutputFileName(ev, pc) {
  return path.join(config.directories.evaluation, `${ev}/${pc}`);
}


module.exports = {
  convertArguments,
  doneEvaluationFileName,
  executableMagic,
  evaluationOutputFileName,
  rawOutputFileName,
  replaceConstants,
  resolveCwd,
};
