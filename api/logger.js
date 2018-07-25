const winston = require('winston');

const { createLogger, format, transports } = require('winston');

const {
  combine, timestamp, printf, colorize, align,
} = format;

winston.configure({
});

const errorLogger = createLogger({
  format: format.json(),
  transports: [
    new transports.File({
      filename: './error.log',
      level: 'error',
      handleExceptions: true,
      humanReadableUnhandledException: true,
    }),
  ],
});


const prodLogger = createLogger({
  format: format.simple(),
  transports: [new transports.Console({
    level: 'info',
    handleExceptions: true,
    humanReadableUnhandledException: true,
  })],
});

const devLogger = createLogger({
  format: combine(
    colorize(),
    timestamp(),
    align(),
    printf(info => `${info.timestamp} ${info.label ? `[${info.label}]` : ''} [${info.level}] ${info.message}`),
  ),
  transports: [new transports.Console({
    level: 'debug',
    handleExceptions: true,
    humanReadableUnhandledException: true,
  })],
});

winston.add(errorLogger);

if (process.env.NODE_ENV === 'production') {
  winston.add(prodLogger);
}

if (process.env.NODE_ENV === 'development') {
  winston.add(devLogger);
}

if (!process.env.NODE_ENV) {
  winston.add(devLogger);
  winston.warn('NODE_ENV is not set');
}
