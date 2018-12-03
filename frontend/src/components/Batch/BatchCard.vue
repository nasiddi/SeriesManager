<template>
  <div
    v-if="f.length !== 0"
    sm
    class="px-0">
    <b-card
      :header="f.location"
      :header-border-variant="validateFile"
      :border-variant="validateFile"
      class="mt-3">
      <b-row>
        <b-col
          sm="6"
          class="pl-2 pr-2">
          <b-input
            id="title"
            v-model="f.title"
            :state="checkTitle(f.title
            )"
            class="mt-2"
            placeholder="Title" />
        </b-col>
        <b-col
          sm
          class="pl-2 pr-2">
          <label
            class="sr-only"
            for="series-form">Username</label>
          <b-input-group
            :style="{width: '100%'}"
            left="@"
            class="mt-2">
            <b-input
              id="season"
              v-model.number="f.s_nr"
              type="number"
              placeholder="S" />
            <b-input
              id="episode"
              v-model.number="f.e_nr"
              type="number"
              placeholder="E" />
          </b-input-group>
        </b-col>
        <b-col
          sm
          class="pl-2 pr-2">
          <b-form-select
            v-model="f.episode_option"
            :options="episode_options"
            :style="{width: '100%'}"
            class="mt-2"/>
        </b-col>
        <b-col
          sm
          class="pl-2 pr-2">
          <b-button
            :variant="'primary'"
            :style="{width: '100%'}"
            class="mt-2"
            @click="updateTitle(f)"
          >Update</b-button>
        </b-col>
      </b-row>
      <b-row>
        <b-col
          sm
          class="pl-2 pr-2">
          <b-input
            v-if="f.episode_option !== 'Single'"
            id="checkTitle2"
            v-model="f.title2"
            :state="checkTitle(f.title2)"
            class="mt-2"
            placeholder="Title 2" />
        </b-col>
      </b-row>
      <b-row>
        <b-col
          sm
          class="pl-2 pr-2">
          <b-input
            v-if="f.episode_option === 'Triple'"
            id="title3"
            v-model="f.title3"
            :state="checkTitle(f.title3)"
            class="mt-2"
            placeholder="Title 3" />
        </b-col>
      </b-row>
    </b-card>
  </div>
</template>

<script>


const _ = require('lodash');


export default {
  components: {
  },
  props: {
    f: {
      type: Object,
      required: true,
    },
    tvdb_id: {
      type: String,
      required: true,
    },
    name_needed: {
      type: Boolean,
      required: true,
    },
  },
  data: () => ({
    episode_options: [
      'Single',
      'Double',
      'Triple',
    ],
    syncColor: 'outline-danger',
    wrongSymbols: [
      ':',
      '/',
      '{',
      '}',
      '\\',
      '<',
      '>',
      '*',
      '?',
      '$',
      '!',
      '@',
    ],
  }),
  computed: {
    validateFile() {
      // eslint-disable-next-line vue/no-side-effects-in-computed-properties
      this.f.sync = false;
      let validated = 'danger';
      if (this.name_needed) {
        if (this.f.title === '') { return this.validated; }
        if (this.f.episode_option !== 'Single' && this.f.title2 === '') { return validated; }
        if (this.f.episode_option === 'Triple' && this.f.title3 === '') { return validated; }
      }
      if (this.f.s_nr === '' || this.f.e_nr === '') {
        return validated;
      }
      // eslint-disable-next-line vue/no-side-effects-in-computed-properties
      this.f.sync = true;
      validated = '';
      return validated;
    },
  },
  watch: {
  },
  mounted() {
  },
  methods: {
    checkTitle(val) {
      let valid = null;
      this.wrongSymbols.forEach((sym) => {
        if (val.includes(sym)) {
          valid = false;
        }
      });
      return valid;
    },
    updateSync(primary) {
      if (primary) {
        if (this.syncColor === 'outline-danger') {
          this.f.sync = true;
        }
        this.syncColor = 'outline-primary';
      } else {
        this.syncColor = 'outline-danger';
        this.f.sync = false;
      }
    },
    async updateTitle(f) {
      if (this.tvdb_id === '' || this.file.s_nr === '' || this.file.e_nr === '') {
        this.$snotify.error('Title failed', { timeout: 5000 });
        return;
      }
      const file = f;
      file.tvdb_id = this.tvdb_id;
      this.$http.post('jobs/tvdb', file)
        .then(
          (res) => {
            const body = _.defaults(res.body, {
            });
            if (!('title' in body)) {
              this.$snotify.error('Title failed', { timeout: 5000 });
            }
            file.title = body.title;
            if (file.episode_option !== 'Single') {
              if (!('title2' in body)) {
                this.$snotify.error('Title 2 failed', { timeout: 5000 });
              }
              file.title2 = body.title2;
            }
            if (file.episode_option === 'Triple') {
              if (!('title3' in body)) {
                this.$snotify.error('Title 3 failed', { timeout: 5000 });
              }
              file.title3 = body.title3;
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
