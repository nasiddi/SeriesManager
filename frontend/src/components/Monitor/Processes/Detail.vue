<template>
  <div
    :id="`card-proc-${proc.id}`"
    class="mb-3 mt-3"
  >
    <b-card
      :title="proc.algorithm.name"
      :sub-title="proc.algorithm_config.name"
      :border-variant="proc.process_status.bs_variant"
    >
      <div slot="header">
        <b-badge :variant="proc.process_status.bs_variant">{{ proc.process_status.name }}</b-badge>
        <small class="text-muted">
          PID: {{ proc.pid }}
        </small>
        <span class="float-right">
          <span v-if="proc.f1_score_current">
            <small>F1 score:</small>
            <b-badge
              v-if="Math.abs(proc.f1_score_current - proc.f1_score_max) < Number.EPSILON"
              key="f1_badge_only_1"
              :variant="proc.process_status.bs_variant"
            >
              {{ f1ScoreFormatted(proc.f1_score_current) }}
            </b-badge>
            <b-badge
              v-else
              key="f1_badge_only_1"
              :variant="proc.process_status.bs_variant"
            >
              {{ f1ScoreFormatted(proc.f1_score_current) }}.
              ({{ f1ScoreFormatted(proc.f1_score_max) }})
            </b-badge>
          </span>
          <!-- eslint-disable max-len -->
          <b-button
            v-b-popover.hover.auto="`If you want to, you can terminate/kill this process in case it is not generating promising results or execution is taking too long.`"
            v-if="proc.process_status.name === 'running' && !processKillsRequested.includes(proc.id)"
            size="sm"
            variant="danger"
            title="Terminate this process"
            class="cursor-pointer"
            @click="killProcess(proc.id)"
          >&times;</b-button>
          <!-- eslint-enable max-len -->
        </span>
      </div>

      <br>

      <b-row class="mb-3">
        <b-col
          v-if="_.size(proc.confusion_matrix) > 0"
          key="has_confusion_matrix">
          <h4>Confusion Matrix</h4>
          <confusion-matrix
            :data="proc.confusion_matrix"/>
        </b-col>
        <b-col
          v-else
          key="has_confusion_matrix">
          <p>
            <small
              v-if="proc.process_status.type === 'alive'"
              key="no_confusion_matrix_running">
              This process has not yet provided a confusion matrix.
            </small>
            <small
              v-else
              key="no_confusion_matrix_running">
              This process doesn't provide a confusion matrix.
            </small>
          </p>
        </b-col>

        <b-col
          v-if="_.size(proc.classification_report) > 0"
          key="has_classification_report">
          <h4>Classification Report</h4>
          <classification-report
            :data="proc.classification_report"/>
        </b-col>
        <b-col
          v-else
          key="
            has_classification_report">
          <p>
            <small
              v-if="proc.process_status.type === 'alive'"
              key="no_classification_report_running">
              This process has not yet provided a classification report.
            </small>
            <small
              v-else
              key="no_classification_report_running">
              This process doesn't provide a classification report.
            </small>
          </p>
        </b-col>
      </b-row>

      <b-row class="mb-3">
        <b-col
          v-if="processEpochGraphData"
          key="has_epoch_graph"
          lg="6"
          class="chart"
        >
          <h4>F1 Score over Epoch Graph</h4>
          <line-chart
            :chart-data="processEpochGraphData"
            :options="epochGraphOptions"
            :height="200"/>
        </b-col>
        <b-col
          v-else
          key="has_epoch_graph"
          lg="6"
        >
          <p>
            <small
              v-if="proc.process_status.type === 'alive'"
              key="no_epoch_graph_running">
              This process has not yet provided any details about epochs.
            </small>
            <small
              v-else
              key="no_epoch_graph_running">
              This process doesn't provide any details about epochs.
            </small>
          </p>
        </b-col>
      </b-row>

      <br>

      <b-btn
        v-b-toggle="`tail${proc.id}`"
        size="sm"
      >Toggle raw output</b-btn>

      <b-collapse :id="`tail${proc.id}`">
        <pre class="pre-scrollable mt-3">{{ processTail }}</pre>
      </b-collapse>

      <div slot="footer">
        <small class="text-muted">
          <span
            v-if="!proc.ended_at"
            key="footer_proc_running">Started {{ proc.started_at | moment("from") }}</span>
          <span
            v-else
            key="footer_proc_running">
          Ended {{ proc.ended_at | moment("from") }}</span> on {{ proc.hostname }}

          <span v-if="proc.ended_at">| Execution took {{ proc.execution_time_human }}</span>
        </small>
      </div>
    </b-card>
  </div>
</template>

<script>
import Trend from 'vuetrend';
import LineChart from '@/components/Snippets/LineChart';
import ConfusionMatrix from '@/components/Monitor/Processes/ConfusionMatrix';
import ClassificationReport from '@/components/Monitor/Processes/ClassificationReport';

const _ = require('lodash');

export default {
  name: 'ProcessDetail',
  components: {
    Trend,
    LineChart,
    ConfusionMatrix,
    ClassificationReport,
  },
  props: {
    proc: {
      type: Object,
      required: true,
    },
    killProcess: {
      type: Function,
      required: true,
    },
    processKillsRequested: {
      type: Array,
      required: true,
    },
    refreshTimeout: {
      type: Number,
      required: true,
    },
    httpTimeout: {
      type: Number,
      required: true,
    },
  },
  data: () => ({
    processTail: null,
    timeoutId: null,
    epochGraphOptions: {
      legend: {
        display: false,
      },
      maintainAspectRatio: false,
      scales: {
        yAxes: [
          {
            scaleLabel: {
              display: true,
              labelString: 'F1 score',
            },
            ticks: {
              min: 0,
              max: 100,
              callback(value) {
                return `${value}%`;
              },
            },
          },
        ],
        xAxes: [
          {
            scaleLabel: {
              display: true,
              labelString: 'Epoch',
            },
          },
        ],
      },
      tooltips: {
        callbacks: {
          title(a) {
            return `Epoch ${a[0].xLabel}`;
          },
          label(a) {
            return `F1 score: ${a.yLabel > 0 ? `${a.yLabel.toFixed(2)}%` : '0%'}`;
          },
        },
      },
    },
  }),
  computed: {
    processHasEpochs() {
      if (!this.proc.details_json) {
        return false;
      }

      return this.proc.details_json.has_epochs;
    },
    processEpochGraphData() {
      if (!this.processHasEpochs) {
        return false;
      }

      return {
        labels: _.chain(this.proc.details_json.epochs)
          .keys()
          .map(i => parseInt(i, 10))
          .map(i => i + 1)
          .value(),
        datasets: [
          {
            label: 'F1 score',
            // eslint-disable-next-line max-len
            data: _.chain(this.proc.details_json.epochs)
              .map(epoch => epoch.toFixed(6) * 100)
              .value(),
          },
        ],
      };
    },
  },
  mounted() {
    this.refresh();
  },
  destroyed() {
    window.clearTimeout(this.timeoutId);
  },
  methods: {
    refresh() {
      this.refreshProcessTail();
      if (this.proc.process_status.type !== 'dead') {
        // eslint-disable-next-line max-len
        this.timeoutId = window.setTimeout(() => {
          this.refresh();
        }, this.refreshTimeout);
      }
    },
    refreshProcessTail() {
      this.$http
        .get(`processes/tail/${this.proc.job_uuid}/${this.proc.id}`, {
          timeout: this.httpTimeout,
        })
        .then((response) => {
          this.processTail = response.body;
        })
        .catch((err) => {
          // eslint-disable-next-line no-console
          if (err.status > 0) console.error('Problem', err);
        });
    },
  },
};
</script>
