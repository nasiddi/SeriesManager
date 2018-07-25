require('./logger');
require('./src/db/db');
require('./src/api/server');

const winston = require('winston');

process.on('exit', (code) => {
  winston.info(`About to exit with code: ${code}`);
});
process.on('warning', (warning) => {
  winston.warn(JSON.stringify(warning));
});
process.on('uncaughtException', (err) => {
  winston.error(err);
});
process.on('unhandledRejection', (reason, p) => {
  winston.error(reason);
  winston.debug(JSON.stringify(p));
  // eslint-disable-next-line no-console
  console.log(reason);
});

const fs = require('fs-extra');
const _ = require('lodash');
const config = require('./config');

_.chain(config.directories)
  .each((dir) => { fs.ensureDirSync(dir); })
  .value();
