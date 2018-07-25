const express = require('express');
const processModel = require('./../models/process');

const routes = express.Router();

routes.get('/tail/:uuid/:process', async (req, res) => {
  const { status, contents } = await processModel.tail(req.params.uuid, req.params.process);
  res.status(status);
  res.send(contents);
});

routes.get('/kill/:process', async (req, res) => {
  await processModel.kill(req.params.process);
  res.send();
});


module.exports = { routes };
