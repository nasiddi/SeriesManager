<template>
  <div>
    <div v-if="hasData">
      <h1>
        {{ project.friendly_name }}
        <span class="float-right">
          <b-button-group>
            <b-dropdown
              v-if="_.size(jobs)"
              variant="outline-primary"
              split
              right
              @click="startNewJob">
              <template slot="button-content">
                <font-awesome-icon icon="play"/> Start a new classification job
              </template>
              <b-dropdown-item
                v-for="job in jobs"
                :key="job.uuid"
                :to="{ name: 'monitor.job', params: { job_uuid: job.uuid } }">
                {{ job.friendly_name }}
              </b-dropdown-item>
            </b-dropdown>
            <b-button
              v-else
              variant="outline-primary"
              @click="startNewJob">
              <font-awesome-icon icon="play"/> Start a new classification job
            </b-button>
          </b-button-group>
        </span>
      </h1>
      <b-alert
        :show="labelValuesCapped"
        variant="info">
        <!-- eslint-disable max-len -->
        <b-form-checkbox
          v-b-tooltip.hover
          v-model="labelValuesCap"
          :value="-1"
          :unchecked-value="labelValuesDefault"
          title="Depending on your data set, your browser may become unresponsive for a brief moment"
          @change="refreshData">
          For every column, only the top 5 values are shown. Show all?
        </b-form-checkbox>
        <!-- eslint-enable max-len -->
      </b-alert>
      <b-alert
        :show="_.size(corpusAnalysis.parse_errors) > 0"
        variant="danger"
      >
        Validation for the selected label type(s) failed
        and the column(s) is (are) ignored for the analysis:<br>
        <ul>
          <li
            v-for="(e, i) in corpusAnalysis.parse_errors"
            :key="i">
            {{ e }}
          </li>
        </ul>
        To see the column anyway, set the type to string label in the parse options.
        <b-button
          variant="warning"
          @click="resetParse()">
          Re-set parse options
        </b-button>
      </b-alert>

      <corpus-stats
        :instances="corpusAnalysis.instances"
        :labels="corpusAnalysis.labelsValuedFlat"
        :row-count="project.file.row_count"
        class="my-5"/>

      <corpus-cloud
        v-if="_.size(corpusAnalysis.labelsValuedFlat) > 0"
        :labels="corpusAnalysis.labelsValuedFlat"
        class="my-5"/>

      <corpus-topic
        v-if="_.size(corpusAnalysis.topic) > 0"
        :topic="corpusAnalysis.topic"
        class="my-5"/>

      <corpus-sentences
        v-if="_.size(corpusAnalysis.sentences) > 0"
        :sentences="corpusAnalysis.sentences"
        class="my-5"/>

      <corpus-tokenizers
        v-if="
          _.size(corpusAnalysis.tokenizer_overlap) > 0 || _.size(corpusAnalysis.tokenizers) > 0
        "
        :tokenizers="corpusAnalysis.tokenizers"
        :tokenizer-overlap="corpusAnalysis.tokenizer_overlap"
        class="my-5"/>

    </div>
    <div v-if="!hasData && !hasPendingRequest">

      <h1>{{ project.friendly_name }}</h1>
      <b-alert
        variant="warning"
        show>
        Unfortunately, this project's corpus has not yet been analyzed.
      </b-alert>
    </div>
  </div>
</template>

<script>
import CorpusCloud from './Cloud';
import CorpusSentences from './Sentences';
import CorpusStats from './Stats';
import CorpusTokenizers from './Tokenizers';
import CorpusTopic from './Topic';

const _ = require('lodash');

export default {
  components: {
    CorpusCloud,
    CorpusSentences,
    CorpusStats,
    CorpusTokenizers,
    CorpusTopic,
  },
  data: () => ({
    project: {},
    corpusAnalysis: {},
    jobs: {},
    hasData: false,
    hasPendingRequest: true,
    timeoutId: null,
    refreshTimeout: 1000,
    lastHash: null,
    refreshingNotif: null,
    labelValuesDefault: 5,
    labelValuesCap: 5,
    labelValuesCapped: false,
  }),
  computed: {},
  mounted() {
    this.refreshData();
    this.refresh();
  },
  destroyed() {
    window.clearTimeout(this.timeoutId);
  },
  metaInfo: {
    title: 'Corpus',
  },
  methods: {
    resetParse() {
      const { uuid } = this.project.file;
      this.$http
        .post(`files/${uuid}/reset`)
        .then(() => {
          this.$snotify.success('Reset file');
        })
        .then(() => {
          this.$router.push({
            name: 'files.parse',
            params: { file_uuid: uuid },
          });
        });
    },
    refresh() {
      if (!this.project || this.project.is_corpus_analyzed !== 1) {
        this.timeoutId = setTimeout(() => {
          if (this.project && this.project.is_corpus_analyzed !== 1 && !this.refreshingNotif) {
            this.refreshingNotif = this.$snotify.info(
              'The corpus analysis is running and the screen will be updated automatically.',
              {
                timeout: 0,
              },
            );
          }
          const url = `projects/${
            this.$router.currentRoute.params.project_uuid
          }/corpus_analysis/check`;
          this.$http.get(url).then((res) => {
            const hash = res.headers.get('X-File-Hash');
            if (hash !== this.lastHash) {
              this.$snotify.info('Updating with latest data from server');
              this.lastHash = hash;
              this.refreshData(() => {
                if (this.project.is_corpus_analyzed === 1) {
                  this.$snotify.success('Corpus analysis is complete');

                  if (this.refreshingNotif) {
                    this.$snotify.remove(this.refreshingNotif.id);
                  }
                }
              });
            }
          });
          this.refresh();
        }, this.refreshTimeout);
      }
    },
    refreshData(cb = () => {}) {
      const notifWait = this.$snotify.info('Hang on, this might take a while', {
        timeout: 0,
      });

      this.$http.get(`projects/${this.$router.currentRoute.params.project_uuid}`).then((res) => {
        this.project = res.body;
      });

      this.$http.get(`projects/${this.$router.currentRoute.params.project_uuid}/jobs`).then((res) => {
        this.jobs = res.body;
      });

      const url = `projects/${this.$router.currentRoute.params.project_uuid}/corpus_analysis`;
      this.$http
        .get(url)
        .then(
          (res) => {
            this.lastHash = res.headers.get('X-File-Hash');
            const body = _.defaults(res.body, {
              instances: {},
              labels: {},
              parse_errors: [],
              sentences: {},
              tokenizer_overlap: {},
              tokenizers: {},
              topic: {},
            });

            body.labelsTyped = this.getLabelsTyped(body.labels);
            body.labelsValued = this.getLabelsValued(body.labelsTyped);
            body.labelsValuedFlat = this.getLabelsValuedFlat(body.labelsValued);

            this.corpusAnalysis = body;

            this.hasData = res.status !== 204;
          },
          () => {
            this.$snotify.error('Failed to load data', { timeout: 0 });
          },
        )
        .then((res) => {
          this.$snotify.remove(notifWait.id);
          this.hasPendingRequest = false;
          cb(res);
        });
    },
    getLabelsTyped(labels) {
      if (_.size(labels) > 0) {
        const step1 = _.chain(labels)
          .mapValues((v, k) => {
            const kArr = _.times(
              _.chain(v)
                .keys()
                .size()
                .value(),
              _.constant(k),
            );
            return _.zipObject(_.keys(v), kArr);
          })
          .values()
          .value();

        const step2 = Object.assign(...step1);

        const step3 = _.chain(step2)
          .mapValues((type, label) => {
            const x = labels[type][label];
            x.type = type;
            return x;
          })
          .value();

        return step3;
      }
      return {};
    },
    getLabelsValued(labels) {
      const result = {};
      if (_.size(labels) > 0) {
        const flattenByKey = (data, key, label) => ({
          char_count: data.char_count[key],
          count: data.count[key],
          tokens: data.tokens[key],
          word_count: data.word_count[key],
          type: data.type,
          value: key,
          label,
          name: `${label}: ${key}`,
        });
        _.chain(labels)
          .each((data, label) => {
            if (_.includes(['none', 'total'], data.type)) {
              result[label] = flattenByKey(data, label, label);
              return;
            }

            if (_.includes(['binary'], data.type)) {
              result[label] = flattenByKey(data, _.keys(data.char_count)[0], label);
              return;
            }

            if (!_.has(result, 'label')) {
              result[label] = { values: {} };
            }

            let capped = _.chain(data.count)
              .map((count, value) => ({ count, value }))
              .orderBy(['count'], ['desc'])
              .value();

            if (this.labelValuesCap > 0) {
              this.labelValuesCapped = _.size(data.count) > this.labelValuesCap;
              capped = _.chain(capped)
                .take(this.labelValuesCap)
                .value();
              if (this.labelValuesCapped) {
                // eslint-disable-next-line
                const t =
                  "For every column, only the top 5 values are shown. If you'd like to show all values, tick the checkbox at the top of the page";
                this.$snotify.info(t);
              }
            }

            _.chain(capped)
              .map(x => x.value)
              .each((v) => {
                result[label].values[v] = flattenByKey(data, v, label);
              })
              .value();
          })
          .value();
      }
      return result;
    },
    getLabelsValuedFlat(labels) {
      const result = {};
      if (_.size(labels) > 0) {
        _.chain(labels)
          .each((data, label) => {
            if (_.has(data, 'values')) {
              _.chain(data.values)
                .each((d) => {
                  result[d.name] = d;
                })
                .value();
            } else {
              result[`${label}`] = data;
            }
          })
          .value();
      }
      return result;
    },
    startNewJob() {
      this.$router.push({
        name: 'job.start_from_file',
        params: {
          file_uuid: this.project.file.uuid,
        },
      });
    },
  },
};
</script>

<style>
/*.wordCloud svg text {
  cursor: pointer;
}*/
</style>
