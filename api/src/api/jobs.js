/* eslint no-console: 0 */
/* eslint no-undef: 0 */
/* eslint max-len: 0 */

const express = require('express');
const db = require('sqlite');
const path = require('path');
const fs = require('fs-extra');
const TVDB = require('node-tvdb');
const jobModel = require('./../models/job');
const processModel = require('./../models/process');
const config = require('../../config');
const python = require('../python/controller');

const tvdb = new TVDB('C9BPCUYZ8GFT2BZL');

const routes = express.Router();

routes.post('/unlock', async (req, res) => {
  python.unlockShows(res);
});

routes.post('/update/prep', async (req, res) => {
  python.updatePrep(res);
});

routes.post('/batch/files', async (req, res) => {
  python.batchFiles(res);
});

routes.post('/batch/sync', async (req, res) => {
  python.batchSync(req.body, res);
});

routes.post('/reload', async (req, res) => {
  python.reloadSeries(res);
});

routes.post('/filetree', async (req, res) => {
  python.fileTree(req.body, res);
});

routes.post('/stats', async (req, res) => {
  python.getStats(res);
});

routes.post('/sync/start', async (req, res) => {
  python.syncFiles(req.body, res);
});

routes.post('/update/save', async (req, res) => {
  python.updateSave(req.body, res);
});

routes.post('/batch/match', async (req, res) => {
  const outputFile = path.join(config.directories.storage, 'batch_match');

  fs.writeJSON(outputFile, req.body, (err) => {
    console.log('req.body');
    console.log(req.body);
    if (err) {
      winston.error(err);
      res.sendStatus(500).end();
    }
    res.json(outputFile);
  });
});

routes.post('/batch/start', async (req, res) => {
  const inputFile = path.join(config.directories.storage, 'batch_match');
  python.batchMatch(inputFile, res);
});

routes.get('/sync/prep', async (req, res) => {
  python.prepFiles(res);
});

// TVDB
routes.post('/tvdb', async (req, res) => {
  console.log(req.body.series_name);
  if (req.body.new_series && req.body.tvdb_id === '') {
    console.log('New Series');
    res.send(
      await tvdb.getSeriesByName(req.body.series_name).then((response) => {
        const shows = [];
        response.forEach((s) => {
          shows.push({
            text: `${s.seriesName} | ${s.firstAired} | ${s.network}`,
            value: s.id,
          });
          console.log(`${s.seriesName} | ${s.firstAired} | ${s.network}`);
        });
        return { newShows: shows, select: shows[0].text };
      }),
    );
    return;
  }
  res.send(
    await tvdb
      .getEpisodesBySeriesId(req.body.tvdb_id)
      .then((response) => {
        console.log(response[response.length - 1]);
        if ('batch' in req.body) {
          return response;
        }
        let episode2 = null;
        let episode3 = null;
        const titles = {};
        const episode = response.find(
          obj => obj.airedSeason === req.body.s_nr && obj.airedEpisodeNumber === req.body.e_nr,
        );
        if (req.body.episode_option !== 'Single') {
          episode2 = response.find(
            obj => obj.airedSeason === req.body.s_nr && obj.airedEpisodeNumber === req.body.e_nr + 1,
          );
        }
        if (req.body.episode_option === 'Triple') {
          episode3 = response.find(
            obj => obj.airedSeason === req.body.s_nr && obj.airedEpisodeNumber === req.body.e_nr + 2,
          );
        }
        if (episode != null && 'episodeName' in episode) {
          titles.title = episode.episodeName;
        }
        if (episode2 != null && 'episodeName' in episode2) {
          titles.title2 = episode2.episodeName;
        }
        if (episode3 != null && 'episodeName' in episode3) {
          titles.title3 = episode3.episodeName;
        }
        console.log(titles);
        return titles;
      })
      .catch((error) => {
        console.log(error);
      }),
  );
});

routes.post('/tvdb/dates', async (req, res) => {
  res.send(
    await tvdb
      .getEpisodesBySeriesId(req.body.tvdb_id)
      .then((response) => {
        let counter = 1;
        while (
          response.length > counter
          && (response[response.length - counter].firstAired === ''
            || response[response.length - counter].airedSeason === 0)
        ) {
          counter += 1;
        }
        let finalDate = '';
        if (response.length !== counter) {
          finalDate = response[response.length - counter].firstAired;
        }
        console.log(`${response[0].firstAired} | ${finalDate}`);
        return { premiere: response[0].firstAired, final: finalDate };
      })
      .catch((error) => {
        console.log(error);
      }),
  );
});

routes.get('/', async (req, res) => {
  res.send(await jobModel.getAll());
});

routes.get('/:uuid', async (req, res) => {
  res.send(await jobModel.get(req.params.uuid));
});

routes.get('/:uuid/projects', async (req, res) => {
  const job = await db.get('SELECT * FROM jobs WHERE uuid = $uuid', {
    $uuid: req.params.uuid,
  });

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
  const file = `${path.join(config.directories.classification, req.params.uuid)}/comparison_${
    req.params.set
  }`;
  if (!fs.existsSync(file)) {
    res.sendStatus(404);
    return;
  }
  res.download(file, `${req.params.uuid}_${req.params.set}.csv`);
});

module.exports = { routes };
