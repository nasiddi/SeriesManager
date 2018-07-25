const Promise = require('bluebird');
const db = require('sqlite');
const _ = require('lodash');
const fs = require('fs-extra');
const path = require('path');
const winston = require('winston');

const config = require('./../../config');

fs.ensureDirSync('./db');

Promise.resolve()
  .then(() => db.open('./db/database.sqlite'))
  .then(() => db.migrate()) // { force: 'last' }
  .then(async () => {
    await db.run('PRAGMA foreign_keys = ON');
  })
  .then(async () => {
    const projects = await db.all('SELECT uuid FROM projects');
    const jobs = await db.all('SELECT uuid FROM jobs');
    const files = await db.all('SELECT uuid FROM files');

    const projectUuids = _.chain(projects)
      .map(project => project.uuid)
      .value();
    const jobUuids = _.chain(jobs)
      .map(job => job.uuid)
      .value();
    const fileUuids = _.chain(files)
      .map(file => file.uuid)
      .value();

    const uuids = _.union(projectUuids, jobUuids, fileUuids);
    _.chain([
      config.directories.classification,
      config.directories.corpusAnalysis,
      config.directories.evaluation,
      config.directories.models,
      config.directories.output,
      config.directories.parsed,
      config.directories.preprocess,
      config.directories.uploads,
    ])
      .each((dir) => {
        fs.readdirSync(dir).forEach((file) => {
          if (!uuids.includes(file.substr(0, 36))) {
            const p = path.join(dir, file);
            if (config.cleanup) fs.removeSync(p);
            winston.verbose(`${!config.cleanup ? 'PRETEND ' : ''}removed stale ${p}`);
          }
        });
      })
      .value();
  });

/*
async function setup() {
  const bcrypt = require('bcrypt');
  const salt = await bcrypt.genSalt(10);
  const hashed = await bcrypt.hash('password', salt);
  await db.run('INSERT INTO users (name, password) VALUES (?, ?)', 'user', hashed);
}
setup();
*/

