<template>
  <div>
    <h1>
      {{ job ? job.friendly_name : 'Job' }}

      <span class="float-right">
        <b-badge
          v-if="job && job.job_status"
          :variant="job.job_status.bs_variant"
        >{{ job.job_status.name }}</b-badge>
        <b-button-group class="cursor-pointer">
          <b-dropdown
            right
            text="Tools"
            variant="outline-primary"
          >
            <b-dropdown-item :to="{ name: 'evaluate.job', params: { jobId: jobId } }">
              Evaluate this job
            </b-dropdown-item>
            <span v-if="_.size(projects) > 0">
              <b-dropdown-divider/>
              <b-dropdown-header>Corpus Analysis</b-dropdown-header>
              <b-dropdown-item
                v-for="project in projects"
                :key="project.uuid"
                :to="{ name: 'corpus.project', params: { project_uuid: project.uuid} }">
                {{ project.friendly_name }}
              </b-dropdown-item>
            </span>
            <b-dropdown-divider/>
            <div v-if="job && job.job_status.type === 'alive' && processes.length > 0">
              <b-dropdown-item
                variant="danger"
                @click="killAllProcesses()"
              >Kill all processes</b-dropdown-item>
              <div>
                <b-dropdown-header>Kill algorithms</b-dropdown-header>
                <b-dropdown-item
                  v-for="algorithm in algorithms"
                  v-if="algorithmsAlive.includes(algorithm.id)"
                  :key="algorithm.id"
                  @click="killAlgorithm(algorithm.id)"
                >{{ algorithm.name }}</b-dropdown-item>
              </div>
            </div>
          </b-dropdown>
        </b-button-group>
      </span>
    </h1>

    <b-table
      :fields="jobStatusHeaders"
      :items="jobStatus">
      <template
        slot="sentenceTokenizer"
        slot-scope="data">
        <code>{{ data.value }}</code>
      </template>
      <template
        slot="wordTokenizer"
        slot-scope="data">
        <code>{{ data.value }}</code>
      </template>
      <template
        slot="input"
        slot-scope="data">
        <span v-html="data.value"/>
      </template>
    </b-table>

    <div
      v-if="!processes.length"
      class="mt-5 mb-5 d-flex justify-content-center"
    >
      <font-awesome-icon
        icon="circle-notch"
        scale="3"
        spin/>
    </div>

    <h2>
      F1 Scores
      <small v-if="highestScoreCurrently">
        current highscore: {{ highestScoreCurrently }} (max: {{ highestScoreOverall }})
      </small>
    </h2>

    <b-card class="mb-4">
      <process-overview
        v-for="proc in processes"
        :key="proc.id"
        :proc="proc"
        :job="job"
        :hms-format="hmsFormat"/>
    </b-card>

    <div
      v-if="job.classifier_comparison && _.size(processes) > 0">
      <h2>Classifier Comparison</h2>
      <classifier-comparison
        :classifier-comparison="job.classifier_comparison"
        :processes="processes"
        :uuid="job.uuid"
        endpoint="jobs"
      />
    </div>

    <h2>Processes</h2>
    <process-detail
      v-for="proc in processes"
      :key="proc.id"
      :proc="proc"
      :kill-process="killProcess"
      :process-kills-requested="processKillsRequested"
      :refresh-timeout="refreshTimeout"
      :http-timeout="httpTimeout"/>
  </div>
</template>


<script>
import ClassifierComparison from '@/components/Monitor/ClassifierComparison';
import ProcessOverview from '@/components/Monitor/Processes/Overview';
import ProcessDetail from '@/components/Monitor/Processes/Detail';

const moment = require('moment');
const _ = require('lodash');

export default {
  components: { ClassifierComparison, ProcessOverview, ProcessDetail },
  data: () => ({
    refreshTimeout: 1000,
    httpTimeout: 3000,
    jobId: null,
    jobStatusHeaders: {
      httpStatus: { label: 'Monitor status' },
      runTime: { label: 'Run time' },
      sentenceTokenizer: {},
      wordTokenizer: {},
      input: {},
    },
    jobStatus: [
      {
        httpStatus: null,
        runTime: null,
        sentenceTokenizer: null,
        wordTokenizer: null,
        input: null,
        _cellVariants: { httpStatus: 'active' },
      },
    ],
    job: { job_status: {} },
    processes: {},
    projects: [],
    timeoutId: null,
    processKillsRequested: [],
  }),
  computed: {
    highestScoreCurrently() {
      if (!this.processes.length || !this.job.best_process) {
        return null;
      }
      const proc = _.find(this.processes, p => p.id === this.job.best_process);
      if (!proc) {
        return null;
      }
      return this.f1ScoreFormatted(proc.f1_score_current);
    },
    highestScoreOverall() {
      if (!this.processes.length || !this.job.best_process) {
        return null;
      }
      const proc = _.find(this.processes, p => p.id === this.job.best_process);
      if (!proc) {
        return null;
      }
      return this.f1ScoreFormatted(proc.f1_score_max);
    },
    algorithms() {
      return _.chain(this.processes)
        .mapKeys(proc => proc.algorithm.id)
        .mapValues(proc => proc.algorithm)
        .value();
    },
    algorithmsAlive() {
      return _.chain(this.processes)
        .filter(proc => proc.process_status.type === 'alive')
        .mapKeys(proc => proc.algorithm.id)
        .keys()
        .map(id => parseInt(id, 10))
        .value();
    },
  },
  metaInfo() {
    return {
      title: `Monitor for ${this.job ? this.job.friendly_name : this.jobId}`,
    };
  },
  created() {
    this.jobId = this.$route.params.job_uuid;
  },
  mounted() {
    this.refresh();
  },
  destroyed() {
    window.clearTimeout(this.timeoutId);
  },
  methods: {
    refresh() {
      this.refreshJob();
      this.refreshProcesses();
      // eslint-disable-next-line max-len
      this.timeoutId = setTimeout(() => {
        this.refresh();
      }, !this.job || this.job.job_status.type !== 'dead' ? this.refreshTimeout : 10 * 1000);
    },
    hmsFormat(diff) {
      return `${_.padStart(diff.hours(), 2, 0)}:${_.padStart(
        diff.minutes(),
        2,
        0,
      )}:${_.padStart(diff.seconds(), 2, 0)}`;
    },
    refreshJob() {
      this.$http
        .get(`jobs/${this.$router.currentRoute.params.job_uuid}/projects`)
        .then((res) => {
          this.projects = res.body;
        });

      this.$http.get(`jobs/${this.jobId}`, { timeout: this.httpTimeout }).then(
        (response) => {
          this.httpStatus(response);
          this.job = response.body;

          this.jobStatus[0].sentenceTokenizer = this.job.start_config.tokenizers.sentence;
          this.jobStatus[0].wordTokenizer = this.job.start_config.tokenizers.word;

          if (this.job.file_id_data) {
            this.jobStatus[0].input = this.job.file_data.friendly_name;
          }

          if (this.job.file_id_train && this.job.file_id_test) {
            this.jobStatus[0].input = `train: ${
              this.job.file_train.friendly_name
            }<br>test: ${this.job.file_test.friendly_name}`;
          }

          /*eslint-disable*/
          if (this.job.ended_at) {
            const diff = moment.duration(
              moment(this.job.ended_at).diff(this.job.started_at)
            );
            this.jobStatus[0].runTime = `This job ran for ${diff.humanize()} (${this.hmsFormat(
              diff
            )})`;
          } else {
            const diff = moment.duration(
              moment().diff(moment(this.job.started_at))
            );
            this.jobStatus[0].runTime = `This job has been running for ${diff.humanize()} (${this.hmsFormat(
              diff
            )})`;
          }
          /* eslint-enable */

          // eslint-disable-next-line no-underscore-dangle
          this.jobStatus[0]._cellVariants.status = this.job.job_status.bs_variant;
        },
        (response) => {
          this.httpStatus(response);
        },
      );
    },
    refreshProcesses() {
      this.$http
        .get(`jobs/${this.jobId}/processes`, { timeout: this.httpTimeout })
        .then((response) => {
          this.processes = response.body;
        })
        .catch((err) => {
          // eslint-disable-next-line no-console
          if (err.status > 0) console.error('Problem', err);
        });
    },
    httpStatus(response) {
      this.jobStatus[0].httpStatus = `${response.status} ${
        response.statusText
      }`;
      if (response.status >= 400 || !response.status) {
        // eslint-disable-next-line no-underscore-dangle
        this.jobStatus[0]._cellVariants.httpStatus = 'danger';
        if (response.status === 0) {
          this.jobStatus[0].httpStatus = 'Timeout';
        }
      } else if (response.status === 206) {
        // eslint-disable-next-line no-underscore-dangle
        this.jobStatus[0]._cellVariants.httpStatus = 'warning';
      } else {
        // eslint-disable-next-line no-underscore-dangle
        this.jobStatus[0]._cellVariants.httpStatus = 'success';
      }
    },
    killAllProcesses() {
      // eslint-disable-next-line max-len
      _.each(
        _.map(
          _.filter(this.processes, p => p.process_status.type === 'alive'),
          p => p.id,
        ),
        procId => this.killProcess(procId),
      );
    },
    killAlgorithm(aid) {
      _.chain(this.processes)
        .filter(p => p.process_status.type === 'alive')
        .filter(p => p.algorithm.id === aid)
        .each(p => this.killProcess(p.id, p.friendly_name))
        .value();
    },
    killProcess(id, name) {
      this.processKillsRequested.push(id);
      this.$http.get(`processes/kill/${id}`).then(() => {
        this.$snotify.success(`${name} was killed successfully`);
      });
    },
  },
};
</script>
