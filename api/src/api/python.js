/* eslint no-console: 0 */
/* eslint no-undef: 0 */
/* eslint max-len: 0 */

const express = require('express');
const path = require('path');
const fs = require('fs-extra');
const TVDB = require('node-tvdb');
const config = require('../../config');
const python = require('../python/controller');

const routes = express.Router();

routes.post('/unlock', async (req, res) => {
  python.unlockShows(res);
});

routes.post('/exceptionfile/load', async (req, res) => {
  python.editExceptionFile(res);
});

routes.post('/exceptionfile/save', async (req, res) => {
  python.saveExceptionFile(req.body, res);
});

routes.post('/backup', async (req, res) => {
  python.backUp(res);
});

routes.post('/getbackup', async (req, res) => {
  python.getBackUp(res);
});

routes.post('/restorebackup', async (req, res) => {
  python.restoreBackUp(req.body, res);
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
  python.reloadSeries(req.body, res);
});

routes.post('/filetree', async (req, res) => {
  python.fileTree(req.body, res);
});

routes.post('/filetree/save', async (req, res) => {
  python.saveFileTree(req.body, res);
});

routes.post('/filetree/dictionary', async (req, res) => {
  python.wordSearch(req.body, res);
});

routes.post('/filetree/savedictionary', async (req, res) => {
  python.saveWords(req.body, res);
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

routes.post('/filetree/missing', async (req, res) => {
  python.missingFiles(req.body, res);
});

routes.post('/synclog', async (req, res) => {
  const outputFile = path.join(config.directories.storage, 'synclog');
  fs.readJson(outputFile, (err, file) => {
    if (err) {
      winston.error(err);
      res.sendStatus(500).end();
    }
    res.json(file.reverse());
  });
});

routes.post('/clearlog', async (req, res) => {
  const outputFile = path.join(config.directories.storage, 'synclog');
  const out = [];
  fs.writeJSON(outputFile, out, (err) => {
    if (err) {
      winston.error(err);
      res.sendStatus(500).end();
    }
    res.json(out);
  });
});

routes.post('/batch/match', async (req, res) => {
  python.batchMatch(req.body, res);
});

routes.post('/sync/prep', async (req, res) => {
  console.log(req);
  python.prepFiles(req.body, res);
});

routes.post('/filetree/missing/filter', async (req, res) => {
  const outputFile = path.join(config.directories.storage, 'missing_filter');
  console.log(req.body);
  delete req.body.key;
  console.log(req.body);
  fs.readJson(outputFile, (err, file) => {
    if (err) {
      winston.error(err);
      res.sendStatus(500).end();
    }
    file.push(req.body);
    fs.writeJSON(outputFile, file, (errInner) => {
      if (errInner) {
        winston.error(errInner);
        res.sendStatus(500).end();
      }
      res.json({ done: true });
    });
  });
});

// TVDB
routes.post('/tvdb', async (req, res) => {
  const tvdb = new TVDB('C9BPCUYZ8GFT2BZL');
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
  const tvdb = new TVDB('C9BPCUYZ8GFT2BZL');
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

module.exports = { routes };
