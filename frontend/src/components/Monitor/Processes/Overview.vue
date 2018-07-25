<template>
  <b-row
    align-v="center"
    class="my-1"
  >
    <b-col lg="4">
      <b-link
        :href="`#card-proc-${proc.id}`"
        class="link-as-text"
      >
        <font-awesome-icon
          :class="`text-${proc.process_status.bs_variant}`"
          icon="circle"
        />
        {{ proc.friendly_name }}
      </b-link>
    </b-col>
    <b-col lg="1">
      <font-awesome-icon
        v-if="parseInt(proc.id, 10) === job.best_process"
        icon="trophy"
      />
    </b-col>
    <b-col lg="1">
      {{ processDuration }}
    </b-col>
    <b-col lg="2">
      <trend
        v-if="processSparkLine"
        :data="processSparkLine"
        :gradient="['var(--red)', 'var(--orange)', 'var(--yellow)', 'var(--green)']"
        :auto-draw-duration="0"
        :height="30"
        auto-draw
        smooth
      />
    </b-col>
    <b-col>
      <!-- eslint-disable max-len -->
      <b-progress
        v-b-popover.hover.auto="`If a process is below this score, it is not distinguishable from a random algorithm.\nThe baseline for this job is ${f1ScoreFormatted(job.f1_score_baseline)}`"
        v-if="job.f1_score_baseline"
        :min="0"
        :max="1"
        :value="job.f1_score_baseline"
        :variant="job.f1_score_baseline < proc.f1_score_max ? 'dark' : 'danger'"
        height="2px"
        title="Baseline"
      />
      <!-- eslint-enable max-len -->
      <b-progress
        :min="0"
        :max="1"
        height="2rem"
      >
        <!-- eslint-disable max-len -->
        <b-progress-bar
          v-if="Math.abs(proc.f1_score_current - proc.f1_score_max) < Number.EPSILON"
          key="only_1_f1_score"
          :value="proc.process_status.type === 'alive' ? (proc.f1_score_current || 0) : proc.f1_score_max"
          :label="`${f1ScoreFormatted(proc.f1_score_current)}`"
          :animated="proc.process_status.type === 'alive'"
          :variant="proc.process_status.bs_variant"
          show-progress
        />
        <!-- eslint-enable max-len -->
        <!-- eslint-disable max-len -->
        <b-progress-bar
          v-b-popover.hover.auto="`The first value represents the current/final score of this process whereas the value in brackets refers to the highest score this process achieved in any epoch.`"
          v-else
          key="only_1_f1_score"
          :value="proc.process_status.type === 'alive' ? (proc.f1_score_current || 0) : proc.f1_score_max"
          :label="`${f1ScoreFormatted(proc.f1_score_current)} (${f1ScoreFormatted(proc.f1_score_max)})`"
          :animated="proc.process_status.type === 'alive'"
          :variant="proc.process_status.bs_variant"
          show-progress
          title="Two scores"
        />
        <!-- eslint-enable max-len -->

        <!-- eslint-disable max-len -->
        <b-progress-bar
          v-b-popover.hover.auto="`The max score of this process is higher than its current/final score.`"
          v-if="proc.f1_score_current < proc.f1_score_max && proc.process_status.type === 'alive'"
          :value="proc.f1_score_max - proc.f1_score_current"
          :show-progress="false"
          variant="warning"
          title="Difference between current and max score"
        />
        <!-- eslint-enable max-len -->
      </b-progress>
    </b-col>
  </b-row>
</template>

<script>
import Trend from 'vuetrend';

const _ = require('lodash');
const moment = require('moment');

export default {
  name: 'ProcessOverview',
  components: { Trend },
  props: {
    job: {
      type: Object,
      required: true,
    },

    proc: {
      type: Object,
      required: true,
    },

    hmsFormat: {
      type: Function,
      required: true,
    },
  },
  computed: {
    processDuration() {
      const start = moment(this.proc.ended_at ? this.proc.ended_at : moment());
      const duration = moment.duration(start.diff(this.proc.started_at));
      return this.hmsFormat(duration);
    },
    processSparkLine() {
      if (!this.proc.details_json || !this.proc.details_json.has_epochs) {
        return [];
      }
      return _.chain(this.proc.details_json.epochs)
        .map(epoch => epoch * 100)
        .value();
    },
  },
};
</script>
