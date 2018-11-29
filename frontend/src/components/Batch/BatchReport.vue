<template>
  <div>
    <div>
      <b-button
        type="dashboard"
        variant="primary"
        size="lg"
        class="mt-3"
        block
        @click.prevent="dashboard"
      >Dashboard</b-button>
    </div>
    <div
      v-if="json.length !== 0"
      class="mt-3">
      <b-alert
        v-if="'summary' in json"
        show
        class="mt-2 mb-0"
        variant="success">
        <h4>{{ json.summary.total }}</h4>
        <div
          v-for="s in json.summary.seasons"
          :key="s">
          <hr>
          <p>{{ s }}</p>
        </div>
        <div v-if="'subs' in json.summary">
          <hr>
          <p>{{ json.summary.subs }}</p>
        </div>
      </b-alert>
      <div v-if="'error' in json && json.error.length !== 0" >
        <hr>
        <b-alert
          v-for="err in json.error"
          :key="err"
          show
          class="mt-2 mb-0"
          variant="danger">{{ err }}
        </b-alert>
      </div>
      <div v-if="'info' in json && json.info.length !== 0" >
        <hr>
        <b-alert
          v-for="info in json.info"
          :key="info"
          show
          class="mt-2 mb-0"
          variant="primary">{{ info }}
        </b-alert>
      </div>
      <div v-if="'success' in json && json.success.length !== 0" >
        <hr>
        <b-alert
          v-for="success in json.success"
          :key="success"
          show
          class="mt-2 mb-0"
          variant="success">{{ success }}
        </b-alert>
      </div>
      <b-button
        type="dashboard"
        variant="primary"
        size="lg"
        class="mt-3"
        block
        @click.prevent="dashboard"
      >Dashboard</b-button>
    </div>
  </div>
</template>

<script>
const _ = require('lodash');

export default {
  data: () => ({
    json: {},
  }),
  created() {
    this.loadData();
  },
  mounted() {
  },
  methods: {
    async dashboard() {
      this.$router.push({ name: 'dashboard' });
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
      this.$http.post('jobs/batch/sync', this.$route.params).then(
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
  },
};
</script>
