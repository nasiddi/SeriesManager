<template>
  <div v-if="!_.isEmpty(json)">
    <b-row class="mt-4">
      <b-col sm="2">
        <b-button
          :style="{width: '100%'}"
          variant="success"
          class="mt-2 mb-3"
          @click="backup"
        >BackUp</b-button>
      </b-col>
      <b-col>
        <b-form-select
          v-model="json.selected"
          :options="json.backups"
          :selected="json.selected"
          class="mt-2 mb-3"/>
      </b-col>
      <b-col sm="2">
        <b-button
          :style="{width: '100%'}"
          variant="warning"
          class="mt-2 mb-3"
          @click="restore"
        >Restore BackUp</b-button>
      </b-col>
    </b-row>
    <b-row>
      <vue-json-pretty
        :path="'res'"
        :data="getFiles()"
        @click="handleClick"/>
    </b-row>
  </div>
</template>

<script>
import VueJsonPretty from 'vue-json-pretty';

const _ = require('lodash');

export default {
  components: {
    VueJsonPretty,
  },
  data: () => ({
    json: {},
  }),
  computed: {
    getFiles() {
      return this.json.backups.filter(obj => obj.value === this.selected);
    },
  },
  created() {
    this.loadData();
  },
  mounted() {
  },
  methods: {
    loadData() {
      this.notifLoading = this.$snotify.info('Loading', { timeout: 0 });
      this.$http.post('python/getbackup').then(
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
      this.$http.post('python/unlock')
        .then(
          (res) => {
            this.json = res;
            this.loadData();
          },
        );
    },
    async backup() {
      this.notifLoading = this.$snotify.info('Creating BackUp', { timeout: 0 });
      this.$http.post('python/backup')
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
            }
          },
          () => {
            this.$snotify.error('Failed to load data', { timeout: 0 });
          },
        );
    },
    async restore() {
      this.notifLoading = this.$snotify.info('Restore from BackUp', { timeout: 0 });
      this.$http.post('python/restorebackup', { date: this.json.selected })
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
            }
          },
          () => {
            this.$snotify.error('Failed to load data', { timeout: 0 });
          },
        );
    },
  },
};
</script>
