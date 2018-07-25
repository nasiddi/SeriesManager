<template>
  <b-card
    header="Parse">
    <b-form-group>
      <b-form-checkbox
        v-model="header"
        :value="true"
        :unchecked-value="false">
        Headers</b-form-checkbox>
    </b-form-group>
    <b-form-group>
      <b-form-checkbox
        v-model="smartHeader"
        :value="true"
        :unchecked-value="false">
        Smart columns</b-form-checkbox>
    </b-form-group>
    <b-form-group>
      <b-form-checkbox
        v-model="smartCsv"
        :value="true"
        :unchecked-value="false">
        Smart CSV parsing</b-form-checkbox>
    </b-form-group>
    <b-form-group
      label="Lines to show in preview">
      <b-form-input
        v-model="previewLines"
        :value="50"
        :min="0"
        :max="250"
        type="number"/>
    </b-form-group>
  </b-card>
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    header: {
      get() {
        return this.$store.getters.setting('parse.header', true);
      },
      set(value) {
        this.$store.dispatch('saveSetting', {
          key: 'parse.header',
          value,
        });
      },
    },
    smartHeader: {
      get() {
        return this.$store.getters.setting('parse.smartHeader', true);
      },
      set(value) {
        this.$store.dispatch('saveSetting', {
          key: 'parse.smartHeader',
          value,
        });
      },
    },
    smartCsv: {
      get() {
        return this.$store.getters.setting('parse.smartCsv', true);
      },
      set(value) {
        this.$store.dispatch('saveSetting', {
          key: 'parse.smartCsv',
          value,
        });
      },
    },
    previewLines: {
      get() {
        return this.$store.getters.setting('parse.previewLines', 50);
      },
      set(value) {
        this.$store.dispatch('saveSetting', {
          key: 'parse.previewLines',
          value,
        });
      },
    },
  },
};
</script>
