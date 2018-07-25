const fs = require('fs-extra');
const _ = require('lodash');
const {
  evaluationOutputFileName,
  doneEvaluationFileName,
} = require('./../python/helpers');
const python = require('./../python/controller');

async function start(processId, evalId, input) {
  python.preprocessEvaluate(processId, evalId, input, () => {
    python.classificationEvaluate(processId, evalId, input, () => { });
  });
}

async function check(processId, evalId) {
  const doneFile = doneEvaluationFileName(evalId, processId);
  const output = evaluationOutputFileName(evalId, processId);

  if (!fs.existsSync(doneFile)) {
    return { label: null, status: 'running', download: false };
  }

  const status = 'done';
  let data;

  try {
    data = fs.readJsonSync(output);
  } catch (error) {
    data = {};
  }

  const extraData = _.defaultTo(data.final_output, {});

  if ('predict' in data) {
    return {
      label: data.predict,
      status,
      extraData,
    };
  }


  if (fs.existsSync(`${output}_csv`)) {
    return {
      label: false,
      status,
      download: true,
      extraData,
    };
  }

  return {
    label: false,
    status,
    extraData,
  };
}

module.exports = {
  check,
  start,
};
