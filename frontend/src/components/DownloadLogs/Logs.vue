<template>
  <div v-if="Object.keys(json).length !== 0">
    <b-row
      v-for="log in json"
      :key="log.file"
      class="mt-3">
      <b-col>
        <b-button
          :class="log.opened ? 'collapsed' : null"
          :aria-expanded="log.opened ? 'true' : 'false'"
          :style="{width: '100%'}"
          :aria-controls="log.file"
          @click="log.opened = !log.opened"
        >{{ log.file }}</b-button>
        <b-collapse
          :id="log.file"
          v-model="log.opened">
          <div
            v-for="l in log.data"
            :key="l.key">
            <b-button
              :class="l.opened ? 'collapsed' : null"
              :aria-expanded="l.opened ? 'true' : 'false'"
              :style="{width: '100%'}"
              :aria-controls="l.key"
              @click="l.opened = !l.opened"
            >{{ l.key }}</b-button>
            <b-collapse
              :id="l.key"
              v-model="l.opened">
              <b-alert
                v-for="f in l.files"
                :key="f"
                :style="{width: '100%'}"
              >{{ f }}</b-alert>
            </b-collapse>
          </div>
        </b-collapse>
      </b-col>
    </b-row>
  </div>
</template>

<script>

const _ = require('lodash');

export default {
  components: {
  },
  data: () => ({
    json: {},
  }),
  computed: {},
  created() {
    this.loadData();
  },
  methods: {
    loadData() {
      this.notifLoading = this.$snotify.info('Loading', {
        timeout: 0,
      });
      this.$http.post('python/loadlogs').then(
        (res) => {
          if (res.body === 'failed') {
            this.$snotify.remove(this.notifLoading.id);
            this.$snotify.error('Python failed', { timeout: 0 });
            return;
          }
          const body = _.defaults(res.body, {});
          this.json = body;
          // eslint-disable-next-line no-console
          console.log(this.json[0].data[0].key);
        },
        () => {
          this.$snotify.error('Failed to load data', { timeout: 0 });
        },
      );
    },
    async sync() {
      this.$router.push({
        name: 'sync.report',
        params: this.json.files,
      });
    },
  },
};
</script>
