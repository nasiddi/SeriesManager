<template>
  <div v-if="Object.keys(json).length !== 0">
    <b-button
      type="sync"
      variant="primary"
      size="lg"
      block
      @click.prevent="sync"
    >Sync</b-button>
    <b-card
      v-for="file in json.files"
      :key="file.location"
      :header="file.location"
      class="mt-3">
      <b-form
        inline>
        <label
          class="sr-only"
          for="file-card">Name</label>
        <b-form-select
          v-model="file.type_option.selected"
          :options="file.type_option.options"
          :style="{width: '100px'}"
          selected="Series"
          class="mr-2"/>
        <b-form
          v-if="file.type_option.selected === 'Series'"
          inline>
          <b-input
            v-if="file.field_selector === 'manual'"
            id="series-manual"
            :style="{width: '345px'}"
            class="mr-2"
            placeholder="Series"/>
          <b-form-select
            v-if="file.field_selector === 'selectable'"
            id="series-selector"
            v-model="file.series_name"
            :options="series_options"
            :style="{width: '345px'}"
            selected="file.series_name"
            class="mr-2"/>
          <label
            class="sr-only"
            for="series-form">Username</label>
          <b-input-group
            :style="{width: '100px'}"
            left="@"
            class="mr-2">
            <b-input
              id="season"
              v-model="file.s_nr"
              placeholder="S" />
            <b-input
              id="episode"
              v-model="file.e_nr"
              placeholder="E" />
          </b-input-group>
          <b-form-select
            v-model="file.episode_option.selected"
            :options="file.episode_option.options"
            :style="{width: '100px'}"
            selected="Single"
            class="mr-2"/>
          <b-form-checkbox
            v-model="file.field_selector"
            value="manual"
            unchecked-value="selectable">Manual</b-form-checkbox>
        </b-form>
      </b-form>
      <b-form
        inline
        class="mt-3">
        <b-input
          id="title"
          v-model="file.e_name"
          :style="{width: '669px'}"
          class="mr-2"
          placeholder="Title" />
        <b-form-checkbox
          v-model="file.syncit"
          value="sync"
          selected="sync"
          unchecked-value="nosync">Sync</b-form-checkbox>
      </b-form>
    </b-card>
    <b-button
      type="sync"
      variant="primary"
      size="lg"
      block
      @click.prevent="sync"
    >Sync</b-button>
  </div>
</template>

<script>

const _ = require('lodash');


export default {
  components: {
  },
  data: () => ({
    json: {},
    series_selected: 'Series Name',
    series_options: [],
  }),
  mounted() {
    const notifLoading = this.$snotify.info('Loading', {
      timeout: 0,
    });
    this.$http
      .get('jobs/names')
      .then(
        (res) => {
          const body = _.defaults(res.body, {
          });
          this.$snotify.remove(notifLoading.id);
          this.json = body;
          this.series_options = this.json.shows;
        },
        () => {
          this.$snotify.error('Failed to load data', { timeout: 0 });
        },
      );
  },
  methods: {
    async sync() {
      this.$http.post('jobs/sync/start', this.json.files);
    },
  },
};
</script>
