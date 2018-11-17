<template>
  <div>
    <b-row class="mb-4">
      <b-col
        sm=""
        class="px-2">
        <b-button
          :style="{width: '100%'}"
          type="start"
          variant="primary"
          size="lg"
          class="mt-3"
          block
          @click.prevent="start"
        >Start</b-button>
      </b-col>
    </b-row>
    <RegexForm
      v-for="r in reg"
      v-if="r.key < counter"
      :key="r.key"
      :regex="r"/>
    <b-row class="mb-4">
      <b-col
        sm=""
        class="px-2">
        <b-button
          :disabled="disableButton()"
          :style="{width: '100%'}"
          type="add"
          variant="primary"
          class="mt-3"
          block
          @click.prevent="addRegex"
        >Add Regex</b-button>
      </b-col>
    </b-row>
    <b-row class="mb-4">
      <b-col
        sm=""
        class="px-2">
        <b-button
          :style="{width: '100%'}"
          type="update"
          variant="primary"
          class="mt-3"
          block
          @click.prevent="updateRegex"
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
          v-if="'files' in u && u.files.length === 0"
          no-body
          class="px-2 py-2 mt-2">
          <text-highlight
            :queries="matches">
            {{ u.text }}
          </text-highlight>
        </b-card>
        <b-button
          v-b-toggle="u.text"
          v-if="'files' in u && u.files.length > 0"
          :pressed.sync="u.opened"
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
              v-for="f in u.files"
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
  </div>
</template>

<script>
import TextHighlight from 'vue-text-highlight';
import RegexForm from './RegexForm';


const _ = require('lodash');

export default {
  components: {
    TextHighlight,
    RegexForm,
  },
  data: () => ({
    reg: [],
    units: [],
    counter: 1,
    matches: [],
  }),
  watch: {
  },
  created() {
    this.loadData();
  },
  mounted() {
    this.updateRegex();
  },
  methods: {
    loadData() {
      this.$http.post('jobs/batch/files').then(
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
            this.units = body.units;
            this.reg = body.regex;
          }
        },
        () => {
          this.$snotify.error('Failed to load data', { timeout: 0 });
        },
      );
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
    unlockShowsStart() {
      this.$snotify.remove(this.notifLock.id);
      this.$http.post('jobs/unlock')
        .then(
          (res) => {
            this.json = res;
            this.start();
          },
        );
    },
    disableButton() {
      return this.counter === 10;
    },
    async start() {
      this.$http
        .post('jobs/batch/match', this.json)
        .then(
          (res) => {
            if ('shows_locked' in res.body) {
              this.notifLock = this.$snotify.confirm('', 'Shows locked', {
                timeout: 0,
                buttons: [
                  { text: 'Unlock', action: () => this.unlockShowsStart(), bold: true },
                ],
              });
            } else {
              this.$snotify.error('res.body', { timeout: 0 });
              this.$router.push({
                name: 'batch.validate',
                paras: res.body,
              });
            }
            this.$snotify.error(res.body, { timeout: 0 });
          },
          (res) => {
            this.hasSubmitError = true;
            this.$snotify.error('res.body', { timeout: 0 });
            if (res.body) this.output = res.body;
          },
        );
    },
    updateRegex() {
      if (this.units.length === 0) {
        setTimeout(this.updateRegex, 250);
        return;
      }
      this.matches = [];
      this.reg.forEach((r) => {
        const regex = r;
        regex.matches = [];
        regex.sxe = [];
        if (r.regex === '') { return; }
        this.units.forEach((u) => {
          if (u.files.length > 0) {
            u.files.forEach((f) => {
              const match = f.match(r.regex);
              if (match !== null) {
                regex.matches = r.matches.concat(match);
                this.matches = this.matches.concat(match);
                match.forEach((m) => {
                  if (r.s_start !== '' && r.s_end !== '') {
                    r.sxe.push(m.slice(r.s_start, r.s_end));
                  }
                  if (r.e_start !== '' && r.e_end !== '') {
                    r.sxe.push(m.slice(r.e_start, r.e_end));
                  }
                });
              }
            });
          } else {
            const match = u.text.match(r.regex);
            if (match !== null) {
              regex.matches = r.matches.concat(match);
              this.matches = this.matches.concat(match);
              match.forEach((m) => {
                if (r.s_start !== '' && r.s_end !== '') {
                  r.sxe.push(m.slice(r.s_start, r.s_end));
                }
                if (r.e_start !== '' && r.e_end !== '') {
                  r.sxe.push(m.slice(r.e_start, r.e_end));
                }
              });
            }
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
    addRegex() {
      if (this.counter <= 10) {
        this.counter += 1;
      }
    },
  },
};
</script>
