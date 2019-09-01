var fs = require('fs');
var http = require('http');
var https = require('https');
var privateKey  = fs.readFileSync('/etc/letsencrypt/live/api.skyship.space/privkey.pem', 'utf8');
var certificate = fs.readFileSync('/etc/letsencrypt/live/api.skyship.space/cert.pem', 'utf8');
var credentials = {key: privateKey, cert: certificate};

const winston = require('winston');
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const morgan = require('morgan');
const compression = require('compression');

const config = require('./../../config');

const auth = require('./auth');
const authMiddleware = require('./auth-middleware');
const jobs = require('./jobs');
const python = require('./python');
const settings = require('./settings');

const { port } = config;

const app = express();

winston.stream = {
  write(message) {
    winston.verbose(message.trim());
  },
};

if (config.logging.http) {
  app.use(morgan('dev', { stream: winston.stream }));
}
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json({ limit: '100mb' }));
app.use(cookieParser());
app.use(compression());

app.use(
  cors({
    exposedHeaders: ['X-Access-Token', 'X-Access-Token-Expiry', 'X-File-Hash'].join(','),
  }),
);

// https://github.com/scotch-io/node-token-authentication

// Add routes below

app.get('/', (req, res) => {
  res.send('Hello world');
});

app.use('/auth', auth.routesPublic);

//
// ABOVE: public API
//

app.use(authMiddleware.middleware);

//
// BELOW: authed API
//

app.use('/auth', auth.routesAuthed);
app.use('/jobs', jobs.routes);
app.use('/python', python.routes);
app.use('/settings', settings.routes);

app.get('/dashboard', (req, res) => {
  res.send(req.jwt.name);
});
// Add routes above

// eslint-disable-next-line no-unused-vars
app.use((err, req, res, next) => {
  winston.error(err);
  res.status(500);
  res.send('Something broke!');
});

var httpServer = http.createServer(app);
var httpsServer = https.createServer(credentials, app);

httpServer.listen(port);
httpsServer.listen(8443);
winston.info(`https://localhost:${port}`);
