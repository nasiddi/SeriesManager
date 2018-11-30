<template>

  <div>
    <div v-if="Object.keys(json).length !== 0">
      <b-button
        variant="success"
        size="lg"
        block
        class="my-3"
        @click.prevent="save"
      >Save Changes</b-button>
      <b-row
        v-for="(list, k) in json"
        :key="list.order"
        class="mt-3">
        <b-col>
          <b-button
            :class="list.open ? 'collapsed' : null"
            :aria-expanded="list.open ? 'true' : 'false'"
            :style="{width: '100%'}"
            aria-controls="k"
            @click="list.open = !list.open"
          >{{ list.title }}</b-button>
          <b-collapse
            :id="k"
            v-model="list.open">
            <InfoCard
              v-for="v in list.items"
              ref="card"
              :key="v.key"
              :e="v"
              class="mt-2 px-3"/>
          </b-collapse>
        </b-col>
      </b-row>
      <b-button
        variant="success"
        size="lg"
        block
        class="my-3"
        @click.prevent="save"
      >Save Changes</b-button>
    </div>
</div></template>

<script>
import InfoCard from './InfoCard';

const _ = require('lodash');


export default {
  components: {
    InfoCard,
  },
  data: () => ({
    json: {},
    opened: {},
    dictionary: [],
    part: [],
    lower: {},
    upper: {},
    double: {},
    lowerGeneral: {},
  }),
  computed: {
  },
  watch: {
  },
  created() {
    this.loadData();
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
      this.$http.post('jobs/infofiles/load', { series_name: '*' }).then(
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
            _.keys(body).forEach((k) => {
              this.opened[k] = false;
            });
          }
          this.$snotify.remove(this.notifLoading.id);
        },
        () => {
          this.$snotify.error('Failed to load data', { timeout: 0 });
        },
      );
    },
    save() {
      this.notifLoading = this.$snotify.info('Saving', { timeout: 0 });
      this.$http.post('jobs/infofiles/save', this.json).then(
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
            this.$snotify.remove(this.notifLoading.id);
            this.loadData();
            this.$snotify.success('Done', { timeout: 500 });
          }
          this.$snotify.remove(this.notifLoading.id);
        },
        () => {
          this.$snotify.error('Failed to save data', { timeout: 0 });
        },
      );
    },
  },
};
</script>
