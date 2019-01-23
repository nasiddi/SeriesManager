/* eslint-disable no-unreachable */
<template>
  <div v-if="json.length !== 0 && 'total' in json">
    <b-row >
      <b-col >
        <b-button
          variant="primary"
          class="mt-3"
          block
          @click.prevent="result"
        >Show Result</b-button>
      </b-col>
      <b-col >
        <b-button
          variant="primary"
          class="mt-3"
          block
          @click.prevent="reset"
        >Reset</b-button>
      </b-col>
      <b-col>
        <b-form-select
          v-model="level"
          :options="['all', 'single']"
          class="mt-3"/>
      </b-col>
    </b-row>
    <b-row class="text-center mt-3">
      <b-col class="text-center">
        <h1
          v-if="trueCounter > 0 || level === 'single'"
          class="mb-3 mt-2 text-center"> {{ trueCounter }} / {{ shows.length }} </h1>
      </b-col>
    </b-row>
    <div v-if="level === 'all'">
      <stats-quiz-card
        v-for="show in shows"
        :key="show.series_name"
        :show="show"
        :selector="seriesNames"
        class="mt-3"/>
    </div>
    <div v-if="level === 'single'">
      <b-row >
        <b-col >
          <b-button
            :disabled="currentIndex === 0"
            variant="primary"
            class="mt-3"
            block
            @click.prevent="back"
          >Back</b-button>
        </b-col>
        <b-col >
          <b-button
            variant="primary"
            class="mt-3"
            block
            @click.prevent="submit"
          >Submit</b-button>
        </b-col>
        <b-col >
          <b-button
            :disabled="currentIndex >= shows.length"
            variant="primary"
            class="mt-3"
            block
            @click.prevent="next"
          >Next</b-button>
        </b-col>
      </b-row>
      <b-row >
        <b-col >
          <stats-quiz-card
            :key="shows[currentIndex].series_name"
            :show="shows[currentIndex]"
            :selector="seriesNames"
            class="mt-3"/>
        </b-col>
      </b-row>
    </div>
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
    trueCounter: 0,
    level: 'single',
    currentIndex: 0,
  }),
  computed: {
  },
  watch: {
  },
  created() {
    this.loadData();
    this.$root.$on('colors', this.setColors);
    this.$root.$on('submit', this.submit);
    this.$root.$on('back', this.back);
    this.$root.$on('next', this.next);
  },
  mounted() {
    window.addEventListener('keyup', (event) => {
      if (event.keyCode === 32) {
        this.$root.$emit('submit');
      } else if (event.keyCode === 37) {
        this.$root.$emit('back');
      } else if (event.keyCode === 39) {
        this.$root.$emit('next');
      }
    });
  },
  methods: {
    submit() {
      const s = this.shows[this.currentIndex];
      this.$set(s, 'result', true);
      if (s.series_name === s.selected) {
        this.trueCounter += 1;
        this.$set(s, 'color', 'success');
      } else {
        this.$set(s, 'color', 'danger');
      }
    },
    back() {
      if (this.currentIndex > 0) {
        this.currentIndex -= 1;
      }
    },
    next() {
      if (this.currentIndex < this.shows.length) {
        this.currentIndex += 1;
      }
    },
    reset() {
      this.loadData();
    },
    result() {
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
          if (!(n.value === '')) {
            if (selected.includes(n.value)) {
              if (!n.text.includes('SELECTED')) {
                this.$set(n, 'text', `${n.text} | SELECTED`);
              }
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
            this.seriesNames = [{ value: '', text: '' }].concat(this.seriesNames);
            this.trueCounter = 0;
            this.currentIndex = 0;
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
