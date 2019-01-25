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
          :options="['word', 'no_lows', 'title', 'ordered_title',
                     'ordered_no_lows', 'hidden_title', 'hidden_no_lows', 'sxe_no_lows']"
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
      <b-col v-if="level.includes('sxe') && !_.isEmpty(episodes) && !_.isEmpty(episodes[0])">
        <h1
          class="mb-3 mt-2"> {{ pad2(episodes[positions[curPos][0]][positions[curPos][1]].s_nr)
          }}x{{ pad2(episodes[positions[curPos][0]][positions[curPos][1]].e_nr) }} </h1>
      </b-col>
      <b-col sm="6">
        <b-form-input
          v-model="word"
          type="text"
          class="mb-3 mt-3"
          @keyup.native.enter="word = ''"/>
      </b-col>
      <b-col>
        <h1
          class="mb-3 mt-2"> {{ found }} / {{ total + ' | ' + duration }} </h1>
      </b-col>
    </b-row>
    <b-row v-if="!level.includes('sxe') || stop ">
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
    curPos: [0, 0],
    positions: [],
  }),
  computed: {
  },
  watch: {
    word: {
      handler(w) {
        if (w === '') {
          return;
        }
        const word = w.toLowerCase();
        if (this.level.includes('ordered')) {
          this.checkNext(word);
          return;
        }
        if (this.level.includes('hidden')) {
          this.findRandom(word);
          return;
        }
        if (this.level.includes('sxe')) {
          this.findRandom(word);
          return;
        }
        let found = false;

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
          this.shows = _.sortBy(body.shows);
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
    findRandom(w) {
      if (this.positions.length <= this.curPos) {
        return;
      }
      const current = this.episodes[this.positions[this.curPos][0]][this.positions[this.curPos][1]];
      if (current.title_list.includes(w) || current.title_list.includes(w.replace(/[^a-zA-Z0-9' ]/g, ''))) {
        current.highlight = 'info';
        this.word = '';
        this.found += 1;
        this.curPos += 1;
        if (this.found === this.total) {
          this.showAll();
        } else {
          const next = this.episodes[
            this.positions[this.curPos][0]][this.positions[this.curPos][1]];
          next.highlight = 'warning';
        }
      }
    },
    getPositions() {
      this.episodes.forEach((s, iS) => {
        s.forEach((e, iE) => {
          this.positions.push([iS, iE]);
        });
      });
      this.positions = _.shuffle(this.positions);
    },
    checkNext(w) {
      const current = this.episodes[this.curPos[0]][this.curPos[1]];
      if (current.title_list.includes(w) || current.title_list.includes(w.replace(/[^a-zA-Z0-9' ]/g, ''))) {
        current.title = current.solution;
        current.highlight = 'info';
        this.word = '';
        this.found += 1;
        if (this.episodes[this.curPos[0]].length > this.curPos[1] + 1) {
          this.curPos[1] += 1;
        } else if (this.episodes.length > this.curPos[0] + 1) {
          this.curPos[0] += 1;
          this.curPos[1] = 0;
        }
        if (this.found === this.total) {
          this.showAll();
        } else {
          const next = this.episodes[this.curPos[0]][this.curPos[1]];
          next.highlight = 'warning';
        }
      }
    },
    showAll() {
      this.stop = true;
      setTimeout(() => {
        this.episodes.forEach((s) => {
          s.forEach((e) => {
            e.title = e.solution;
            if (e.highlight !== 'info') {
              e.highlight = 'danger';
            } else {
              e.highlight = 'success';
            }
          });
        });
      }, 50);
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
      // eslint-disable-next-line prefer-destructuring
      let levelType = this.level;
      if (levelType.includes('title')) {
        levelType = 'title';
      } else if (levelType.includes('no_lows')) {
        levelType = 'no_lows';
      }
      this.$http.post('python/titlequiz', { series_name: this.show, level: levelType })
        .then(
          (res) => {
            const body = _.defaults(res.body, {
            });
            this.episodes = body.episodes;
            this.found = 0;
            this.total = body.total;
            this.stop = false;
            if (this.level.includes('ordered')) {
              this.curPos = [0, 0];
              this.episodes[this.curPos[0]][this.curPos[1]].highlight = 'warning';
            }
            if (this.level.includes('hidden') || this.level.includes('sxe')) {
              this.getPositions();
              this.curPos = 0;
              this.episodes[this.positions[0][0]][this.positions[0][1]].highlight = 'warning';
            }
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
