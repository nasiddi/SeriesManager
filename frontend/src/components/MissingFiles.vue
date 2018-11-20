<template>
  <div v-if="json.length !== 0">
    <b-alert
      v-for="line in json"
      :key="line.key"
      :variant="color(line.e_nr)"
      show
      class="mt-2 mx-2 mb-0">
      {{ message(line) }}
    </b-alert>
  </div>
</template>

<script>

const _ = require('lodash');


export default {
  components: {
  },
  data: () => ({
    json: {},
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
    color(num) {
      if (num === '*') {
        return 'danger';
      }
      return 'warning';
    },
    message(line) {
      if (line.e_nr === '*') {
        return `${line.series_name} Season ${this.pad2(line.s_nr)}`;
      }
      return `${line.series_name} ${this.pad2(line.s_nr)}x${this.pad2(line.e_nr)}`;
    },
    pad2(number) {
      return (number < 10 ? '0' : '') + number;
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
      this.$http.post('jobs/filetree/missing').then(
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
  },
};
</script>
