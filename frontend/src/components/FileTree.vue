<template>
  <div>
    <div v-if="!_.isEmpty(error)">
      <ErrorCard
        ref="card"
        :key="error.old_location"
        :e="error"
        class="mt-4"/>
      <b-row class="mt-3 mx-1">
        <b-col
          class="px-2 mb-1">
          <b-button
            :style="{width: '100%'}"
            :disabled="backDisable"
            variant="outline-primary"
            @click="move(-1)">
            <font-awesome-icon icon="angle-left"/>
          </b-button>
        </b-col>
        <b-col
          class="px-2 mb-1">
          <b-button
            :style="{width: '100%'}"
            variant="success"
            @click.prevent="save">
            Save
          </b-button>
        </b-col>
        <b-col
          class="px-2 mb-1">
          <b-button
            :style="{width: '100%'}"
            :disabled="forwardDisable"
            variant="outline-primary"
            @click="move(1)">
            <font-awesome-icon icon="angle-right"/>
          </b-button>
        </b-col>
      </b-row>
    </div>
    <b-card
      v-if="_.isEmpty(error) && _.isEmpty(json) && 'info' in json "
      :style="{width: '100%'}"
      :title="json.info"
      class="text-center mt-4"/>
    <div v-if="json.length !== 0 && 'shows' in json">
      <b-button
        v-if="_.isEmpty(error)"
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
            :options="shows"
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
  </div>
</template>

<script>

import FileCard from './FileCard';
import ErrorCard from './ErrorCard';


const _ = require('lodash');


export default {
  components: {
    FileCard,
    ErrorCard,
  },
  data: () => ({
    json: {},
    errors: [],
    show: {},
    error: {},
    selected: null,
    errorlist: {},
    shows: [],
    forwardDisable: false,
    backDisable: false,
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
          const current = this.errors.indexOf(this.error);
          if (current + 1 >= this.errors.length) {
            this.forwardDisable = true;
          } else {
            this.forwardDisable = false;
          }
          if (current === 0) {
            this.backDisable = true;
          } else {
            this.backDisable = false;
          }
        });
      },
    },
  },
  created() {
    this.displayError();
  },
  mounted() {
  },
  methods: {
    async displayError() {
      const promises = [];
      let name = '*';
      if (!_.isEmpty(this.error)) {
        name = this.error.series_name;
      }
      if ('json' in this.$route.params) {
        this.json = this.$route.params.json;
      } else {
        promises.push(this.loadData(name));
        await Promise.all(promises);
      }
      this.errors = this.json.errors;
      this.shows = Object.values(this.json.shows).map(s => s.series_name).sort();

      if ('selected' in this.$route.params) {
        this.selected = this.$route.params.selected;
      } else {
        // eslint-disable-next-line prefer-destructuring
        this.selected = Object.values(this.json.shows)
          .map(s => s.series_name).sort()[0];
      }

      if ('skip' in this.$route.params) {
        // eslint-disable-next-line prefer-destructuring
        const skip = this.$route.params.skip;
        if (skip >= this.errors.length) {
          // eslint-disable-next-line prefer-destructuring
          this.error = this.errors[this.errors.length - 1];
          this.error.save = true;
        } else {
          this.error = this.errors[skip];
          this.error.save = true;
        }
      } else if (this.errors.length > 0) {
        // eslint-disable-next-line prefer-destructuring
        this.error = this.errors[0];
        this.error.save = true;
      }
    },
    async move(dir) {
      const current = this.errors.indexOf(this.error);
      this.error.save = false;
      this.error = this.errors[current + dir];
      this.error.save = true;
      this.selected = this.error.series_name;
    },
    sleep(milliseconds) {
      return new Promise(resolve => setTimeout(resolve, milliseconds));
    },
    unlockShows() {
      this.$snotify.remove(this.notifLock.id);
      this.$http.post('jobs/unlock')
        .then(
          (res) => {
            this.json = res;
            this.loadData('*');
          },
        );
    },
    async loadData(name) {
      return new Promise((resolve) => {
        this.notifLoading = this.$snotify.info('loading FileTree', { timeout: 0 });
        this.$http.post('jobs/filetree', { series_name: name }).then(
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
            resolve(true);
          },
          () => {
            this.$snotify.error('Failed to load data', { timeout: 0 });
          },
        );
      });
    },
    save() {
      this.notifErrors = this.$snotify.info('Saving', { timeout: 0 });
      this.$http.post('jobs/filetree/save', this.error).then(
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
          this.$snotify.remove(this.notifErrors.id);
          this.$snotify.success('Done', { timeout: 500 });
          this.$router.push({
            name: 'reroute',
            params: { json: this.json, skip: this.errors.indexOf(this.error) },
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
