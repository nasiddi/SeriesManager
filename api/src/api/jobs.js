const express = require('express');
const db = require('sqlite');
const path = require('path');
const fs = require('fs-extra');
const jobModel = require('./../models/job');
const processModel = require('./../models/process');
const config = require('../../config');
const python = require('../python/controller');
const TVDB = require('node-tvdb');
const tvdb = new TVDB('C9BPCUYZ8GFT2BZL');


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

// TVDB
routes.post('/tvdb', async (req, res) => {
  console.log(req.body)
  res.send(await tvdb.getEpisodesBySeriesId(req.body.tvdb)
    .then(response => {
      var episode2 = null;
      var episode3 = null;
      var titles = {};
      var episode = response.find(obj => {
        return obj.airedSeason === req.body.s_nr && obj.airedEpisodeNumber === req.body.e_nr
      })
      if (req.body.episode_option.selected !== 'Single') {
        episode2 = response.find(obj => {
        return obj.airedSeason === req.body.s_nr && obj.airedEpisodeNumber === req.body.e_nr + 1
        })
      }
      if (req.body.episode_option.selected === 'Triple') {
        episode3 = response.find(obj => {
        return obj.airedSeason === req.body.s_nr && obj.airedEpisodeNumber === req.body.e_nr + 2
        })
      }
      if (episode != null && 'episodeName' in episode){
        titles.title = episode.episodeName
      }
      if (episode2 != null && 'episodeName' in episode2){
        titles.title2 = episode2.episodeName
      }
      if (episode3 != null && 'episodeName' in episode3){
        titles.title3 = episode3.episodeName
      }
      console.log(titles)
      return titles
    })
    .catch(error => { console.log(error) }));
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
