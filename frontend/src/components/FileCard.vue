<template>
  <div
    v-if="file.length !== 0">
    <b-card
      :header="file.location"
      class="mt-3">
      <b-form
        inline>
        <label
          class="sr-only"
          for="fc">Name</label>
        <b-form-select
          v-model="file.type_option.selected"
          :options="file.type_option.options"
          :style="{width: '100px'}"
          selected="Series"
          class="mr-2 mb-2"/>
        <b-input
          id="title"
          v-model="file.title"
          :style="{width: '55%'}"
          class="mb-2 mr-2"
          placeholder="Title" />
        <b-button
          :pressed.sync="file.override"
          :variant="'outline-primary'"
          :style="{width: '100px'}"
          class="mr-2 mb-2"
        >Override</b-button>
        <b-button
          :pressed.sync="file.show_subs"
          :variant="'outline-primary'"
          :disabled="subs.length === 0"
          :style="{width: '100px'}"
          class="mr-2 mb-2"
        >Subtitles</b-button>
        <b-button
          :pressed.sync="file.sync"
          :variant="setColor(file)"
          :style="{width: '100px'}"
          class="mb-2"
          @click="checkData(file)"
        >Sync</b-button>
      </b-form>
      <b-form
        v-if="file.type_option.selected === 'Series'"
        inline>
        <b-input
          v-if="file.manual === true"
          id="series-manual"
          :style="{width: '55%'}"
          class="mr-2 mt-2"
          placeholder="Series Name"/>
        <b-form-select
          v-if="file.manual === false"
          id="series-selector"
          v-model="file.series_name"
          :options="Object.keys(shows)"
          :style="{width: '55%'}"
          selected="file.series_name"
          class="mr-2 mt-2"/>
        <label
          class="sr-only"
          for="series-form">Username</label>
        <b-input-group
          :style="{width: '100px'}"
          left="@"
          class="mr-2 mt-2">
          <b-input
            id="season"
            v-model.number="file.s_nr"
            type="number"
            placeholder="S" />
          <b-input
            id="episode"
            v-model.number="file.e_nr"
            type="number"
            placeholder="E" />
        </b-input-group>
        <b-form-select
          v-model="file.episode_option.selected"
          :options="file.episode_option.options"
          :style="{width: '100px'}"
          selected="Single"
          class="mr-2 mt-2"/>
        <b-button
          :pressed.sync="file.manual"
          :variant="'outline-primary'"
          :style="{width: '100px'}"
          class="mr-2 mt-2"
        >Manual</b-button>
        <b-button
          :variant="'success'"
          :style="{width: '100px'}"
          class="mt-2"
          @click="updateTitle(file)"
        >Update</b-button>
      </b-form>
      <b-input
        v-if="file.episode_option.selected !== 'Single' && file.type_option.selected === 'Series'"
        id="title2"
        v-model="file.title2"
        class="mt-3"
        placeholder="Title 2" />
      <b-input
        v-if="file.episode_option.selected === 'Triple' && file.type_option.selected === 'Series'"
        id="title3"
        v-model="file.title3"
        class="mt-3"
        placeholder="Title 3" />
      <b-form-checkbox-group
        v-if="file.show_subs === true"
        v-model="file.subs"
        :options="subs"
        :style="{width: '100%'}"
        buttons
        button-variant="outline-primary"
        class="mt-3"
        stacked/>
    </b-card>
  </div>
</template>

<script>


const _ = require('lodash');


export default {
  components: {
  },
  props: {
    file: {
      type: Object,
      required: true,
    },
    shows: {
      type: Object,
      required: true,
    },
    subs: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
  }),
  computed: {
  },
  methods: {
    async checkData(file) {
      const f = file;
      let sync = false;
      if (file.title === '') {
        sync = false;
      } else {
        sync = true;
      }
      if (sync && file.sync) {
        return;
      }
      f.sync = false;
    },
    setColor(file) {
      if (file.override) {
        return 'outline-primary';
      }
      return 'outline-danger';
    },
    async updateTitle(f) {
      return new Promise((resolve) => {
        const file = f;
        file.tvdb = this.shows[file.series_name];
        this.$http.post('jobs/tvdb', file)
          .then(
            (res) => {
              const body = _.defaults(res.body, {
              });
              if (!('title' in body)) {
                this.$snotify.error('Failed to load title', file.series_name, { timeout: 0 });
              }
              file.title = body.title;
              if (file.episode_option.selected !== 'Single') {
                if (!('title2' in body)) {
                  this.$snotify.error('Failed to load title 2', file.series_name, { timeout: 0 });
                }
                file.title2 = body.title2;
              }
              if (file.episode_option.selected === 'Triple') {
                if (!('title3' in body)) {
                  this.$snotify.error('Failed to load title 3', file.series_name, { timeout: 0 });
                }
                file.title3 = body.title3;
              }
              resolve(true);
            },
            () => {
              this.$snotify.error('Failed to load data', { timeout: 0 });
              resolve(false);
            },
          );
      });
    },
  },
};
</script>
