
<template>
  <div>
    <b-row>
      <b-col>
        <b-form-input
          v-model="artist"
          type="text"
          placeholder="Artist"
          class="mb-2 mt-3"
          @keyup.native.enter="loadSong()"/>
      </b-col>
      <b-col>
        <b-form-input
          v-model="title"
          type="text"
          placeholder="Title"
          class="mb-2 mt-3"
          @keyup.native.enter="loadSong()"/>
      </b-col>
      <b-col sm="3">
        <b-button
          :style="{width: '100%'}"
          variant="primary"
          class="mb-2 mt-3"
          @click.prevent="loadSong()"
        >Load</b-button>
      </b-col>
      <b-col sm="1">
        <b-form-select
          v-model="columns"
          :options="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
          class="mb-3 mt-3" />
      </b-col>
    </b-row>
    <b-row>
      <b-col sm="3">
        <b-button
          :style="{width: '100%'}"
          variant="primary"
          class="mb-2 mt-3"
          @click.prevent="showAll()"
        >Show All</b-button>
      </b-col>
      <b-col sm="3">
        <b-button
          :style="{width: '100%'}"
          :disabled="(title !== '')"
          variant="primary"
          class="mb-2 mt-3"
          @click.prevent="title = titleHidden"
        >Show Title</b-button>
      </b-col>
    </b-row>
    <b-row
      v-sticky="true"
      sticky-offset="10"
      sticky-side="top">
      <b-col sm="9">
        <b-form-input
          v-model="word"
          type="text"
          class="mb-3 mt-3"
          @input="matchWord"
          @keyup.native.enter="word = ''"/>
      </b-col>
      <b-col>
        <h1
          class="mb-3 mt-2"> {{ found }} / {{ total + ' | ' + duration }} </h1>
      </b-col>
    </b-row>
    <b-row>
      <b-col
        v-for="(a, c) in slicedLyrics"
        :key="a[0] + c"
        class="mx-0 px-1">
        <b-list-group
          class="mx-0 px-0">
          <b-list-group-item
            v-for="(w, i) in a"
            :key="w + i"
            :variant="slicedHighlights[c][i]"
            class="text-center px-1 py-1">
            {{ w }}
          </b-list-group-item>
        </b-list-group>
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
    lyrics: '',
    lyricsLower: [],
    lyricsText: [],
    foundLyrics: [],
    highlight: [],
    word: '',
    columns: 10,
    found: 0,
    total: 0,
    artist: 'queen',
    title: '',
    titleHidden: '',
    start: {},
    stop: false,
    duration: '',
  }),
  computed: {
    slicedLyrics() {
      return this.slice(this.foundLyrics);
    },
    slicedHighlights() {
      return this.slice(this.highlight);
    },
  },
  watch: {},
  created() {
    this.duration = this.hmsFormat(moment.duration(0));
  },
  mounted() {
  },
  methods: {
    slice(arr) {
      const arrays = [];
      const lyr = arr;
      const l = _.map(lyr, _.clone);
      const size = Math.ceil(l.length / (this.columns * 1.0));
      while (l.length > 0) { arrays.push(l.splice(0, size)); }
      // eslint-disable-next-line
      const found = this.found;
      return arrays;
    },
    setDuration() {
      if (this.stop) { return; }
      this.duration = this.hmsFormat(moment.duration(moment(moment()).diff(this.start)));
    },
    hmsFormat(diff) {
      return `${_.padStart(diff.minutes(), 2, 0)}:${_.padStart(diff.seconds(), 2, 0)}`;
    },
    matchWord(w) {
      if (w === '') {
        return;
      }
      let word = w.toLowerCase();
      let index = this.lyricsLower.reduce((a, e, i) => ((e === word) ? a.concat(i) : a), []);
      word = word.replace("'", '');
      index = index.concat(this.lyricsText.reduce((a, e, i) => ((e === word)
        ? a.concat(i) : a), []));
      if (index.length) {
        index = index.filter((item, pos, self) => self.indexOf(item) === pos);
        // eslint-disable-next-line no-return-assign
        index.forEach(i => this.foundLyrics[i] = this.lyrics[i]);
        // eslint-disable-next-line no-return-assign
        index.forEach(i => this.lyricsLower[i] = '');
        // eslint-disable-next-line no-return-assign
        index.forEach(i => this.lyricsText[i] = '');
        this.found += index.length;
        this.highlight = this.highlight.map(item => ((item === 'success') ? '' : item));
        // eslint-disable-next-line no-return-assign
        index.forEach(i => this.highlight[i] = 'success');
        setTimeout(() => {
          this.word = '';
        }, 50);
        if (this.found === this.total) {
          this.showAll();
        }
      }
    },
    showAll() {
      this.stop = true;
      this.foundLyrics = this.lyrics;
      this.title = this.titleHidden;
      this.highlight = this.highlight.map(item => ((item === 'secondary') ? 'danger' : 'success'));
    },
    getWidth() {
      return `${window.innerWidth * 10 / 12}px`;
    },
    prepLyrics() {
      let lyrics = this.lyrics.replace(/[\n\s]/g, ' ');
      while (lyrics.includes('  ')) {
        lyrics = lyrics.replace('  ', ' ');
      }
      lyrics = lyrics.replace(/[^a-zA-Z0-9' ]/g, '');
      this.lyricsLower = lyrics.toLowerCase();
      this.lyricsText = this.lyricsLower.replace(/[']/g, '');
      this.lyricsLower = _.filter(this.lyricsLower.split(' '), sub => sub.length);
      this.lyricsText = _.filter(this.lyricsText.split(' '), sub => sub.length);
      this.lyrics = _.filter(lyrics.split(' '), sub => sub.length);
      this.stableCopy = _.map(this.lyrics, _.clone);
      this.foundLyrics = _.fill(Array(this.lyrics.length), '\u200F');
      this.highlight = _.fill(Array(this.lyrics.length), 'secondary');
      this.total = this.lyrics.length;
    },
    loadSong() {
      this.$http.post('jobs/getlyrics', { artist: this.artist, song: this.title })
        .then(
          (res) => {
            const body = _.defaults(res.body, {
            });
            if (body.lyrics.split(' ').length < 10) {
              this.$snotify.error('Loading Lyrics Failed', { timeout: 2000 });
              this.lyrics = '';
              this.prepLyrics();
              this.word = '';
              this.found = 0;
              return;
            }
            this.lyrics = body.lyrics;
            this.prepLyrics();
            this.titleHidden = body.title;
            this.found = 0;
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
