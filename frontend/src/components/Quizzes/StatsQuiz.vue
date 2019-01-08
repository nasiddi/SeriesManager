/* eslint-disable no-unreachable */
<template>
  <div v-if="json.length !== 0 && 'total' in json">
    <b-row >
      <b-col >
        <b-button
          variant="primary"
          size="lg"
          class="mt-3"
          block
          @click.prevent="result"
        >Show Result</b-button>
      </b-col>
      <b-col >
        <b-button
          variant="primary"
          size="lg"
          class="mt-3"
          block
          @click.prevent="reset"
        >Reset</b-button>
    </b-col></b-row>
    <b-row class="text-center mt-3">
      <b-col class="text-center">
        <h1
          v-if="trueCounter > -1"
          class="mb-3 mt-2 text-center"> {{ trueCounter }} / {{ shows.length }} </h1>
      </b-col>
    </b-row>
    <stats-quiz-card
      v-for="show in shows"
      :key="show.series_name"
      :show="show"
      :selector="seriesNames"
      class="mt-3"/>
  </div>
</template>

<script>
import StatsQuizCard from './StatsQuizCard';


const _ = require('lodash');


export default {
  components: {
    StatsQuizCard,
  },
  data: () => ({
    json: {},
    shows: [],
    seriesNames: [],
    trueCounter: -1,
  }),
  computed: {
  },
  watch: {
  },
  created() {
    this.loadData();
    this.$root.$on('colors', this.setColors);
  },
  methods: {
    reset() {
      this.loadData();
    },
    result() {
      this.trueCounter = 0;
      this.seriesNames.forEach((n) => {
        this.$set(n, 'text', `${n.value}`);
      });
      this.shows.forEach((s) => {
        this.$set(s, 'result', true);
        if (s.series_name === s.selected) {
          this.trueCounter += 1;
          this.$set(s, 'color', 'success');
        } else {
          this.$set(s, 'color', 'danger');
        }
      });
    },
    async setColors() {
      setTimeout(() => {
        const selected = _.map(this.shows, 'selected');
        const duplicates = _.filter(selected, (val, i, e) => _.includes(e, val, i + 1));
        this.seriesNames.forEach((n) => {
          if (!(n.value == null)) {
            if (selected.includes(n.value) && !n.text.includes('SELECTED')) {
              this.$set(n, 'text', `${n.text} | SELECTED`);
            } else if (n.text.includes('SELECTED')) {
              this.$set(n, 'text', n.value);
            }
          }
        });
        this.shows.forEach((s) => {
          if (s.selected === '') {
            this.$set(s, 'color', 'warning');
          } else if (duplicates.includes(s.selected)) {
            this.$set(s, 'color', 'danger');
          } else {
            this.$set(s, 'color', 'info');
          }
        });
      }, 50);
    },
    loadData() {
      this.notifLoading = this.$snotify.info('Loading', { timeout: 0 });
      this.$http
        .post('python/stats')
        .then(
          (res) => {
            const body = _.defaults(res.body, {
            });
            if (res.body === 'failed') {
              this.$snotify.remove(this.notifLoading.id);
              this.$snotify.error('Python failed', { timeout: 0 });
              return;
            }

            this.json = body;
            this.shows = _.shuffle(body.shows);


            const names = _.sortBy(_.map(body.shows, 'series_name'));
            this.seriesNames = names.map(n => ({ text: n, value: n }));
            this.seriesNames = [{ value: null, text: '' }].concat(this.seriesNames);
            this.trueCounter = -1;

            this.setColors();
            this.$snotify.remove(this.notifLoading.id);
          },
          () => {
            this.$snotify.error('Failed to load data', { timeout: 0 });
          },
        );
    },
  },
};
</script>
