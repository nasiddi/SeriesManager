<template>
  <div>
    <b-button
      type="start"
      variant="primary"
      size="lg"
      class="mt-3"
      block
      @click.prevent="start"
    >Start</b-button>
    <b-form-group>
      <b-row class="mt-3">
        <b-col
          sm
          class="px-2">
          <b-input
            v-model="series_name"
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
            v-model.number="tvdb_id"
            type="number"
            class="mt-2"
            placeholder="TVDB ID" />
        </b-col>
        <b-col
          sm
          class="px-2">
          <b-input
            v-model="premiere"
            class="mt-2"
            placeholder="Premiere" />
        </b-col>
        <b-col
          sm
          class="px-2">
          <b-input
            v-model="final"
            class="mt-2"
            placeholder="Final" />
        </b-col>
        <b-col
          sm
          class="px-2">
          <b-form-select
            v-model="status"
            :options="status_option"
            class="mt-2"/>
        </b-col>
        <b-col
          sm
          class="px-2">
          <b-form-select
            v-model="anime"
            :options="anime_option"
            class="mt-2"/>
        </b-col>
        <b-col
          sm
          class="px-2">
          <b-form-select
            v-model="name_needed"
            :options="name_option"
            class="mt-2"/>
        </b-col>
        <b-col
          sm
          class="px-2">
          <b-button
            :variant="'primary'"
            :style="{width: '100%'}"
            class="mt-2"
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
            v-model="tvdb_id"
            :options="showSelect"
            class="mt-2"/>
        </b-col>
      </b-row>
      <b-row class="mb-4">
        <b-col
          v-for="r in reg"
          :key="r.text"
          sm
          class="px-2">
          <b-input
            v-model.lazy="r.value"
            class="mt-2"
            placeholder="Regex" />
        </b-col>
        <b-col
          sm
          class="px-2">
          <b-button
            :variant="'primary'"
            :style="{width: '100%'}"
            class="mt-2"
            @click="updateRegex"
          >Update Regex</b-button>
        </b-col>
      </b-row>
      <b-row
        v-for="u in units"
        :key="u.text">
        <b-col
          sm="10"
          class="px-2">
          <b-card
            v-if="u.value.length === 0"
            no-body
            class="px-2 py-2 mt-2">
            <text-highlight
              :queries="matches">
              {{ u.text }}
            </text-highlight>
          </b-card>
          <b-button
            v-b-toggle="u.text"
            v-if="u.value.length > 0"
            :variant="'outline-secondary'"
            :style="{width: '100%'}"
            class="mt-2"
          >{{ u.text }}</b-button>
          <b-collapse
            :id="u.text">
            <b-card
              no-body
              class="px-2 py-2 mt-2">
              <text-highlight
                v-for="f in u.value"
                :key="f"
                :queries="matches">
                {{ f }}
              </text-highlight>
            </b-card>
          </b-collapse>
        </b-col>
        <b-col
          sm
          class="px-2">
          <b-button
            :pressed.sync="u.select"
            :variant="'outline-primary'"
            :style="{width: '100%'}"
            class="mt-2"
          >Select</b-button>

        </b-col>
      </b-row>
    </b-form-group>
  </div>
</template>

<script>
import TextHighlight from 'vue-text-highlight';

const _ = require('lodash');

export default {
  components: {
    TextHighlight,
  },
  data: () => ({
    series_name: '',
    tvdb_id: '',
    premiere: '',
    final: '',
    showSelect: [],
    matches: ['S14E24', 'S08E22'],
    status_option: [
      'Airing',
      'Hiatus',
      'Ended',
    ],
    units: [],
    json: {},
    name_option: [
      { text: 'Name required', value: true },
      { text: 'Name optional', value: false },
    ],
    anime_option: [
      { text: 'Anime: Yes', value: true },
      { text: 'Anime: No', value: false },
    ],
    status: null,
    anime: false,
    name_needed: true,
    reg: [],
  }),
  computed: {
  },
  created() {
    this.$http.post('jobs/batch/files').then(
      (res) => {
        const body = _.defaults(res.body, {
        });
        this.json = body;
        this.units = body.units;
        this.reg = body.regex;
      },
      () => {
        this.$snotify.error('Failed to load data', { timeout: 0 });
      },
    );
  },
  mounted() {
    this.updateRegex();
  },
  methods: {
    async start() {
      this.$http
        .post('jobs/batch/match', this.json)
        .then(
          (res) => {
            this.$router.push({
              name: 'batch.validate',
              paras: res.body,
            });
          },
          (res) => {
            this.hasSubmitError = true;
            if (res.body) this.output = res.body;
          },
        );
    },
    async updateRegex() {
      if (this.units.length === 0) {
        setTimeout(this.updateRegex, 250);
        return;
      }
      this.matches = [];
      this.reg.forEach((r) => {
        if (r.value === '') { return; }
        this.units.forEach((o) => {
          if (o.value.length === 0) {
            const matched = o.text.match(r.value);
            if (matched === null) { return; }
            matched.forEach((m) => {
              if (m !== null) {
                this.matches.push(m);
              }
            });
          } else {
            o.value.forEach((v) => {
              const matched = v.match(r.value);
              if (matched === null) { return; }
              matched.forEach((m) => {
                if (m !== null) {
                  this.matches.push(m);
                }
              });
            });
          }
        });
      });
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
      if (this.tvdb_id === '') {
        const reqBody = { series_name: this.series_name, tvdb_id: this.tvdb_id, new_series: true };
        this.$http.post('jobs/tvdb', reqBody)
          .then(
            (res) => {
              const body = _.defaults(res.body, {
              });
              if ('newShows' in body) {
                this.showSelect = body.newShows;
                const [s] = body.newShows;
                this.tvdb_id = s.value;
              }
            },
            () => {
              this.$snotify.error('Failed to load data', { timeout: 0 });
            },
          );
      } else {
        if (this.isValidDateWithDash(this.premiere)) {
          if (this.status !== 'Ended') {
            if (this.final === '') {
              return;
            }
            this.final = '';
            return;
          }
        }
        if (this.isValidDateWithDash(this.final)) { return; }
        if (this.tvdb_id === '') {
          return;
        }
        this.$http.post('jobs/tvdb/dates', { tvdb_id: this.tvdb_id })
          .then(
            (res) => {
              const body = _.defaults(res.body, {
              });
              if ('premiere' in body) {
                this.premiere = body.premiere;
              }
              if (this.status === 'Ended' && 'final' in body) {
                this.final = body.final;
              }
              if (this.status !== 'Ended') {
                this.final = '';
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
