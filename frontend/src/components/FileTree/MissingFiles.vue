<template>
  <div v-if="json.length !== 0">
    <div v-if="'files' in json && json.files.length !== 0">
      <b-button
        :pressed.sync="showFilteredFiles"
        variant="outline-primary"
        size="lg"
        block
        class="mt-3"
      >Show Filtered Files</b-button
      >
      <b-alert
        v-for="line in json.files"
        :key="line.key"
        :variant="color(line.e_nr)"
        :show="!filtered(line)"
        dismissible
        class="mt-2 mx-2 mb-0"
        @dismissed="filter(line)"
      >
        <a
          :href="getLink(line)"
          target="_blank"
          class="alert-link">
          <font-awesome-icon icon="download" />
        </a>
        {{ message(line) }}
      </b-alert>
    </div>
    <b-card
      v-else
      :style="{ width: '100%' }"
      :title="json.info"
      class="text-center py-1 mt-4"
    />
  </div>
</template>

<script>
const _ = require('lodash');

export default {
  components: {},
  data: () => ({
    json: {},
    baseLink: 'https://pirateproxy.live/search/',
    endLink: '/1/3/0',
    showFilteredFiles: false,
  }),
  computed: {},
  watch: {},
  created() {
    this.loadData();
  },
  mounted() {},
  methods: {
    filtered(line) {
      if (this.showFilteredFiles) {
        return false;
      }
      return this.json.filter.some((f) => {
        if (
          f.e_nr === line.e_nr
          && f.s_nr === line.s_nr
          && f.series_name === line.series_name
        ) {
          return true;
        }
        return false;
      });
    },
    filter(line) {
      this.$http.post('jobs/filetree/missing/filter', line);
    },
    color(num) {
      if (num === '*') {
        return 'danger';
      }
      return 'warning';
    },
    getLink(line) {
      const seriesName = line.series_name.replace(/[^0-9a-z-A-Z ]/g, '');
      // eslint-disable-next-line no-console
      console.log(seriesName);
      if (line.e_nr === '*') {
        return `${this.baseLink}${seriesName} season ${this.pad2(
          line.s_nr,
        )}${this.endLink}`;
      }
      return `${this.baseLink}${seriesName} s${this.pad2(
        line.s_nr,
      )}e${this.pad2(line.e_nr)}${this.endLink}`;
    },
    message(line) {
      if (line.e_nr === '*') {
        return `${line.series_name} Season ${this.pad2(line.s_nr)}`;
      }
      return `${line.series_name} ${this.pad2(line.s_nr)}x${this.pad2(
        line.e_nr,
      )}`;
    },
    pad2(number) {
      return (number < 10 ? '0' : '') + number;
    },
    unlockShows() {
      this.$snotify.remove(this.notifLock.id);
      this.$http.post('python/unlock').then((res) => {
        this.json = res;
        this.loadData();
      });
    },
    loadData() {
      this.notifLoading = this.$snotify.info('loading', { timeout: 0 });
      this.$http.post('python/filetree/missing').then(
        (res) => {
          const body = _.defaults(res.body, {});
          if (res.body === 'failed') {
            this.$snotify.remove(this.notifLoading.id);
            this.$snotify.error('Python failed', { timeout: 0 });
            return;
          }
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
  },
};
</script>
