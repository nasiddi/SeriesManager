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
      <div
        v-for="s in json"
        :key="s.series_name_unchanged"
      >
        <update-card
          v-if="(s.status == 'Airing' && a)||(s.status == 'Hiatus' && h)
          ||(s.status == 'Ended' && e)||(s.status =='none')"
          :key="s.series_name_unchanged"
          :id="setRef(s)"
          :s="s"
          :updated="updated"/>
      </div>
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
    hasNone: false,
    a: true,
    h: true,
    e: true,
    body: {},
    updated: false,
  }),
  watch: {
    json: {
      handler(json) {
        this.findNone(json);
      },
      deep: true,
    },
  },
  created() {
    this.loadData();
  },
  mounted() {
  },
  methods: {
    findNone(json) {
      if (json.some(s => s.status === 'none')) {
        this.a = false;
        this.h = false;
        this.e = false;
      } else if (!this.a && !this.b && !this.c) {
        this.a = true;
        this.h = true;
        this.e = true;
      }
    },
    loadData() {
      this.notifLoading = this.$snotify.info('Loading', { timeout: 0 });
      this.$http.post('python/update/prep').then(
        (res) => {
          const body = _.defaults(res.body, {
          });
          if (res.body === 'failed') {
            this.$snotify.remove(this.notifLoading.id);
            this.$snotify.error('Python failed', { timeout: 0 });
            return;
          }
          this.json = body;
          this.findNone(body);

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
      this.$http.post('python/unlock')
        .then(
          (res) => {
            this.json = res;
            this.loadData();
          },
        );
    },
    async update() {
      this.updated = false;
      this.notifLoading = this.$snotify.info('Updating', { timeout: 0 });
      this.$http.post('python/update/save', this.json)
        .then(
          (res) => {
            const body = _.defaults(res.body, {
            });
            // this.json = {};
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
            this.updated = true;
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
