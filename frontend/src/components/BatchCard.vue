<template>
  <div
    v-if="f.length !== 0">
    <b-card
      :header="f.location"
      class="mt-3">
      <b-row>
        <b-col
          sm="6"
          class="pl-2 pr-2">
          <b-input
            id="title"
            v-model="f.title"
            class="mt-2"
            placeholder="Title" />
        </b-col>
        <b-col
          sm
          class="pl-2 pr-2">
          <label
            class="sr-only"
            for="series-form">Username</label>
          <b-input-group
            :style="{width: '100%'}"
            left="@"
            class="mt-2">
            <b-input
              id="season"
              v-model.number="f.s_nr"
              type="number"
              placeholder="S" />
            <b-input
              id="episode"
              v-model.number="f.e_nr"
              type="number"
              placeholder="E" />
          </b-input-group>
        </b-col>
        <b-col
          sm
          class="pl-2 pr-2">
          <b-form-select
            v-model="f.episode_option"
            :options="episode_options"
            :style="{width: '100%'}"
            class="mt-2"/>
        </b-col>
        <b-col
          sm
          class="pl-2 pr-2">
          <b-button
            :variant="'primary'"
            :style="{width: '100%'}"
            class="mt-2"
            @click="updateTitle(f)"
          >Update</b-button>
        </b-col>
      </b-row>
      <b-row>
        <b-col
          sm
          class="pl-2 pr-2">
          <b-input
            v-if="f.episode_option !== 'Single'"
            id="checkTitle2"
            v-model="f.title2"
            class="mt-2"
            placeholder="Title 2" />
        </b-col>
      </b-row>
      <b-row>
        <b-col
          sm
          class="pl-2 pr-2">
          <b-input
            v-if="f.episode_option === 'Triple'"
            id="title3"
            v-model="f.title3"
            class="mt-2"
            placeholder="Title 3" />
        </b-col>
      </b-row>
    </b-card>
  </div>
</template>

<script>


const _ = require('lodash');


export default {
  components: {
  },
  props: {
    f: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    episode_options: [
      'Single',
      'Double',
      'Triple',
    ],
    syncColor: 'outline-danger',
    wrongSymbols: [
      ':',
      '/',
      '{',
      '}',
      '(',
      ')',
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
  },
  watch: {
    f: {
      handler(file) {
        if (this.checkWrongSymbols(file.title)) {
          return this.updateSync(false);
        }
        if (this.checkWrongSymbols(file.title2)) {
          return this.updateSync(false);
        }
        if (this.checkWrongSymbols(file.title3)) {
          return this.updateSync(false);
        }
        if (file.t_o.s !== 'Series') {
          if (file.title === '') {
            return this.updateSync(false);
          }
          return this.updateSync(true);
        }
        if (file.series_name === '' || file.series_name === 'Series Name') {
          return this.updateSync(false);
        }
        if ((file.series_name in this.shows && this.shows[file.series_name].name_needed) || (file.new_series && file.name_o.s === 'Name required')) {
          if (file.title === '') {
            return this.updateSync(false);
          }
          if (file.title2 === '' && file.e_o.s !== 'Single') {
            return this.updateSync(false);
          }
          if (file.title3 === '' && file.e_o.s === 'Triple') {
            return this.updateSync(false);
          }
        }
        if (file.s_nr === '' || file.e_nr === '') {
          return this.updateSync(false);
        }
        return this.updateSync(true);
      },
      deep: true,
    },
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
    updateSync(primary) {
      if (primary) {
        if (this.syncColor === 'outline-danger') {
          this.f.sync = true;
        }
        this.syncColor = 'outline-primary';
      } else {
        this.syncColor = 'outline-danger';
        this.f.sync = false;
      }
    },
    async updateTitle(f) {
      return new Promise((resolve) => {
        const file = f;
        if (!(file.new_series)) {
          file.tvdb_id = this.shows[file.series_name].tvdb_id;
        }
        this.$http.post('jobs/tvdb', file)
          .then(
            (res) => {
              const body = _.defaults(res.body, {
              });
              if ('newShows' in body) {
                this.new_show.o = body.newShows;
                const [s] = body.newShows;
                this.f.tvdb_id = s.value;
                return resolve(true);
              }
              if (!('title' in body)) {
                this.$snotify.error(file.series_name, 'Title failed', { timeout: 5000 });
                return resolve(false);
              }
              file.title = body.title;
              if (file.e_o.s !== 'Single') {
                if (!('title2' in body)) {
                  this.$snotify.error(file.series_name, 'Title 2 failed', { timeout: 5000 });
                  return resolve(false);
                }
                file.title2 = body.title2;
              }
              if (file.e_o.s === 'Triple') {
                if (!('title3' in body)) {
                  this.$snotify.error(file.series_name, 'Title 3 failed', { timeout: 5000 });
                  return resolve(false);
                }
                file.title3 = body.title3;
              }
              return resolve(true);
            },
            () => {
              this.$snotify.error('Failed to load data', { timeout: 0 });
              resolve(false);
            },
          );
      });
    },
  },
};
</script>
