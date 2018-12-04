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
            :variant="saveColor"
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
        :variant="saveColor"
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
        v-for="s in orderedSeasons"
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
    original: {},
    updated: {},
    saveColor: 'success',
    wrongSymbols: [
      ':',
      '/',
      '{',
      '}',
      '\\',
      '<',
      '>',
      '*',
      '?',
      '$',
      '!',
      '@',
    ],
  }),
  computed: {
    orderedSeasons() {
      return _.orderBy(this.show.seasons, 'key');
    },
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
    error: {
      handler(e) {
        if (this.error.delete) {
          return this.updateSave(true);
        }

        const o = this.original;

        if (this.checkWrongSymbols(e.title)) {
          return this.updateSave(false);
        }
        if (e.name_needed) {
          if (e.title === '') {
            return this.updateSave(false);
          }
        }
        if (e.s_nr === '' || e.e_nr === '') {
          return this.updateSave(false);
        }
        this.updateSave(true);

        if (e.save !== o.save) {
          o.save = e.save;
          return e.save;
        }

        e.save = true;
        o.save = e.save;
        return e.save;
      },
      deep: true,
    },
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
    checkWrongSymbols(val) {
      let found = false;
      this.wrongSymbols.forEach((sym) => {
        if (val.includes(sym)) {
          found = true;
        }
      });
      return found;
    },
    updateSave(primary) {
      if (primary) {
        this.saveColor = 'success';
      } else {
        this.saveColor = 'outline-danger';
        this.error.save = false;
        this.original.save = false;
      }
    },
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

      if (this.errors.length === 0) {
        return;
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
      } else {
        // eslint-disable-next-line prefer-destructuring
        this.error = this.errors[0];
        this.error.save = true;
      }
      this.selected = this.error.series_name;
      this.original = _.cloneDeep(this.error);
      this.updated = _.cloneDeep(this.error);
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
            resolve(true);
          },
          () => {
            this.$snotify.error('Failed to load data', { timeout: 0 });
          },
        );
      });
    },
    save() {
      if (this.saveColor === 'outline-danger') {
        this.$snotify.error('Can\'t Save with Errors', { timeout: 1000 });
        return;
      }
      this.notifErrors = this.$snotify.info('Saving', { timeout: 0 });
      this.$http.post('jobs/filetree/save', { error: this.error, tree: this.json }).then(
        (res) => {
          const body = _.defaults(res.body, {
          });
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
          this.$snotify.remove(this.notifErrors.id);
          this.$snotify.success('Done', { timeout: 500 });
          this.$router.push({
            name: 'reroute',
            params: {
              json: this.json,
              skip: this.errors.indexOf(this.error),
              selected: this.selected,
            },
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
