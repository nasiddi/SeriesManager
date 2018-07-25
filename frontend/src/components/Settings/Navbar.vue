<template>
  <b-card
    header="Navbar">
    <b-form-group
      label="Variant">
      <b-form-select
        :options="variants"
        v-model="variant"
      />
    </b-form-group>
    <b-form-group
      label="Type">
      <b-form-select
        :options="types"
        v-model="type"
      />
    </b-form-group>
  </b-card>
</template>

<script>
export default {
  data: () => ({
    variants: [
      { value: 'primary', text: 'primary' },
      { value: 'success', text: 'success' },
      { value: 'info', text: 'info' },
      { value: 'warning', text: 'warning' },
      { value: 'danger', text: 'danger' },
      { value: 'dark', text: 'dark' },
      { value: 'light', text: 'light' },
    ],
    types: [{ value: 'light', text: 'light' }, { value: 'dark', text: 'dark' }],
  }),
  computed: {
    type: {
      get() {
        return this.$store.getters.setting('navbar.type', true);
      },
      set(value) {
        this.$store.dispatch('saveSetting', {
          key: 'navbar.type',
          value,
        });
      },
    },
    variant: {
      get() {
        return this.$store.getters.setting('navbar.variant', true);
      },
      set(value) {
        this.$store.dispatch('saveSetting', {
          key: 'navbar.variant',
          value,
        });
      },
    },
  },
};
</script>
