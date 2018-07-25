<template>
  <div>
    <b-form>
      <b-button
        type="reload"
        variant="primary"
        size="lg"
        block
        @click.prevent="reload"
      >Reload</b-button>
      <b-button
        type="sync"
        variant="primary"
        size="lg"
        block
        @click.prevent="sync"
      >Sync</b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  methods: {
    async reload() {
      this.$http.post('jobs/reload')
        .then(this.$snotify.info('loading'))
        .then((res) => {
          if (res.body === 'failed') {
            this.$snotify.error('Loading failed');
          } else {
            this.$snotify.success(res.body);
          }
        });
    },
    async sync() {
      this.$router.push({
        name: 'sync',
      });
    },
  },
};
</script>
