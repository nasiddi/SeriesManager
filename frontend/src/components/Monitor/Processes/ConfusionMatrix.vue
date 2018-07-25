<template>

  <b-table
    :items="table.items"
    :fields="table.fields"
    responsive
    striped
    small
    hover/>
</template>

<script>
const _ = require('lodash');

export default {
  props: {
    data: {
      type: Array,
      required: true,
    },
  },
  computed: {
    table() {
      if (!this.data) {
        return false;
      }

      const header = this.data[0];
      return {
        items: _.chain(this.data)
          .tail()
          .map(row => _.zipObject(header, row))
          .value(),
        fields: _.map(header, cell => ({ key: cell, label: cell })),
      };
    },
  },
};
</script>
