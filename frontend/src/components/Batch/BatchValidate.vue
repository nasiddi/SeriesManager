<template>
  <div>
    <b-row class="mt-3">
      <b-col
        sm
        class="px-2">
        <b-button
          :variant="'primary'"
          :style="{width: '100%'}"
          :disabled="disableSync"
          class="mt-2 mb-3"
          size="lg"
          @click.prevent="sync"
        >Sync</b-button>
      </b-col>
    </b-row>
    <b-row class="mt-2">
      <b-col
        sm
        class="px-2">
        <b-input
          v-model="json.series_name"
          class="mt-2"
          size="lg"
          placeholder="Series Title" />
      </b-col>
    </b-row>
    <b-row class="mt-2">
      <b-col
        sm
        class="px-2">
        <b-input
          v-model.number="json.tvdb_id"
          type="number"
          class="mt-2"
          placeholder="TVDB ID" />
      </b-col>
      <b-col
        sm
        class="px-2">
        <b-input
          v-model="lang"
          class="mt-2"
          placeholder="Language" />
      </b-col>
      <b-col
        sm
        class="px-2">
        <b-input
          v-model="json.premiere"
          class="mt-2"
          placeholder="Premiere" />
      </b-col>
      <b-col
        sm
        class="px-2">
        <b-input
          v-model="json.final"
          class="mt-2"
          placeholder="Final" />
      </b-col>
    </b-row>
    <b-row class="mt-2">
      <b-col
        sm
        class="px-2">
        <b-form-select
          v-model="json.status"
          :options="status_option"
          class="mt-2"/>
      </b-col>
      <b-col
        sm
        class="px-2">
        <b-form-select
          v-model="json.anime"
          :options="anime_option"
          class="mt-2"/>
      </b-col>
      <b-col
        sm
        class="px-2">
        <b-form-select
          v-model="json.name_needed"
          :options="name_option"
          class="mt-2"/>
      </b-col>
      <b-col
        sm
        class="px-2">
        <b-button
          :variant="'primary'"
          :style="{width: '100%'}"
          class="mt-2 mb-3"
          @click="update"
        >Update Meta</b-button>
      </b-col>
    </b-row>
    <b-row>
      <b-col
        sm
        class="px-2">
        <b-form-select
          v-if="showSelect.length != 0"
          v-model="json.tvdb_id"
          :options="showSelect"
          class="mt-2"/>
      </b-col>
    </b-row>
    <b-row>
      <b-card-group
        sm
        deck
        class="px-2 mt-2 py-0">
        <b-card
          v-for="o in overview"
          :key="o.s_nr"
          :header="'Season ' + String(o.s_nr)">
          <b-row>
            <b-col
              v-for="e in o"
              :key="e.eNR"
              align-h="start">
              <b-alert
                v-if="typeof e !== 'number'"
                :variant="e.variant"
                :style="{width: '60px'}"
                show
                class=""
              >{{ addZero(e.eNr) }}</b-alert>
            </b-col>
          </b-row>
        </b-card>
      </b-card-group>
    </b-row>

    <b-row>
      <b-col
        sm
        class="px-2">
        <BatchCard
          v-for="f in json.files"
          :key="f.location"
          :f="f"
          :tvdb_id="String(json.tvdb_id)"
          :name_needed="json.name_needed"/>
      </b-col>
    </b-row>
    <b-row class="mt-3">
      <b-col
        sm
        class="px-2">
        <b-button
          :variant="'primary'"
          :style="{width: '100%'}"
          :disabled="disableSync"
          class="mt-2 mb-3"
          size="lg"
          @click.prevent="sync"
        >Sync</b-button>
      </b-col>
    </b-row>
  </div>

</template>

<script>
import BatchCard from './BatchCard';

const _ = require('lodash');

export default {
  components: {
    BatchCard,
  },
  data: () => ({
    json: {},
    overview: {},
    showSelect: [],
    tvdbEpisodes: [],
    eps: {},
    lang: 'en',
    status_option: [
      'Airing',
      'Hiatus',
      'Ended',
    ],
    disableSync: false,
    name_option: [
      { text: 'Name required', value: true },
      { text: 'Name optional', value: false },
    ],
    anime_option: [
      { text: 'Anime: Yes', value: true },
      { text: 'Anime: No', value: false },
    ],
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
  watch: {
    json: {
      handler(j) {
        this.overview = {};
        this.disableSync = false;
        if (this.json.status === ''
        || this.json.series_name === '') {
          this.disableSync = true;
        }
        const currentDate = new Date();
        this.tvdbEpisodes.forEach((e) => {
          if (e.airedSeason === 0) { return; }
          const airDate = new Date(e.firstAired);
          if (airDate - currentDate > 0) { return; }
          if (!(e.airedSeason in this.overview)) {
            this.overview[e.airedSeason] = { s_nr: e.airedSeason };
          }
          this.overview[e.airedSeason][e.airedEpisodeNumber] = { eNr: e.airedEpisodeNumber, variant: 'secondary' };
        });
        j.files.forEach((f) => {
          if (f.s_nr === '' || f.e_nr === '') { return; }
          if (!(f.s_nr in this.overview)) {
            this.overview[f.s_nr] = { s_nr: f.s_nr };
          }
          if (f.e_nr in this.overview[f.s_nr] && this.overview[f.s_nr][f.e_nr].variant !== 'secondary') {
            if (!f.sub && !this.overview[f.s_nr][f.e_nr].sub) {
              this.overview[f.s_nr][f.e_nr].variant = 'warning';
              this.disableSync = true;
              return;
            }
          } else {
            this.overview[f.s_nr][f.e_nr] = { eNr: f.e_nr, variant: 'primary' };
          }
          if (f.episode_option !== 'Single') {
            if (f.e_nr + 1 in this.overview[f.s_nr] && this.overview[f.s_nr][f.e_nr + 1].variant !== 'secondary') {
              if (!f.sub && !this.overview[f.s_nr][f.e_nr + 1].sub) {
                this.overview[f.s_nr][f.e_nr + 1].variant = 'warning';
                this.disableSync = true;
                return;
              }
            } else {
              this.overview[f.s_nr][f.e_nr + 1] = { eNr: f.e_nr + 1, variant: 'primary' };
            }
          }
          if (f.episode_option === 'Triple') {
            if (f.e_nr + 2 in this.overview[f.s_nr] && this.overview[f.s_nr][f.e_nr + 2].variant !== 'secondary') {
              if (!f.sub && !this.overview[f.s_nr][f.e_nr + 2].sub) {
                this.overview[f.s_nr][f.e_nr + 2].variant = 'warning';
                this.disableSync = true;
                return;
              }
            } else {
              this.overview[f.s_nr][f.e_nr + 2] = { eNr: f.e_nr + 2, variant: 'primary' };
            }
          }
          this.overview[f.s_nr][f.e_nr].variant = this.checkTitle(f.title);
          if (f.episode_option !== 'Single') {
            this.overview[f.s_nr][f.e_nr + 1].variant = this.checkTitle(f.title2);
          }
          if (f.episode_option === 'Triple') {
            this.overview[f.s_nr][f.e_nr + 2].variant = this.checkTitle(f.title3);
          }
        });
      },
      deep: true,
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
      this.$http.post('python/unlock')
        .then(
          (res) => {
            this.json = res;
            this.loadData();
          },
        );
    },
    loadData() {
      this.$http.post('python/batch/match', this.$route.params).then(
        (res) => {
          const body = _.defaults(res.body, {
          });
          if (res.body === 'failed') {
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
        },
        () => {
          this.$snotify.error('Failed to load data', { timeout: 0 });
        },
      );
    },
    async sync() {
      this.$router.push({
        name: 'batch.report',
        params: this.json,
      });
    },
    checkTitle(title) {
      let color = 'success';
      this.wrongSymbols.forEach((sym) => {
        if (title.includes(sym)) {
          color = 'danger';
          this.disableSync = true;
        }
      });
      if (title === '') {
        if (this.json.name_needed) {
          color = 'info';
          this.disableSync = true;
        } else {
          color = 'primary';
        }
      }
      return color;
    },
    addZero(eNr) {
      if (eNr < 10) {
        return `0${eNr}`;
      }
      return `${eNr}`;
    },
    episodeExists(s, e) {
      return Object.keys(s).some(k => e === s[k].eNr);
    },
    isValidDateWithDash(dateString) {
      const regEx = /^\d{4}-\d{2}-\d{2}$/;
      if (!dateString.match(regEx)) return false;
      const d = new Date(dateString);
      if (!d.getTime() && d.getTime() !== 0) return false;
      return d.toISOString().slice(0, 10) === dateString;
    },
    isValidDateNoDash(dateString) {
      const regEx = /^\d{8}$/;
      if (!dateString.match(regEx)) return '';
      const val = `${dateString.slice(0, 4)}-${dateString.slice(4, 6)}-${dateString.slice(6, 8)}`;
      const d = new Date(val);
      if (!d.getTime() && d.getTime() !== 0) return '';
      if (d.toISOString().slice(0, 10) === val) {
        return val;
      }
      return '';
    },
    update() {
      if (this.json.tvdb_id === '') {
        const reqBody = {
          series_name: this.json.series_name,
          tvdb_id: this.json.tvdb_id,
          new_series: true,
        };
        this.$http.post('jobs/tvdb', reqBody)
          .then(
            (res) => {
              const body = _.defaults(res.body, {
              });
              if ('newShows' in body) {
                this.showSelect = body.newShows;
                const [s] = body.newShows;
                this.json.tvdb_id = s.value;
              }
            },
            () => {
              this.$snotify.error('Failed to load data', { timeout: 0 });
            },
          );
      } else {
        this.$http.post('jobs/tvdb', { tvdb_id: this.json.tvdb_id, batch: true })
          .then(
            (res) => {
              this.tvdbEpisodes = _.defaults(res.body, {
              });
              this.json.files.forEach((f) => {
                const file = f;
                let episode2 = null;
                let episode3 = null;
                if (f.s_nr === '' || f.e_nr === '') { return; }
                const episode = this.tvdbEpisodes.find(obj => obj.airedSeason === f.s_nr
                  && obj.airedEpisodeNumber === f.e_nr);
                episode2 = this.tvdbEpisodes.find(obj => obj.airedSeason === f.s_nr
                  && obj.airedEpisodeNumber === f.e_nr + 1);
                episode3 = this.tvdbEpisodes.find(obj => obj.airedSeason === f.s_nr
                  && obj.airedEpisodeNumber === f.e_nr + 2);
                if (episode != null && 'episodeName' in episode) {
                  file.title = episode.episodeName;
                }
                if (episode2 != null && 'episodeName' in episode2) {
                  file.title2 = episode2.episodeName;
                }
                if (episode3 != null && 'episodeName' in episode3) {
                  file.title3 = episode3.episodeName;
                }
              });
            },
            () => {
              this.$snotify.error('Failed to load data', { timeout: 0 });
            },
          );
        if (this.isValidDateWithDash(this.json.premiere)) {
          if (this.json.status !== 'Ended') {
            if (this.json.final === '') {
              return;
            }
            this.json.final = '';
            return;
          }
        }
        if (this.isValidDateWithDash(this.json.final)) { return; }
        if (this.json.tvdb_id === '') {
          return;
        }
        this.$http.post('jobs/tvdb/dates', { tvdb_id: this.json.tvdb_id })
          .then(
            (res) => {
              const body = _.defaults(res.body, {
              });
              if ('premiere' in body) {
                this.json.premiere = body.premiere;
              }
              if (this.json.status === 'Ended' && 'final' in body) {
                this.json.final = body.final;
              }
              if (this.json.status !== 'Ended') {
                this.json.final = '';
              }
            },
            () => {
              this.$snotify.error('Failed to load data', { timeout: 0 });
            },
          );
      }
    },
  },
};
</script>
