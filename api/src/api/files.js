const os = require('os');
const express = require('express');
const fs = require('fs-extra');
const multer = require('multer');
const uuidv1 = require('uuid/v1');
const db = require('sqlite');
const path = require('path');
const winston = require('winston');
const _ = require('lodash');
const moment = require('moment');
require('lodash.product');
const Papa = require('papaparse');
const config = require('../../config');

const upload = multer({
  limits: {
    fieldSize: 100 * 1024 * 1024 * 1024,
  },
  storage: multer.diskStorage({
    destination: os.tmpdir(),
  }),
});

const routes = express.Router();

Papa.parsePromise = (fileStream, papaConfig) => new Promise(((complete, error) => {
  const mergedConfig = papaConfig;
  mergedConfig.complete = complete;
  mergedConfig.error = error;
  Papa.parse(fileStream, mergedConfig);
}));

async function getFile(req, res) {
  const file = await db.get(
    'SELECT * FROM files WHERE uuid = $uuid AND user_id = $user_id',
    {
      $user_id: req.jwt.sub,
      $uuid: req.params.uuid,
    },
  );
  if (!file) {
    res.sendStatus(404).end();
  }
  return file;
}

function guessHeaders(columns, data) {
  const cutoff = 100;
  const threshold = cutoff * 0.9;
  const preview = _.chain(data).tail().take(cutoff).value();
  const guesses = _.zipObject(
    columns,
    // eslint-disable-next-line consistent-return
    _.map(columns, (col) => {
      if (
        col.toLowerCase() === 'lang'
        || col.toLowerCase() === 'language'
      ) {
        return 'lang';
      }
      if (col.match(/(_|\b)ID(_|\b)/i) !== null) {
        return 'id';
      }
      if (col.match(/(_|\b)label(_|\b)/i) !== null) {
        return 'label';
      }
      if (col.match(/(_|\b)date(_|\b)/i) !== null) {
        return 'date';
      }
      if (
        col.match(/(_|\b)text(_|\b)/i) !== null
        || col.match(/(_|\b)tweet(_|\b)/i) !== null
      ) {
        return 'text';
      }

      const values = _.map(preview, col);
      const uniqueValues = _.uniq(values);
      const uniqueValuesSize = _.size(uniqueValues);
      const lengths = _.map(values, str => str.length);
      const lengthsMean = _.mean(lengths);
      const uniqueLengths = _.uniq(lengths);
      const uniqueLengthsSize = _.size(uniqueLengths);
      const uniqueLengthsMean = _.mean(uniqueLengths);

      const numericValuesSize = _.chain(values)
        // eslint-disable-next-line no-restricted-globals
        .map(n => !isNaN(parseFloat(n)) && isFinite(n))
        .filter()
        .size()
        .value();

      moment.suppressDeprecationWarnings = true;
      const dateValuesSize = _.chain(values)
        .map(date => moment(date).isValid())
        .filter()
        .size()
        .value();

      if (uniqueValuesSize === 2) {
        return 'binary';
      }

      if (dateValuesSize > threshold) {
        return 'date';
      }

      if (lengthsMean > 40) {
        return 'text';
      }

      if (uniqueValuesSize > threshold) {
        return 'id';
      }

      if (uniqueLengthsSize === 1 && (uniqueLengthsMean === 2 || uniqueLengthsMean === 5)) {
        return 'lang';
      }

      if (numericValuesSize > threshold) {
        return 'numeric';
      }

      if (uniqueValuesSize < (cutoff * 0.1)) {
        return 'label';
      }
    }),

  );

  return guesses;
}

routes.get('/', async (req, res) => {
  const files = await db.all(
    'SELECT * FROM files WHERE user_id = $user_id ORDER BY created_at DESC',
    {
      $user_id: req.jwt.sub,
    },
  );

  const promises = await files.map(async (file) => {
    const p = file;
    const projects = await db.all(
      'SELECT * FROM projects WHERE file_id = $file_id',
      {
        $file_id: file.id,
      },
    );
    const jobs = await db.all(
      'SELECT * FROM jobs WHERE file_id_data = $file_id OR file_id_train = $file_id OR file_id_test = $file_id',
      {
        $file_id: file.id,
      },
    );
    p.jobs = jobs;
    p.projects = projects;
    return p;
  });
  Promise.all(promises).then(data => res.json(data));
});


routes.get('/:uuid', async (req, res) => {
  res.json(await getFile(req, res));
});

routes.post('/:uuid/reset', async (req, res) => {
  const result = await db.run(
    'UPDATE files SET is_parsed = 0, parse_config = NULL, corpus_analysis_config = NULL, row_count = NULL,filepath_parsed = NULL  WHERE uuid = $uuid',
    {
      $uuid: req.params.uuid,
    },
  );
  res.json(result.changes === 1);
});

routes.delete('/:uuid', async (req, res) => {
  const result = await db.run(
    'DELETE FROM files WHERE uuid = $uuid AND user_id = $user_id',
    {
      $user_id: req.jwt.sub,
      $uuid: req.params.uuid,
    },
  );
  res.json(result.changes === 1);
});

routes.post(
  '/upload',
  upload.fields([{
    name: 'file', maxCount: 1,
  }]),
  async (req, res) => {
    const file = req.files.file[0];
    const uuid = uuidv1();
    const location = path.join(config.directories.uploads, uuid);

    await fs.moveSync(file.path, location);
    await db.run(
      'INSERT INTO files (user_id, uuid, friendly_name, filename, filepath_original) VALUES ($user_id, $uuid, $friendly_name, $filename, $location)',
      {
        $user_id: req.jwt.sub,
        $uuid: uuid,
        $friendly_name: req.body.name,
        $filename: file.originalname,
        $location: location,
      },
    );

    res.send(uuid);
  },
);


routes.get('/parse/options', (req, res) => {
  res.json({
    columnTypes: config.parse.columnTypes,
    delimiters: config.parse.delimiters,
    quotes: config.parse.quotes,
    escapes: config.parse.escapes,
  });
});

routes.post('/:uuid/analyze', async (req, res) => {
  const body = _.chain(req.body).mapValues(JSON.parse).value();

  const file = await db.get(
    'SELECT * FROM files WHERE uuid = $uuid',
    {
      $uuid: req.params.uuid,
    },
  );

  const promises = [];

  let product = [];
  if (body.smartCsv) {
    product = _.product([''], config.parse.quotes, config.parse.escapes);
  } else {
    product = _.product(
      [body.parseOptions.delimiter],
      [body.parseOptions.quoteChar],
      [body.parseOptions.escapeChar],
    );
  }

  const keys = ['delimiter', 'quoteChar', 'escapeChar'];
  const options = _.map(product, arr => _.zipObject(keys, _.map(arr, a => a)));


  const optionsUsed = _.chain(options)
    .map((option) => {
      const optionMerged = option;
      optionMerged.header = body.header;
      optionMerged.skipEmptyLines = true;
      optionMerged.trimHeader = true;
      optionMerged.preview = config.parse.previewLines;
      return optionMerged;
    })
    .value();

  const fileStream = fs.createReadStream(file.filepath_original, { encoding: 'utf8' });
  optionsUsed.forEach((opt) => {
    const p = Papa.parsePromise(fileStream, opt);
    promises.push(p);
  });


  Promise.all(promises.map(p => p.catch(e => e)))
    .then((results) => {
      const errorCounts = _.chain(results)
        .map(result => result.errors.length)
        .value();
      const minErrorIndex = errorCounts.indexOf(Math.min(...errorCounts));

      const parsed = results[minErrorIndex];

      return { parsed, options: optionsUsed[minErrorIndex] };
    })
    .then(async (data) => {
      const { parsed } = data;
      const parseOptions = data.options;
      fileStream.close();

      res.json({
        analysis: {
          errors: parsed.errors,
          meta: parsed.meta,
          data: parsed.data.slice(0, 250),
          linesRead: config.parse.previewLines,
        },
        guessedHeaders: body.smartHeader
          ? (
            guessHeaders(body.header
              ? parsed.meta.fields
              : _.keys(parsed.data[0]), parsed.data)
          )
          : {},
        options: parseOptions,
      });
    })
    .catch(e => winston.error(e));
});

routes.post('/:uuid/save', async (req, res) => {
  const body = _.chain(req.body).mapValues(JSON.parse).value();

  const file = await db.get(
    'SELECT * FROM files WHERE uuid = $uuid',
    {
      $uuid: req.params.uuid,
    },
  );
  await db.run(
    'UPDATE files SET parse_config = $parse_config, corpus_analysis_config = $corpus_analysis_config WHERE uuid = $uuid',
    {
      $uuid: req.params.uuid,
      $parse_config: JSON.stringify(body.parseOptions),
      $corpus_analysis_config: JSON.stringify(body.config),
    },
  );
  const location = path.join(config.directories.parsed, req.params.uuid);
  fs.ensureFileSync(location);
  const wstream = fs.createWriteStream(location);

  const fileStream = fs.createReadStream(file.filepath_original, { encoding: 'utf8' });
  const errors = [];
  let lines = 0;
  Papa.parse(fileStream, {
    skipEmptyLines: true,
    trimHeader: true,
    delimiter: body.parseOptions.delimiter,
    quoteChar: body.parseOptions.quoteChar,
    escapeChar: body.parseOptions.escapeChar,
    step(results) {
      lines += results.data.length;
      errors.push(...results.errors);
      const csv = Papa.unparse(results, {
        quotes: false,
        quoteChar: "'",
        delimiter: ';',
        newline: '\n',
      });
      wstream.write(`${csv}\n`);
    },
    complete: async () => {
      fileStream.close();
      wstream.end();

      await db.run(
        'UPDATE files SET filepath_parsed = $location, row_count = $row_count, is_parsed = 1 WHERE uuid = $uuid',
        {
          $uuid: req.params.uuid,
          $location: location,
          $row_count: lines - (body.config.header + 1),
        },
      );

      res.json({ errors });
    },
  });
});


module.exports = { routes };
