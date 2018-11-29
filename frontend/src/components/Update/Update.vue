<template>
  <div>
    <div>
      <b-button
        type="update"
        variant="primary"
        size="lg"
        class="mt-3"
        block
        @click.prevent="update"
      >Update</b-button>
      <b-row>
        <b-col>
          <b-button
            :pressed.sync="a"
            :variant="'outline-success'"
            :style="{width: '100%'}"
            size="lg"
            class="mt-3"
          >Airing</b-button>
        </b-col>
        <b-col>
          <b-button
            :pressed.sync="h"
            :variant="'outline-primary'"
            :style="{width: '100%'}"
            size="lg"
            class="mt-3"
          >Hiatus</b-button>
        </b-col>
        <b-col>
          <b-button
            :pressed.sync="e"
            :variant="'outline-warning'"
            :style="{width: '100%'}"
            size="lg"
            class="mt-3"
          >Ended</b-button>
        </b-col>
      </b-row>
    </div>
    <div v-if="json.length !== 0">

      <update-card
        v-for="s in json"
        v-if="(s.status == 'Airing' && a)||(s.status == 'Hiatus' && h)||(s.status == 'Ended' && e)"
        :key="s.series_name_unchanged"
        :id="setRef(s)"
        :s="s"/>
      <b-button
        type="update"
        variant="primary"
        size="lg"
        class="mt-3"
        block
        @click.prevent="update"
      >Update</b-button>
    </div>
  </div>
</template>

<script>
import UpdateCard from './UpdateCard';

const _ = require('lodash');

export default {
  components: {
    UpdateCard,
  },
  data: () => ({
    json: {},
    a: true,
    h: true,
    e: true,
    status_s: [],
    status_option: [
      'Airing',
      'Hiatus',
      'Ended',
    ],
    name_option: [
      { text: 'Name required', value: true },
      { text: 'Name optional', value: false },
    ],
  }),
  created() {
    this.loadData();
  },
  mounted() {
  },
  methods: {
    loadData() {
      this.notifLoading = this.$snotify.info('Loading', { timeout: 0 });
      this.$http.post('jobs/update/prep').then(
        (res) => {
          const body = _.defaults(res.body, {
          });
          if (res.body === 'failed') {
            this.$snotify.remove(this.notifLoading.id);
            this.$snotify.error('Python failed', { timeout: 0 });
            return;
          }
          this.json = body;
          this.$snotify.remove(this.notifLoading.id);
          if ('shows_locked' in body) {
            this.notifLock = this.$snotify.confirm('', 'Shows locked', {
              timeout: 0,
              buttons: [
                { text: 'Unlock', action: () => this.unlockShows(), bold: true },
              ],
            });
          }
        },
        () => {
          this.$snotify.error('Failed to load data', { timeout: 0 });
        },
      );
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
    async update() {
      this.notifLoading = this.$snotify.info('Updating', { timeout: 0 });
      this.$http.post('jobs/update/save', this.json)
        .then(
          (res) => {
            const body = _.defaults(res.body, {
            });
            if (res.body === 'failed') {
              this.$snotify.remove(this.notifLoading.id);
              this.$snotify.error('Python failed', { timeout: 0 });
              return;
            }
            this.$snotify.remove(this.notifLoading.id);
            if ('error' in body) {
              this.$snotify.error(body.error, { timeout: 5000 });
              return;
            }
            this.json = body;
            this.$emit('dates');
          },
          () => {
            this.$snotify.error('Failed to load data', { timeout: 0 });
          },
        );
    },
    setRef(s) {
      const name = s.series_name_unchanged.slice(0, 1);
      // const index = this.json.indexOf(s);
      if (name.toUpperCase() !== name.toLowerCase()) {
        return name.toUpperCase();
      }
      return '#';
    },
  },
};
</script>
