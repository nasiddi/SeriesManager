const jwt = require('jsonwebtoken');
const config = require('./../../config');

// eslint-disable-next-line consistent-return
function middleware(req, res, next) {
  // check header or url parameters or post parameters for token
  const token = req.body.token || req.query.token || req.headers['x-access-token'] || req.cookies.token;

  // if there is no token
  // return an error
  if (!token) {
    return res
      .status(403)
      .json({
        success: false,
        message: 'No token provided.',
      });
  }
  // decode token
  // verifies secret and checks exp
  try {
    const decoded = jwt.verify(token, config.auth.key);
    req.jwt = decoded;
    next();
  } catch (err) {
    return res
      .status(401)
      .json({ success: false, message: 'Failed to authenticate token.' });
  }
}

module.exports = { middleware };
