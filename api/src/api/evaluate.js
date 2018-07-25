const express = require('express');
const path = require('path');
const fs = require('fs-extra');
const evaluate = require('./../models/evaluate');
const { evaluationOutputFileName } = require('./../python/helpers');
const python = require('./../python/controller');
const config = require('../../config');

const routes = express.Router();

routes.post('/:evaluation/compare_classifiers', async (req, res) => {
  python.compareClassifiers(
    req.params.evaluation,
    config.directories.evaluation,
    (code, signal, output) => {
      if (code === 0) {
        const data = fs.readJsonSync(output);
        res.json(data);
      } else {
        res.sendStatus(500);
      }
    },
  );
});

routes.post('/:evaluation/:process', async (req, res) => {
  res.send(await evaluate.start(
    req.params.process,
    req.params.evaluation,
    { type: req.body.type, value: req.body.value },
  ));
});

routes.get('/:evaluation/:process', async (req, res) => {
  res.send(await evaluate.check(req.params.process, req.params.evaluation));
});

routes.get('/:evaluation/:process/download', async (req, res) => {
  const file = `${evaluationOutputFileName(req.params.evaluation, req.params.process)}_csv`;
  res.download(file, `${req.params.evaluation}_${req.params.process}.csv`);
});

routes.get('/:uuid/download_comparison/:set', async (req, res) => {
  const file = `${path.join(config.directories.evaluation, req.params.uuid)}/comparison_${req.params.set}`;
  if (!fs.existsSync(file)) {
    res.sendStatus(404);
    return;
  }
  res.download(file, `${req.params.uuid}_${req.params.set}.csv`);
});

module.exports = { routes };
