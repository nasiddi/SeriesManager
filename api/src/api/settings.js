const express = require('express');
const db = require('sqlite');
const _ = require('lodash');

const routes = express.Router();

routes.get('/', async (req, res) => {
  const settings = await db.all('SELECT * FROM settings WHERE user_id = $user_id OR user_id IS NULL ORDER BY user_id', { $user_id: req.jwt.sub });
  if (_.size(settings) === 0) {
    res.json({});
  } else {
    const pickedSettings = _.chain(settings)
      .mapKeys(setting => setting.key)
      .mapValues(setting => ({ value: JSON.parse(setting.value) }))
      .value();

    res.json(pickedSettings);
  }
});

routes.post('/', async (req, res) => {
  const { key, value } = req.body;
  const settingExists = await db.get(
    'SELECT * FROM settings WHERE user_id = $user_id AND key = $key',
    {
      $user_id: req.jwt.sub,
      $key: key,
    },
  );
  if (settingExists) {
    await db.run(
      'UPDATE settings SET value = $value WHERE user_id = $user_id AND key = $key',
      {
        $user_id: req.jwt.sub,
        $key: key,
        $value: JSON.stringify(value),
      },
    );
  } else {
    await db.run(
      'INSERT INTO settings (user_id, key, value) VALUES ($user_id, $key, $value)',
      {
        $user_id: req.jwt.sub,
        $key: key,
        $value: JSON.stringify(value),
      },
    );
  }
  res.json();
});


module.exports = { routes };
