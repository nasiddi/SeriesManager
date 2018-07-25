<template>

  <b-table
    :items="table.items"
    :fields="table.fields"
    responsive
    striped
    small
    hover>
    <template
      slot="HEAD_empty"
      slot-scope="data">&nbsp;</template>
  </b-table>

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

      const header = _.chain(this.data[0])
        .map(v => (v === '' ? 'empty' : v))
        .value();
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
