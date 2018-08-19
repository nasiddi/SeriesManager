<template>
  <div v-if="json.length !== 0 && 'shows' in json">
    <b-row class="mt-3">
      <b-col>
        <b-form-select
          v-model="selected"
          :options="Object.values(json.shows).map(s => s.series_name)"
          :style="{width: '100%'}"
          selected="Series"/>
      </b-col>
    </b-row>
    <b-row
      v-for="s in show.seasons"
      :key="s.key"
      class="mt-3">
      <b-col>
        <b-button
          v-b-toggle="'s' + s.key.toString()"
          :pressed.sync="s.opened"
          :variant="'outline-secondary'"
          :style="{width: '100%'}"
          class="mt-2"
        >Season {{ s.key }}</b-button>
        <b-collapse
          :id="'s' + s.key.toString()">
          <b-row
            v-for="e in s.episodes"
            :key="e.key"
            class="mt-2 px-3">
            <b-card
              :style="{width: '100%'}"
              no-body
              class="px-2 py-2 mt-2">
              <b-row>
                <b-col sm="10">
                  {{ (e.path) ? e.location : e.file_name }}
                </b-col>
                <b-col>
                  <b-button
                    v-b-toggle="'e' + e.key.toString()"
                    :pressed.sync="e.opened"
                    :variant="'outline-primary'"
                    :style="{width: '100%'}"
                    class="mt-2"
                  >Edit</b-button>
                </b-col>
              </b-row>
            </b-card>
          </b-row>
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
    show: {},
    selected: null,
  }),
  watch: {
    selected: {
      handler() {
        // eslint-disable-next-line prefer-destructuring
        this.show = Object.values(this.json.shows).filter(s => s.series_name === this.selected)[0];
      },
    },
  },
  created() {
    this.notifLoading = this.$snotify.info('loading', { timeout: 0 });
    this.$http.post('jobs/filetree', { series_name: '*' }).then(
      (res) => {
        const body = _.defaults(res.body, {
        });
        this.json = body;
        this.$snotify.remove(this.notifLoading.id);
      },
      () => {
        this.$snotify.error('Failed to load data', { timeout: 0 });
      },
    );
  },
  mounted() {
  },
  methods: {
  },
};
</script>
