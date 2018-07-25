const express = require('express');
const jwt = require('jsonwebtoken');
const moment = require('moment');
const bcrypt = require('bcrypt');
const db = require('sqlite');
const config = require('./../../config');

const routesPublic = express.Router();
const routesAuthed = express.Router();

function createAndSendToken(user, res) {
  const payload = { sub: user.id, name: user.name };
  const expiresIn = config.auth.lifetime;
  const expires = moment().add(expiresIn, 'seconds');
  const token = jwt.sign(payload, config.auth.key, {
    expiresIn, // expires in 24 hours
  });

  res.cookie('token', token, { expires: expires.toDate(), httpOnly: true });
  res.header('X-Access-Token', token);
  res.header('X-Access-Token-Expiry', expires.format());
  res.json({
    success: true,
    message: 'Enjoy your token!',
    token,
  });
}

// eslint-disable-next-line consistent-return
routesPublic.post('/authenticate', async (req, res) => {
  // find the user
  const user = await db.get(
    'SELECT * FROM users WHERE name = $name',
    {
      $name: req.body.name,
    },
  );

  if (!user) {
    return res
      .status(401)
      .json({ success: false, message: 'Authentication failed. User not found.' });
  }
  // check if password matches
  const isPasswordCorrect = await bcrypt.compare(req.body.password || '', user.password);
  if (!isPasswordCorrect) {
    return res
      .status(401)
      .json({ success: false, message: 'Authentication failed. Wrong password.' });
  }
  // if user is found and password is right
  // create a token
  createAndSendToken(user, res);
});

routesAuthed.get('/check', (req, res) => {
  res.json(req.jwt);
});

routesAuthed.post('/refresh', (req, res) => {
  const payload = req.jwt;
  createAndSendToken({ id: payload.sub, name: payload.name }, res);
});

module.exports = { routesAuthed, routesPublic };
