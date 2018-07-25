const express = require('express');
const db = require('sqlite');
const path = require('path');
const fs = require('fs-extra');
const jobModel = require('./../models/job');
const processModel = require('./../models/process');
const config = require('../../config');
const python = require('../python/controller');


const routes = express.Router();


routes.post('/reload', async (req, res) => {
  python.reloadSeries(res);
});

routes.post('/sync/start', async (req, res) => {
  python.syncFiles(req.body, res);
});

routes.get('/names', async (req, res) => {
  python.prepFiles(res)
});

routes.get('/', async (req, res) => {
  res.send(await jobModel.getAll());
});

routes.get('/:uuid', async (req, res) => {
  res.send(await jobModel.get(req.params.uuid));
});

routes.get('/:uuid/projects', async (req, res) => {
  const job = await db.get(
    'SELECT * FROM jobs WHERE uuid = $uuid',
    {
      $uuid: req.params.uuid,
    },
  );

  const projects = await db.all(
    'SELECT * FROM projects WHERE file_id IN ($file_data, $file_train, $file_test) AND user_id = $user_id AND file_id IS NOT NULL',
    {
      $file_data: job.file_id_data,
      $file_train: job.file_id_train,
      $file_test: job.file_id_test,
      $user_id: req.jwt.sub,
    },
  );

  res.json(projects);
});

routes.get('/:uuid/processes', async (req, res) => {
  res.send(await processModel.getAll(req.params.uuid));
});

routes.get('/:uuid/download_comparison/:set', async (req, res) => {
  const file = `${path.join(config.directories.classification, req.params.uuid)}/comparison_${req.params.set}`;
  if (!fs.existsSync(file)) {
    res.sendStatus(404);
    return;
  }
  res.download(file, `${req.params.uuid}_${req.params.set}.csv`);
});

module.exports = { routes };
