<template>
  <div v-if="!_.isEmpty(shows)">
    <b-row>
      <b-col>
        <b-form-select
          v-model="show"
          :options="shows"
          class="mb-2 mt-3"/>
      </b-col>
      <b-col sm="3">
        <b-form-select
          v-model="level"
          :options="['word', 'no_lows', 'title']"
          class="mb-2 mt-3" />
      </b-col>
      <b-col sm="3">
        <b-button
          :style="{width: '100%'}"
          :disabled="level === '' || show === ''"
          variant="primary"
          class="mb-2 mt-3"
          @click.prevent="loadEpisodes()"
        >Load</b-button>
      </b-col>
      <b-col sm="3">
        <b-button
          :style="{width: '100%'}"
          variant="primary"
          class="mb-2 mt-3"
          @click.prevent="showAll()"
        >Show All</b-button>
      </b-col>
    </b-row>
    <b-row
      v-sticky="true"
      sticky-offset="10"
      sticky-side="top">
      <b-col sm="8">
        <b-form-input
          v-model="word"
          type="text"
          class="mb-3 mt-3"
          @change="match"
          @keyup.native.enter="word = ''"/>
      </b-col>
      <b-col>
        <h1
          class="mb-3 mt-2"> {{ found }} / {{ total + ' | ' + duration }} </h1>
      </b-col>
    </b-row>
    <b-row>
      <b-col
        v-for="(a, c) in episodes"
        :key="c"
        class="mx-0 px-1">
        <b-card
          header-tag="header"
          no-body>
          <h6
            slot="header"
            class="text-center mb-0">S{{ a[0].s_nr }}</h6>
          <b-list-group
            flush
            class="mx-0 px-0">
            <b-list-group-item
              v-for="w in a"
              :key="w.e_nr"
              :variant="w.highlight"
              class="px-1 py-1">
              {{ pad2(w.e_nr) + ' ' + w.title }}
            </b-list-group-item>
          </b-list-group>
        </b-card>
      </b-col>
    </b-row>


  </div>
</template>

<script>

const _ = require('lodash');
const moment = require('moment');

export default {
  components: {
  },
  data: () => ({
    shows: {},
    episodes: {},
    show: '',
    level: '',
    highlight: [],
    word: '',
    found: 0,
    total: 0,
    start: {},
    stop: false,
    duration: '',
  }),
  computed: {
  },
  watch: {
    word: {
      handler(w) {
        if (w === '') {
          return;
        }
        let found = false;
        const word = w.toLowerCase();
        this.episodes.forEach((s) => {
          s.forEach((e) => {
            if (e.title) {
              if (e.highlight === 'success') {
                e.highlight = 'info';
              }
            } else if (e.title_list.includes(word) || e.title_list.includes(word.replace(/[^a-zA-Z0-9' ]/g, ''))) {
              e.title = e.solution;
              e.highlight = 'success';
              found = true;
              this.found += 1;
            }
          });
        });
        if (found) {
          this.word = '';
        }
        if (this.found === this.total) {
          this.showAll();
        }
      },
      deep: true,
    },
  },
  created() {
    this.$http.post('python/titlequizprep')
      .then(
        (res) => {
          const body = _.defaults(res.body, {
          });
          this.shows = body.shows;
          this.duration = this.hmsFormat(moment.duration(0));
        },
        () => {
          this.$snotify.error('Failed to load data', { timeout: 0 });
        },
      );
  },
  mounted() {
  },
  methods: {
    match(w) {
      if (w === '') {
        return;
      }
      let found = false;
      const word = w.toLowerCase();
      this.episodes.forEach((s) => {
        s.forEach((e) => {
          if (e.title) {
            if (e.highlight === 'success') {
              e.highlight = 'secondary';
            }
          } else if (e.title_list.includes(word) || e.title_list.includes(word.replace(/[^a-zA-Z0-9' ]/g, ''))) {
            e.title = e.solution;
            e.highlight = 'success';
            found = true;
            this.found += 1;
          }
        });
      });
      if (found) {
        setTimeout(() => {
          this.word = '';
        }, 50);
      }
    },
    showAll() {
      this.stop = true;
      this.episodes.forEach((s) => {
        s.forEach((e) => {
          if (!e.title) {
            e.highlight = 'danger';
            e.title = e.solution;
          } else {
            e.highlight = 'success';
          }
        });
      });
    },
    setDuration() {
      if (this.stop) { return; }
      this.duration = this.hmsFormat(moment.duration(moment(moment()).diff(this.start)));
    },
    hmsFormat(diff) {
      return `${_.padStart(diff.minutes(), 2, 0)}:${_.padStart(diff.seconds(), 2, 0)}`;
    },
    pad2(number) {
      return (number < 10 ? '0' : '') + number;
    },
    loadEpisodes() {
      this.$http.post('python/titlequiz', { series_name: this.show, level: this.level })
        .then(
          (res) => {
            const body = _.defaults(res.body, {
            });
            this.episodes = body.episodes;
            this.found = 0;
            this.total = body.total;
            this.stop = false;
            this.start = moment(moment());
            setInterval(this.setDuration, 1000);
          },
          () => {
            this.$snotify.error('Failed to load data', { timeout: 0 });
          },
        );
    },
  },
};
</script>
