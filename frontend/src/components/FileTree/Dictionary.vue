<template>

  <div>
    <div v-if="Object.keys(json).length !== 0">
      <div v-if="json.words.length !== 0">
        <b-button
          variant="success"
          size="lg"
          block
          class="my-3"
          @click.prevent="save"
        >Save Changes</b-button>
        <WordCard
          v-for="e in json.words"
          ref="card"
          :key="e.location"
          :e="e"
          class="mt-2 px-3"/>
        <b-button
          variant="success"
          size="lg"
          block
          class="mt-3"
          @click.prevent="save"
        >Save Changes</b-button>
      </div>
      <b-card
        v-else
        :style="{width: '100%'}"
        :title="json.info"
        class="text-center py-1 mt-4"/>
    </div>
  </div>
</template>

<script>
import WordCard from './WordCard';

const _ = require('lodash');


export default {
  components: {
    WordCard,
  },
  data: () => ({
    json: {},
    wrongSymbols: [
      ':',
      '/',
      '{',
      '}',
      '(',
      ')',
      '\\',
      '<',
      '>',
      '*',
      '?',
      '$',
      '!',
      '@',
    ],
  }),
  computed: {
  },
  watch: {
  },
  created() {
    this.loadData();
  },
  mounted() {
  },
  methods: {
    checkWrongSymbols(val) {
      let found = false;
      this.wrongSymbols.forEach((sym) => {
        if (val.includes(sym)) {
          found = true;
        }
      });
      return found;
    },
    unlockShows() {
      this.$snotify.remove(this.notifLock.id);
      this.$http.post('jobs/unlock')
        .then(
          (res) => {
            this.json = res;
            this.loadData();
          },
        );
    },
    loadData() {
      this.notifLoading = this.$snotify.info('loading', { timeout: 0 });
      this.$http.post('jobs/filetree/dictionary', { series_name: '*' }).then(
        (res) => {
          const body = _.defaults(res.body, {
          });

          if ('shows_locked' in body) {
            this.notifLock = this.$snotify.confirm('', 'Shows locked', {
              timeout: 0,
              buttons: [
                { text: 'Unlock', action: () => this.unlockShows(), bold: true },
              ],
            });
          } else {
            this.json = body;
          }
          this.$snotify.remove(this.notifLoading.id);
        },
        () => {
          this.$snotify.error('Failed to load data', { timeout: 0 });
        },
      );
    },
    save() {
      this.notifLoading = this.$snotify.info('Saving', { timeout: 0 });
      this.$http.post('jobs/filetree/savedictionary', this.json).then(
        (res) => {
          const body = _.defaults(res.body, {
          });

          if ('shows_locked' in body) {
            this.notifLock = this.$snotify.confirm('', 'Shows locked', {
              timeout: 0,
              buttons: [
                { text: 'Unlock', action: () => this.unlockShows(), bold: true },
              ],
            });
          } else {
            this.$snotify.remove(this.notifLoading.id);
            this.loadData();
            this.$snotify.success('Done', { timeout: 500 });
          }
          this.$snotify.remove(this.notifLoading.id);
        },
        () => {
          this.$snotify.error('Failed to save data', { timeout: 0 });
        },
      );
    },
  },
};
</script>
