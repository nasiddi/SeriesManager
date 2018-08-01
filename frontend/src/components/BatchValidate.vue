<template>
  <div>
    <BatchCard
      v-for="f in json.files"
      :key="f.location"
      :f="f"/>
  </div>

</template>

<script>
import BatchCard from './BatchCard';

const _ = require('lodash');

export default {
  components: {
    BatchCard,
  },
  data: () => ({
    json: {},
  }),
  created() {
    this.$http.post('jobs/batch/start').then(
      (res) => {
        const body = _.defaults(res.body, {
        });
        this.json = body;
      },
      () => {
        this.$snotify.error('Failed to load data', { timeout: 0 });
      },
    );
  },
  mounted() {
  },
  methods: {
  },
};
</script>
