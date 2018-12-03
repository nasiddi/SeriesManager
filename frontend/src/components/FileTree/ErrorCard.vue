<template>
  <div
    v-if="e.length !== 0">
    <b-card
      :title="e.message"
      :style="{width: '100%'}"
      :header="e.header"
      class="mt-2 text-center">
      <b-row>
        <b-col
          class="px-2 mb-1">
          <b-button
            :style="{width: '100%'}"
            :variant="buttonColor"
            aria-controls="'e' + e.key.toString()"
          >{{ enr }}</b-button>
        </b-col>
        <b-col
          class="px-2 mb-1"
          sm="9">
          <b-input
            id="title"
            v-model="e.title"/>
        </b-col>
        <b-col
          class="px-2 mb-1"
          sm>
          <b-col
            class="px-2 mb-1"
            sm>
            <b-input
              v-model="e.extension"
              :disabled="true"/>
          </b-col>
        </b-col>
      </b-row>
      <div>
        <b-row>
          <b-col
            class="px-2 mt-1">
            <b-input-group
              :style="{width: '100%'}"
              left="@">
              <b-input
                id="season"
                v-model.number="e.s_nr"
                type="number"
                placeholder="S" />
              <b-input
                id="episode"
                v-model.number="e.e_nr"
                type="number"
                placeholder="E" />
            </b-input-group>
          </b-col>
          <b-col
            class="px-2 mt-1"
            sm>
            <b-button
              :variant="'success'"
              :style="{width: '100%'}"
              @click="updateTitle"
            >Update</b-button>
          </b-col>
          <b-col
            class="px-2 mt-1"
            sm>
            <b-form-select
              v-model="e.exception"
              :options="exceptions"
              :style="{width: '100%'}"
              selected="false"/>
          </b-col>
          <b-col
            class="px-2 mt-1"
            sm>
            <b-button
              :pressed.sync="e.delete"
              :variant="'outline-danger'"
              :style="{width: '100%'}"
            >Delete</b-button>
          </b-col>
        </b-row>
        <b-row class="text-center mt-1">
          <b-col
            class="px-2"
            sm>
            <b-card
              :style="{width: '100%'}"
              class="text-center py-1 mt-1"
              no-body>
              {{ e.old_location }}
            </b-card>
          </b-col>
        </b-row>
      </div>
    </b-card>
  </div>
</template>

<script>


const _ = require('lodash');


export default {
  components: {
  },
  props: {
    e: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    exceptions: [
      { value: false, text: 'Exception' },
      { value: 'part', text: 'Part' },
      { value: 'lower', text: 'lowerCase' },
      { value: 'upper', text: 'UpperCase' },
      { value: 'double', text: 'DoubleTitle' },
      { value: 'lower_general', text: 'lowerGeneral' },
    ],
    episode_options: [
      'Single',
      'Double',
      'Triple',
    ],
    original: {},
  }),
  computed: {
    buttonColor() {
      return 'danger';
    },
    enr() {
      const eo = this.e.episode_option;
      if (eo === 'Single') {
        return this.pad2(this.e.e_nr);
      }
      if (eo === 'Double') {
        return `${this.pad2(this.e.e_nr)} & ${this.pad2(this.e.e_nr + 1)}`;
      }
      return `${this.pad2(this.e.e_nr)} & ${this.pad2(this.e.e_nr + 1)} & ${this.pad2(this.e.e_nr + 2)}`;
    },
  },
  watch: {
  },
  mounted() {
    this.original = _.cloneDeep(this.e);
    this.updated = _.cloneDeep(this.e);
  },
  methods: {
    pad2(number) {
      return (number < 10 ? '0' : '') + number;
    },
    async updateTitle() {
      return new Promise((resolve) => {
        const file = this.e;
        this.$http.post('jobs/tvdb', file)
          .then(
            (res) => {
              const body = _.defaults(res.body, {
              });
              if (!('title' in body)) {
                this.$snotify.error(file.series_name, 'Title failed', { timeout: 5000 });
                return resolve(false);
              }
              file.title = body.title;
              if (file.episode_option !== 'Single') {
                if (!('title2' in body)) {
                  this.$snotify.error(file.series_name, 'Title 2 failed', { timeout: 5000 });
                  return resolve(false);
                }
                file.title2 = body.title2;
              }
              if (file.episode_option === 'Triple') {
                if (!('title3' in body)) {
                  this.$snotify.error(file.series_name, 'Title 3 failed', { timeout: 5000 });
                  return resolve(false);
                }
                file.title3 = body.title3;
              }
              return resolve(true);
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
