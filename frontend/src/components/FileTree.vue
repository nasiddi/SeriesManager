<template>
  <div v-if="json.length !== 0 && 'shows' in json">
    <b-button
      variant="success"
      size="lg"
      block
      class="mt-3"
      @click.prevent="save"
    >Save Changes</b-button>
    <b-row class="mt-3">
      <b-col>
        <b-form-select
          v-model="selected"
          :options="Object.values(json.shows).map(s => s.series_name).sort()"
          :style="{width: '100%'}"
          selected="Series"/>
      </b-col>
    </b-row>
    <b-row
      v-for="s in show.seasons"
      :key="s.key"
      class="mt-3">
      <b-col>
        <b-button
          :class="s.opened ? 'collapsed' : null"
          :aria-expanded="s.opened ? 'true' : 'false'"
          :style="{width: '100%'}"
          aria-controls="'s' + s.key.toString()"
          @click="s.opened = !s.opened"
        >Season {{ s.key }}</b-button>
        <b-collapse
          :id="'s' + s.key.toString()"
          v-model="s.opened">
          <FileCard
            v-for="e in s.episodes"
            ref="card"
            :key="e.e_enr"
            :e="e"
            class="mt-2 px-3"/>
        </b-collapse>
      </b-col>
    </b-row>
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
    show: {},
    selected: null,
  }),
  computed: {
    opened(sea) {
      const season = sea;
      if (season.opened === true) {
        season.opened = false;
        return false;
      }
      season.opened = true;
      return true;
    },
  },
  watch: {
    selected: {
      handler() {
        this.show = { loader: { seasons: [], series_name: 'loader' } };
        this.sleep(10).then(() => {
          // eslint-disable-next-line prefer-destructuring
          this.show = Object.values(this.json.shows)
            .filter(s => s.series_name === this.selected)[0];
        });
      },
    },
  },
  created() {
    this.loadData();
  },
  mounted() {
  },
  methods: {
    sleep(milliseconds) {
      return new Promise(resolve => setTimeout(resolve, milliseconds));
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
      this.$http.post('jobs/filetree', { series_name: '*' }).then(
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

            if ('selected' in this.$route.params) {
              this.selected = this.$route.params.selected;
            } else {
            // eslint-disable-next-line prefer-destructuring
              this.selected = Object.values(body.shows)
                .map(s => s.series_name).sort()[0];
            }
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
      this.$http.post('jobs/filetree/save', this.json).then(
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
          this.$snotify.success('Done', { timeout: 500 });
          this.$router.push({
            name: 'reroute',
            params: { selected: this.selected },
          });
        },
        () => {
          this.$snotify.error('Failed to save data', { timeout: 0 });
        },
      );
    },
  },
};
</script>
