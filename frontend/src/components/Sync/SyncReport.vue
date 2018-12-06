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
    <div v-if="json.length !== 0">
      <b-card
        v-for="file in json"
        :key="file.file_name"
        :header="file.file_name"
        no-body
        class="mt-3 pb-2">
        <b-alert
          v-for="err in file.error"
          :key="err"
          show
          class="mt-2 mx-2 mb-0"
          variant="danger">{{ err }}
        </b-alert>
        <b-alert
          v-for="success in file.success"
          :key="success"
          show
          class="mt-2 mb-0 mx-2"
          variant="success">{{ success }}
        </b-alert>
        <b-alert
          v-for="info in file.info"
          :key="info"
          show
          class="mt-2 mb-0 mx-2"
          variant="primary">{{ info }}
        </b-alert>
      </b-card>
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
      this.$http.post('python/sync/start', this.$route.params).then(
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
        },
        () => {
          this.$snotify.error('Failed to load data', { timeout: 0 });
        },
      );
    },
    async dashboard() {
      this.$router.push({ name: 'dashboard' });
    },
  },
};
</script>
