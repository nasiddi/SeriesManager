const Promise = require('bluebird');
const db = require('sqlite');
const fs = require('fs-extra');

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
