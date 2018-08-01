<template>
  <div>
    <b-card
      :border-variant="getColor(s.status)"
      no-body
      class="mt-3 pb-3 px-3"
      @dates="getDates">
      <b-row>
        <b-col
          sm
          class="px-2">
          <b-input
            v-model="s.series_name"
            :state="validateSeriesName"
            size="lg"
            class="mt-3"/>
        </b-col>
      </b-row>
      <b-row>
        <b-col
          sm
          class="px-2">
          <b-form-select
            v-model="s.status"
            :state="validateStatus"
            :options="status_option"
            class="mt-3"/>
        </b-col>
        <b-col
          sm
          class="px-2">
          <b-form-select
            v-model="s.name_needed"
            :state="validateNameNeeded"
            :options="name_option"
            class="mt-3"/>
        </b-col>
        <b-col
          sm
          class="px-2">
          <b-input
            v-model.number="s.tvdb_id"
            :state="validateTVDBID"
            class="mt-3"
            type="number"
            placeholder="TVDB ID"/>
        </b-col>
        <b-col
          sm
          class="px-2">
          <b-input
            v-model="s.premiere"
            :state="validatePremiere"
            :formatter="dateFormat"
            class="mt-3"
            lazy-formatter
            placeholder="Premiere"/>
        </b-col>
        <b-col
          sm
          class="px-2">
          <b-form-input
            v-model="s.final"
            :state="validateFinal"
            :formatter="dateFormat"
            type="text"
            class="mt-3"
            lazy-formatter
            placeholder="Final"/>
        </b-col>
      </b-row>
    </b-card>
  </div>
</template>

<script>
const _ = require('lodash');

export default {
  props: {
    s: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    json: {},
    status_option: [
      'Airing',
      'Hiatus',
      'Ended',
    ],
    name_option: [
      { text: 'Name required', value: true },
      { text: 'Name optional', value: false },
    ],
  }),
  computed: {
    validateSeriesName() {
      return this.s.series_name === this.s.series_name_unchanged ? null : true;
    },
    validateStatus() {
      return this.s.status === this.s.status_unchanged ? null : true;
    },
    validateNameNeeded() {
      return this.s.name_needed === this.s.name_needed_unchanged ? null : true;
    },
    validateTVDBID() {
      return this.s.tvdb_id === this.s.tvdb_id_unchanged ? null : true;
    },
    validatePremiere() {
      if (this.s.premiere === '') { return false; }
      return this.s.premiere === this.s.premiere_unchanged ? null : true;
    },
    validateFinal() {
      if (this.s.final === '' && this.s.status === 'Ended') { return false; }
      return this.s.final === this.s.final_unchanged ? null : true;
    },
  },
  created() {
    this.$parent.$on('dates', this.getDates);
  },
  mounted() {
    this.getDates();
  },
  methods: {
    async getDates() {
      if (this.isValidDateWithDash(this.s.premiere)) {
        if (this.s.status !== 'Ended') {
          if (this.s.final === '') {
            return;
          }
          this.s.final = '';
          return;
        }
      }
      if (this.isValidDateWithDash(this.s.final)) { return; }
      if (this.s.tvdb_id === '') {
        return;
      }
      this.$http.post('jobs/tvdb/dates', this.s)
        .then(
          (res) => {
            const body = _.defaults(res.body, {
            });
            if ('premiere' in body) {
              this.s.premiere = body.premiere;
            }
            if (this.s.status === 'Ended' && 'final' in body) {
              this.s.final = body.final;
            }
            if (this.s.status !== 'Ended') {
              this.s.final = '';
            }
          },
          () => {
            this.$snotify.error('Failed to load data', { timeout: 0 });
          },
        );
    },
    dateFormat(value) {
      if (this.isValidDateWithDash(value)) {
        return value;
      }
      return this.isValidDateNoDash(value);
    },
    getColor(status) {
      if (status === 'Hiatus') {
        return 'primary';
      }
      if (status === 'Airing') {
        return 'success';
      }
      if (status === 'Ended') {
        return 'warning';
      }
      return null;
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
  },
};
</script>
