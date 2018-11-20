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
  .then(() => db.migrate()); // { force: 'last' }

/*
async function setup() {
  const bcrypt = require('bcrypt');
  const salt = await bcrypt.genSalt(10);
  const hashed = await bcrypt.hash('password', salt);
  await db.run('INSERT INTO users (name, password) VALUES (?, ?)', 'user', hashed);
}
setup();
*/
