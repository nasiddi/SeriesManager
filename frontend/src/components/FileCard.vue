<template>
  <div
    v-if="f.length !== 0">
    <b-card
      :header="f.location"
      class="mt-3">
      <b-row>
        <b-col
          sm
          class="pl-2 pr-2">
          <label
            class="sr-only"
            for="fc">Name</label>
          <b-form-select
            v-if="'t_o' in f"
            v-model="f.t_o.s"
            :options="f.t_o.o"
            :style="{width: '100%'}"
            class="mt-2"
            selected="Series"/>
        </b-col>
        <b-col
          sm="4"
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
          <b-button
            :pressed.sync="f.override"
            :variant="'outline-primary'"
            :style="{width: '100%'}"
            class="mt-2"
          >Override</b-button>
        </b-col>
        <b-col
          sm
          class="pl-2 pr-2">
          <b-button
            :pressed.sync="f.show_subs"
            :variant="'outline-primary'"
            :disabled="subs.length === 0"
            :style="{width: '100%'}"
            class="mt-2"
          >Subtitles</b-button>
        </b-col>
        <b-col
          sm
          class="pl-2 pr-2">
          <b-button
            :pressed.sync="f.sync"
            :variant="syncColor"
            :style="{width: '100%'}"
            class="mt-2"
          >Sync</b-button>
        </b-col>
        <b-col
          sm
          class="pl-2 pr-2">
          <b-button
            :pressed.sync="f.delete"
            :variant="outline-warning"
            :style="{width: '100%'}"
            class="mt-2"
          >Sync</b-button>
        </b-col>
      </b-row>
      <b-row
        v-if="'t_o' in f && f.t_o.s === 'Series'">
        <b-col
          sm="6"
          class="pl-2 pr-2">
          <b-input
            v-if="f.new_series === true"
            id="series-new_series"
            v-model="f.series_name"
            :style="{width: '100%'}"
            class="mt-2"
            placeholder="Series Name"/>
          <b-form-select
            v-if="f.new_series === false"
            id="series-selector"
            v-model="f.series_name"
            :options="Object.keys(shows)"
            :style="{width: '100%'}"
            selected="f.series_name"
            class="mt-2"/>
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
            v-if="'e_o' in f"
            v-model="f.e_o.s"
            :options="f.e_o.o"
            :style="{width: '100%'}"
            selected="Single"
            class="mt-2"/>
        </b-col>
        <b-col
          sm
          class="pl-2 pr-2">
          <b-form-select
            v-if="'status_o' in f"
            v-model="f.status_o.s"
            :options="f.status_o.o"
            :style="{width: '100%'}"
            selected="Airing"
            class="mt-2"/>
        </b-col>
        <b-col
          sm
          class="pl-2 pr-2">
          <b-button
            :pressed.sync="f.new_series"
            :variant="'outline-primary'"
            :style="{width: '100%'}"
            class="mt-2"
          >New Series</b-button>
        </b-col>
        <b-col
          sm
          class="pl-2 pr-2">
          <b-button
            v-if="'t_o' in f && f.t_o.s === 'Series'"
            :variant="'success'"
            :style="{width: '100%'}"
            class="mt-2"
            @click="updateTitle(f)"
          >Update</b-button>
        </b-col>
      </b-row>
      <b-row
        v-if="'t_o' in f && f.t_o.s ==='Series' && f.new_series === true">
        <b-col
          sm
          class="pl-2 pr-2">
          <b-form-select
            v-if="'anime_o' in f"
            v-model="f.anime_o.s"
            :options="f.anime_o.o"
            selected="Anime: No"
            class="mt-2"/>
        </b-col>
        <b-col
          sm
          class="pl-2 pr-2">
          <b-form-select
            v-if="'name_o' in f"
            v-model="f.name_o.s"
            :options="f.name_o.o"
            selected="Anime: Name required"
            class="mt-2"/>
        </b-col>
        <b-col
          sm
          class="pl-2 pr-2">
          <b-input
            id="tvdb"
            v-model="f.tvdb_id"
            class="mt-2"
            placeholder="TVDB ID"/>
        </b-col>
      </b-row>
      <b-row>
        <b-col
          sm
          class="pl-2 pr-2">
          <b-form-select
            v-if="new_show.o.length != 0"
            v-model="f.tvdb_id"
            :options="new_show.o"
            :selected="f.tvdb_id"
            class="mt-2"/>
        </b-col>
      </b-row>
      <b-row>
        <b-col
          sm
          class="pl-2 pr-2">
          <b-input
            v-if="'t_o' in f && 'e_o' in f && f.e_o.s !== 'Single' && f.t_o.s === 'Series'"
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
            v-if="'t_o' in f && 'e_o' in f && f.e_o.s === 'Triple' && f.t_o.s === 'Series'"
            id="title3"
            v-model="f.title3"
            class="mt-2"
            placeholder="Title 3" />
        </b-col>
      </b-row>
      <b-row>
        <b-col
          sm
          class="pl-2 pr-2">
          <b-form-checkbox-group
            v-if="f.show_subs === true"
            v-model="f.subs"
            :options="subs"
            :style="{width: '100%'}"
            buttons
            button-variant="outline-primary"
            class="mt-2"
            stacked/>
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
    shows: {
      type: Object,
      required: true,
    },
    subs: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    syncColor: 'outline-danger',
    new_show: { o: [], s: 0 },
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
