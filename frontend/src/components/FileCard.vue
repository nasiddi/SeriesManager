<template>
  <div
    v-if="e.length !== 0">
    <b-card
      :style="{width: '100%'}"
      no-body
      class="px-3 py-2 mt-2">
      <b-row>
        <b-col
          class="px-2 mb-1">
          <b-button
            :aria-expanded="edit ? 'true' : 'false'"
            :style="{width: '100%'}"
            :variant="buttonColor"
            aria-controls="'e' + e.key.toString()"
            @click="edit = !edit"
          >{{ enr }}</b-button>
        </b-col>
        <b-col
          class="px-2 mb-1"
          sm="9">
          <b-input
            id="title"
            :disabled="isEdit"
            v-model="e.title"/>
        </b-col>
        <b-col
          v-if="edit"
          class="px-2 mb-1"
          sm>
          <b-button
            :variant="'success'"
            :style="{width: '100%'}"
            @click="updateTitle"
          >Update</b-button>
        </b-col>
      </b-row>
      <div
        v-if="edit">
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
            <b-form-select
              v-model="e.episode_option"
              :options="episode_options"
              :style="{width: '100%'}"
              selected="Single"/>
          </b-col>
          <b-col
            class="px-2 mt-1"
            sm>
            <b-button
              :pressed.sync="e.save"
              :variant="saveColor"
              :style="{width: '100%'}"
            >Save</b-button>
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
        <b-row
          v-if="e.episode_option !== 'Single'"
          class="mt-2">
          <b-col
            sm
            class="px-2">
            <b-input
              id="checkTitle2"
              v-model="e.title2"
              placeholder="Title 2" />
          </b-col>
        </b-row>
        <b-row
          v-if="e.episode_option === 'Triple'"
          class="mt-2">
          <b-col
            sm
            class="px-2">
            <b-input
              id="title3"
              v-model="e.title3"
              placeholder="Title 3" />
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
              {{ e.duration }} min
            </b-card>
          </b-col>
          <b-col
            class="px-2"
            sm>
            <b-card
              :style="{width: '100%'}"
              class="text-center py-1 mt-1"
              no-body>
              {{ e.size }} MB
            </b-card>
          </b-col>
          <b-col
            class="px-2"
            sm>
            <b-card
              :style="{width: '100%'}"
              class="text-center py-1 mt-1"
              no-body>
              {{ e.quality }} res
            </b-card>
          </b-col>
          <b-col
            class="px-2"
            sm>
            <b-card
              :style="{width: '100%'}"
              class="text-center py-1 mt-1"
              no-body>
              {{ e.extension }}
            </b-card>
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
              {{ e.duration }} min
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
    episode_options: [
      'Single',
      'Double',
      'Triple',
    ],
    original: {},
    updated: {},
    edit: false,
    saveColor: 'outline-primary',
    wrongSymbols: [
      ':',
      '/',
      '{',
      '}',
      '(',
      ')',
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
    isEdit() {
      return !this.edit;
    },
    buttonColor() {
      return this.edit ? 'secondary' : 'outline-secondary';
    },
    title() {
      if (this.e.title === '') {
        return '';
      }
      const eo = this.e.episode_option;
      if (eo === 'Double' && this.e.title2 !== '') {
        return `${this.e.title} & ${this.e.title2}`;
      }
      if (eo === 'Triple' && this.e.title3 !== '') {
        return `${this.e.title} & ${this.e.title2} & ${this.e.title3}`;
      }
      return this.e.title;
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
    e: {
      handler(e) {
        const o = this.original;

        // const u = this.updated;
        if (this.checkWrongSymbols(e.title)) {
          return this.updateSave(false);
        }
        if (this.checkWrongSymbols(e.title2)) {
          return this.updateSave(false);
        }
        if (this.checkWrongSymbols(e.title3)) {
          return this.updateSave(false);
        }
        if (e.name_needed) {
          if (e.title === '') {
            return this.updateSave(false);
          }
        }
        if (e.s_nr === '' || e.e_nr === '') {
          return this.updateSave(false);
        }
        this.updateSave(true);

        if (e.delete) {
          e.save = false;
          return true;
        }

        if (!this.hasChanged(e)) {
          e.save = false;
          o.save = e.save;
          return true;
        }
        if (e.save !== o.save) {
          o.save = e.save;
          return e.save;
        }

        e.save = true;
        o.save = e.save;
        return e.save;
      },
      deep: true,
    },
  },
  mounted() {
    this.original = _.cloneDeep(this.e);
    this.updated = _.cloneDeep(this.e);
  },
  methods: {
    hasChanged(e) {
      const o = this.original;
      if (e.title !== o.title) {
        return true;
      }
      if (e.title !== o.title) {
        return true;
      }
      if (e.title2 !== o.title2) {
        return true;
      }
      if (e.title3 !== o.title3) {
        return true;
      }
      if (e.e_nr !== o.e_nr) {
        return true;
      }
      if (e.s_nr !== o.s_nr) {
        return true;
      }
      if (e.episode_option !== o.episode_option) {
        return true;
      }
      return false;
    },
    pad2(number) {
      return (number < 10 ? '0' : '') + number;
    },
    checkWrongSymbols(val) {
      let found = false;
      this.wrongSymbols.forEach((sym) => {
        if (val.includes(sym)) {
          found = true;
        }
      });
      return found;
    },
    updateSave(primary) {
      if (primary) {
        this.saveColor = 'outline-primary';
      } else {
        this.saveColor = 'outline-danger';
        this.e.save = false;
        this.original.save = false;
      }
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
