<template>
  <div v-if="Object.keys(json).length !== 0">
    <b-button
      type="sync"
      variant="primary"
      size="lg"
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
    <FileCard
      v-for="file in json.files"
      ref="card"
      :key="file.location"
      :file="file"
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
import FileCard from './FileCard';

const _ = require('lodash');


export default {
  components: {
    FileCard,
  },
  data: () => ({
    json: {},
    series_selected: 'Series Name',
    series_options: [],
  }),
  computed: {
  },
  mounted() {
    this.notifLoading = this.$snotify.info('Loading', {
      timeout: 0,
    });
    this.$http
      .get('jobs/names')
      .then(
        (res) => {
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
    async checkData(file) {
      const f = file;
      let sync = false;
      if (file.title === '') {
        sync = false;
      } else {
        sync = true;
      }
      if (sync && file.sync) {
        return;
      }
      f.sync = false;
    },
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
        this.checkData(file);
        if (file.series_name !== 'Series Name' && file.tvdb !== 0) {
          promises.push(this.$refs.card.updateTitle(file));
        }
      });
      await Promise.all(promises);
      this.$snotify.remove(this.notifLoading.id);
      this.notifLoading = null;
    },
    async sync() {
      this.$http.post('jobs/sync/start', this.json.files);
    },
  },
};
</script>
