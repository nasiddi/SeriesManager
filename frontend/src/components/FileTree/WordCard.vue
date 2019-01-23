<template>
  <div
    v-if="e.length !== 0 && 'words' in e">
    <b-card
      no-body
      class="px-3 pt-1 pb-2 mt-2">
      <b-row>
        <b-col
          class="px-1 mt-1"
          sm="1"
          order="3"
          order-md="1">
          <b-button
            :disabled="setInput(e.words[0])"
            :pressed.sync="e.words[0].add"
            :variant="'outline-success'"
            :style="{width: '100%'}"
          >Add</b-button>
        </b-col>
        <b-col
          class="px-1 mt-1"
          sm="3"
          order="2"
          order-md="2">
          <b-input
            v-model="e.words[0].word"
            :state="wordState(e.words[0])"/>
        </b-col>
        <b-col
          class="px-1 mt-1"
          sm="8"
          order="1"
          order-md="3">
          <b-input
            v-model="e.file"
            disabled/>
        </b-col>
      </b-row>
      <b-row
        v-for="w in e.words.slice(1)"
        :key="w.key">
        <b-col
          class="px-1 mt-1"
          sm="1"
          order="2"
          order-md="1">
          <b-button
            :pressed.sync="w.add"
            :variant="'outline-success'"
            :style="{width: '100%'}"
          >Add</b-button>
        </b-col>
        <b-col
          class="px-1 mt-1"
          sm="3"
          order="1"
          order-md="2">
          <b-input
            v-model="w.word"
            :state="wordState(w)"/>
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
        e.words.forEach((w) => {
          if (this.checkWrongSymbols(w.word)) {
            this.updateSave(false);
          }
        });
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
    this.e.words = _.sortBy(this.e.words.slice(1), 'key');
  },
  methods: {
    setInput(w) {
      if (w.lastInput === '') {
        // eslint-disable-next-line no-param-reassign
        w.lastInput = null;
      }
      return false;
    },
    wordState(w) {
      if (this.checkWrongSymbols(w.word)) {
        // eslint-disable-next-line no-param-reassign
        w.add = false;
        // eslint-disable-next-line no-param-reassign
        w.lastInput = false;
        return false;
      }

      let state = null;
      if (w.key !== w.word) {
        state = true;
        // eslint-disable-next-line no-param-reassign
        w.changed = true;
      } else {
        state = null;
        // eslint-disable-next-line no-param-reassign
        w.changed = false;
      }
      if (w.lastInput === false) {
        // eslint-disable-next-line no-param-reassign
        w.add = true;
      }
      return state;
    },
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
  },
};
</script>
