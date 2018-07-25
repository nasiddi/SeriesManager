<template>
  <b-form-select
    :required="required"
    :options="jobIds"
    :value="jobId"
    @input="updateValue($event)"/>
</template>
<script>
const _ = require('lodash');
const moment = require('moment');

export default {
  name: 'JobDropdown',
  props: {
    jobId: {
      type: String,
      required: false,
      default: null,
    },
    required: {
      type: Boolean,
      default: true,
      required: false,
    },
  },
  data: () => ({
    httpTimeout: 3000,
    jobIds: {},
  }),
  mounted() {
    this.$http
      .get('jobs', { timeout: this.httpTimeout })
      .then((response) => {
        const formatter = (job) => {
          const date = moment
            .utc(job.created_at)
            .local()
            .format('YYYY-MM-DD HH:mm');
          return {
            text: `${job.friendly_name} (${date} | ${job.uuid})`,
            value: job.uuid,
          };
        };
        this.jobIds = _.chain(response.body)
          .mapValues(formatter)
          .sortBy(j => j.text.toLowerCase())
          .value();
      })
      .catch((err) => {
        // eslint-disable-next-line no-console
        if (err.status > 0) console.error('Problem', err);
      });
  },
  methods: {
    updateValue(value) {
      this.$emit('update:jobId', value);
    },
  },
};
</script>
