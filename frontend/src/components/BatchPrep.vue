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
      <b-row class="mb-4">
        <b-col
          sm
          class="px-2">
          <b-input
            v-model.lazy="reg1"
            class="mt-2"
            placeholder="Regex" />
        </b-col>
        <text-highlight
          :queries="matchesSE1">
          {{ matches1 }}
        </text-highlight>
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
            class="px-2 py-2 mt-2"/>
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
                queries="S[0-9]{2}E[0-9]{2}">
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
    reg1: 'S[0-9]{2}E[0-9]{2}',
    matches1: '',
    matchesSE1: [],
    units: [],
  }),
  watch: {
    reg1: function r(val) {
      this.updateRegex(val);
    },
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
    updateRegex(r) {
      if (this.units.length === 0) {
        setTimeout(this.updateRegex, 250);
        return '';
      }
      let matches1 = '';
      this.matches = [];
      this.units.forEach((o) => {
        if (o.value.length === 0) {
          const matched = o.text.match(r.value);
          if (matched === null) { return; }
          matched.forEach((m) => {
            if (m !== null) {
              this.matches.push(m);
              matches1 = m;
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
      return matches1;
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
