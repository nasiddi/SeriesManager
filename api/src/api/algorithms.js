const express = require('express');
const db = require('../db/queries');
const config = require('./../../config');

const routes = express.Router();

routes.get('/', async (req, res) => {
  res.send(await db.getAlgorithms());
});

routes.get('/configs', async (req, res) => {
  res.send(await db.getAlgorithmConfigs());
});

routes.get('/tokenizers', async (req, res) => {
  res.json(config.tokenizers);
});

module.exports = { routes };
