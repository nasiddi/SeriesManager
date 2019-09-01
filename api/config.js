const path = require('path');
require('dotenv').config();

module.exports = {
  auth: {
    key: process.env.JWT_KEY || '43c479b5-6c14-44a0-877c-ac0492424496', // change this to invalidate all logins
    lifetime: 86400,
  },
  cleanup: true,
  directories: {
    storage: path.resolve('./storage'),
    backend: path.resolve('../backend'),
  },
  logging: {
    https: true,
  },
  port: process.env.PORT || 8778,
};
