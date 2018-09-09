<template>
  <div v-if="json.length !== 0 && 'shows' in json">
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
          <b-row
            v-for="e in s.episodes"
            :key="e.key"
            class="mt-2 px-3">
            <b-card
              :style="{width: '100%'}"
              no-body
              class="px-2 py-2 mt-2">
              <b-row>
                <b-col>
                  <b-button
                    :class="e.opened ? 'collapsed' : null"
                    :aria-expanded="e.opened ? 'true' : 'false'"
                    :style="{width: '100%'}"
                    aria-controls="'e' + e.key.toString()"
                    variant="outline-primary"
                    @click="e.opened = !e.opened"
                  >{{ e.key }}</b-button>
                </b-col>
                <b-col
                  sm="11"
                  class="mt-2">
                  {{ (e.path) ? e.location : e.file_name }}
                </b-col>
              </b-row>
            </b-card>
          </b-row>
        </b-collapse>
      </b-col>
    </b-row>
  </div>
</template>

<script>

const _ = require('lodash');

export default {
  components: {
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
        // eslint-disable-next-line prefer-destructuring
        this.show = Object.values(this.json.shows).filter(s => s.series_name === this.selected)[0];
      },
    },
  },
  created() {
    this.loadData();
  },
  mounted() {
  },
  methods: {
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
          }
          // eslint-disable-next-line prefer-destructuring
          this.selected = Object.values(body.shows)
            .map(s => s.series_name).sort()[0];
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
