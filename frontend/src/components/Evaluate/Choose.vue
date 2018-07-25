<template>
  <div>
    <h1>Evaluate</h1>

    <b-form @submit.prevent="submit">
      <b-form-group
        id="input-jobid"
        label="Enter the job ID you'd like to evaluate on the server:"
        label-for="input-jobid"
      >
        <job-dropdown :job-id.sync="jobId"/>
      </b-form-group>
      <b-button
        type="submit"
        variant="primary"
        size="lg"
        block
      >Evaluate</b-button>
    </b-form>
  </div>
</template>


<script>
import JobDropdown from '@/components/Snippets/JobDropdown';

export default {
  components: { JobDropdown },
  data: () => ({
    jobId: null,
  }),
  metaInfo() {
    return {
      title: 'Choose a job to evaluate',
    };
  },
  methods: {
    submit() {
      this.$router.push({
        name: 'evaluate.job',
        params: { job_uuid: this.jobId },
      });
    },
  },
};
</script>
