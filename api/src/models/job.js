const fs = require('fs-extra');
const uuidv1 = require('uuid/v1');
const winston = require('winston');
const _ = require('lodash');
const db = require('./../db/queries');
const python = require('./../python/controller');

async function calculateJobBaseline(uuid) {
  await python.baseline(uuid, (code, signal, output) => {
    const data = fs.readJsonSync(output);
    const baseline = data.final_output.score;
    db.updateJobField(uuid, 'f1_score_baseline', baseline);
  });
}

async function create(params) {
  const uuid = uuidv1();
  winston.info(`Starting job ${uuid}`);

  const payload = {
    uuid,
    user_id: params.user_id,
    friendly_name: params.friendly_name,
    start_config: JSON.stringify({
      tokenizers: {
        word: params.wordTokenizer,
        sentence: params.sentenceTokenizer,
      },
    }),
  };

  if (params.fileInputType === 'data') {
    payload.file_uuid_data = params.files.data;
  } else if (params.fileInputType === 'train_test') {
    payload.file_uuid_train = params.files.train;
    payload.file_uuid_test = params.files.test;
  }

  const jobId = await db.newJob(payload);

  python.preprocess(uuid, async (preprocessCode) => {
    if (preprocessCode !== 0) {
      winston.error('preprocess failed');
      await db.setJobErrored(uuid);
      return;
    }
    const algorithmConfigs = _.chain(await db.getAlgorithmConfigs())
      .filter(ac => _.includes(params.algorithmConfigs, ac.id))
      .value();

    calculateJobBaseline(uuid);

    _.each(algorithmConfigs, async (algorithmConfig) => {
      const processId = await db.newProcess({
        algorithm_config_id: algorithmConfig.id,
        uuid,
        job_id: jobId,
      });

      python.classification(processId, () => { });
    });
  });
  return uuid;
}

async function get(uuid) {
  const job = await db.getJob(uuid);
  await db.jobStatusUpdateCheck(uuid); // in case we missed it
  return job;
}

async function getAll() {
  const jobs = await db.getJobs();
  return jobs;
}

module.exports = {
  create,
  get,
  getAll,
};
