/* eslint-disable vue/attribute-hyphenation */
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
    <div v-if="json.selected in json.backups">
      <b-row
        v-for="(c, i) in json.backups[json.selected].content"
        :key="c.key"
        class="mt-2">
        <b-button
          :class="c.opened ? 'collapsed' : null"
          :aria-expanded="c.opened ? 'true' : 'false'"
          :style="{width: '100%'}"
          :aria-controls="c.key"
          @click="c.opened = !c.opened"
        >{{ c.key }}</b-button>
        <b-collapse
          :id="c.key"
          v-model="c.opened">
          <b-card-group>
            <b-card
              :title="json.selected"
              :style="{width: getWidth()}"
              class="mt-2"
              align="top">
              <vue-json-pretty
                :data="c.data"/>
            </b-card>
            <b-card
              :style="{width: getWidth()}"
              title="Current"
              class="mt-2"
              align="top">
              <vue-json-pretty
                :data="json.current.content[i].data"
                show-length/>
            </b-card>
          </b-card-group>
        </b-collapse>
      </b-row>
    </div>
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
    getWidth() {
      return `${window.innerWidth * 10 / 12 / 2}px`;
    },
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
