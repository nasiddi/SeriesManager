<template>
  <div v-if="Object.keys(json).length !== 0">
    <b-button
      type="sync"
      variant="primary"
      size="lg"
      class="mt-3"
      block
      @click.prevent="sync"
    >Sync</b-button>
    <b-button
      type="sync"
      variant="success"
      size="lg"
      block
      class="mt-3"
      @click.prevent="updateAll"
    >Update All</b-button>
    <SyncCard
      v-for="file in json.files"
      ref="card"
      :key="file.location"
      :f="file"
      :shows="json.shows"
      :subs="json.subs"/>

    <b-button
      type="sync"
      variant="success"
      size="lg"
      block
      class="mt-3"
      @click.prevent="updateAll"
    >Update All</b-button>
    <b-button
      type="sync"
      variant="primary"
      size="lg"
      block
      class="mt-3"
      @click.prevent="sync"
    >Sync</b-button>
  </div>
</template>

<script>
import SyncCard from './SyncCard';

const _ = require('lodash');


export default {
  components: {
    SyncCard,
  },
  data: () => ({
    json: {},
    series_selected: 'Series Name',
    series_options: [],
  }),
  computed: {
  },
  created() {
    this.notifLoading = this.$snotify.info('Loading', {
      timeout: 0,
    });
    this.$http
      .get('jobs/sync/prep')
      .then(
        (res) => {
          if (res.body === 'failed') {
            this.$snotify.remove(this.notifLoading.id);
            this.$snotify.error('Python failed', { timeout: 0 });
            return;
          }
          const body = _.defaults(res.body, {
          });
          this.json = body;
          this.series_options = this.json.shows;

          this.updateAll();
        },
        () => {
          this.$snotify.error('Failed to load data', { timeout: 0 });
        },
      );
  },
  methods: {
    setColor(file) {
      if (file.override) {
        return 'outline-primary';
      }
      return 'outline-danger';
    },
    async updateAll() {
      if (this.notifLoading == null) {
        this.notifLoading = this.$snotify.info('Loading', {
          timeout: 0,
        });
      }
      const promises = [];
      this.json.files.forEach((file) => {
        if (file.series_name !== 'Series Name' && file.tvdb !== 0) {
          promises.push(this.updateTitle(file));
        }
      });
      await Promise.all(promises);
      this.$snotify.remove(this.notifLoading.id);
      this.notifLoading = null;
    },
    async updateTitle(f) {
      return new Promise((resolve) => {
        const file = f;
        if (!(file.new_series)) {
          file.tvdb_id = this.json.shows[file.series_name].tvdb_id;
        }
        this.$http.post('jobs/tvdb', file)
          .then(
            (res) => {
              const body = _.defaults(res.body, {
              });
              file.title = body.title;
              if (file.e_o.s !== 'Single') {
                file.title2 = body.title2;
              }
              if (file.e_o.s === 'Triple') {
                file.title3 = body.title3;
              }
              resolve(true);
            },
            () => {
              this.$snotify.error('Failed to load data', { timeout: 0 });
              resolve(false);
            },
          );
      });
    },
    async sync() {
      this.$router.push({
        name: 'sync.report',
        params: this.json.files,
      });
    },
  },
};
</script>
