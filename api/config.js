const path = require('path');
require('dotenv').config();

module.exports = {
  auth: {
    key: process.env.JWT_KEY || '43c479b5-6c14-44a0-877c-ac0492424496', // change this to invalidate all logins
    lifetime: 86400,
  },
  cleanup: true,
  directories: {
    classification: path.resolve('./storage/classification'),
    corpusAnalysis: path.resolve('./storage/corpus_analysis'),
    evaluation: path.resolve('./storage/evaluation'),
    models: path.resolve('./storage/models'),
    output: path.resolve('./storage/output'),
    parsed: path.resolve('./storage/parsed'),
    preprocess: path.resolve('./storage/preprocess'),
    uploads: path.resolve('./storage/uploads'),
    storage: path.resolve('./storage'),
    backend: path.resolve('../backend'),
  },
  logging: {
    http: true,
  },
  port: process.env.PORT || 8778,
  tokenizers: {
    word: ['nltk', 'spacy', 'core'],
    sentence: ['nltk', 'spacy'],
  },
  parse: {
    previewLines: 2048,
    columnTypes: {
      id: 'ID',
      label: 'String label',
      text: 'Text',
      lang: 'Language identifier',
      date: 'Date label',
      numeric: 'Numeric label',
      binary: 'Binary label (0, empty = 0; rest = 1)',
      ignore: '(ignore)',
    },
    delimiters: [
      '',
      ';',
      ',',
      '\t',
    ],
    quotes: [
      '"',
      "'",
      '',
    ],
    escapes: [
      '"',
      "'",
      '',
    ],
  },
};
