<template>
  <div>
    <h2>Parse Results</h2>
    <div v-if="analysis.errorCount > 0">
      <h3>Errors <b-badge variant="warning">{{ analysis.errorCount }}</b-badge></h3>
      <pre
        v-for="(line, i) in analysis.errorLines"
        :key="i">
        {{ line }}
      </pre>
    </div>

    <div v-if="analysis.rowCount > 0">
      <h3>Data</h3>
      <em>The first {{ analysis.rowLimit }} rows are shown.</em>
      <b-table
        :fields="fields"
        :items="analysis.rowTable"
        responsive
        striped
        hover
      />
    </div>
  </div>
</template>

<script>
const _ = require('lodash');

export default {
  props: {
    analysis: {
      type: Object,
      required: true,
    },
  },
  computed: {
    fields() {
      return _.zipObject(
        this.analysis.columns,
        _.map(this.analysis.columns, () => ({
          sortable: true,
        })),
      );
    },
  },
};
</script>
