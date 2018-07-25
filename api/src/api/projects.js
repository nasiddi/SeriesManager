const express = require('express');
const fs = require('fs-extra');
const uuidv1 = require('uuid/v1');
const db = require('sqlite');
const winston = require('winston');
const md5File = require('md5-file');
const _ = require('lodash');
const python = require('../python/controller');

const routes = express.Router();

async function getProject(req, res) {
  const project = await db.get(
    'SELECT * FROM projects WHERE uuid = $uuid AND user_id = $user_id',
    {
      $user_id: req.jwt.sub,
      $uuid: req.params.uuid,
    },
  );
  if (!project) {
    res.sendStatus(404).end();
  }
  const file = await db.get(
    'SELECT * FROM files WHERE id = $id',
    {
      $id: project.file_id,
    },
  );
  project.file = file;
  return project;
}

routes.get('/', async (req, res) => {
  const projects = await db.all(
    'SELECT * FROM projects WHERE user_id = $user_id',
    {
      $user_id: req.jwt.sub,
    },
  );

  res.json(projects);
});

routes.get('/:uuid', async (req, res) => {
  res.json(await getProject(req, res));
});

routes.get('/:uuid/jobs', async (req, res) => {
  const project = await getProject(req, res);
  const jobs = await db.all(
    'SELECT * FROM jobs WHERE (file_id_data = $file_id OR file_id_train = $file_id OR file_id_test = $file_id) AND user_id = $user_id',
    {
      $file_id: project.file_id,
      $user_id: req.jwt.sub,
    },
  );

  res.json(jobs);
});


routes.post('/', async (req, res) => {
  const uuid = uuidv1();

  const file = await db.get(
    'SELECT * FROM files WHERE uuid = $uuid',
    {
      $uuid: req.body.file_uuid,
    },
  );

  const config = _.merge(JSON.parse(file.corpus_analysis_config), JSON.parse(req.body.config));

  await db.run(
    'INSERT INTO projects (user_id, uuid, friendly_name, corpus_analysis_config, file_id) VALUES ($user_id, $uuid, $friendly_name, $corpus_analysis_config, $file_id)',
    {
      $user_id: req.jwt.sub,
      $uuid: uuid,
      $friendly_name: req.body.name,
      $file_id: file.id,
      $corpus_analysis_config: JSON.stringify(config),
    },
  );

  python.corpusAnalysis(uuid);

  res.send(uuid);
});


function getFileHash(file) {
  let hash = '00000000000000000000000000000000';

  if (fs.existsSync(file)) {
    hash = md5File.sync(file);
  }

  return hash;
}

routes.get('/:uuid/corpus_analysis', async (req, res) => {
  const project = await getProject(req, res);

  res.append('X-File-Hash', getFileHash(project.filepath_corpus_analysis));

  if (!fs.existsSync(project.filepath_corpus_analysis)) {
    res.sendStatus(204).end();
    return;
  }

  fs.readJson(project.filepath_corpus_analysis, (err, file) => {
    if (err) {
      winston.error(err);
      res.sendStatus(500).end();
    }

    res.json(file);
  });
});

routes.get('/:uuid/corpus_analysis/check', async (req, res) => {
  const project = await getProject(req, res);
  res.append('X-File-Hash', getFileHash(project.filepath_corpus_analysis)).send();
});

module.exports = { routes };
