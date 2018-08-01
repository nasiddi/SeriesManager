<template>
  <div>
    <b-form>
      <b-button
        type="reload"
        variant="primary"
        size="lg"
        class="mt-3"
        block
        @click.prevent="reload"
      >Reload</b-button>
      <b-button
        type="sync"
        variant="primary"
        size="lg"
        class="mt-3"
        block
        @click.prevent="sync"
      >Sync</b-button>
      <b-button
        type="batch"
        variant="primary"
        size="lg"
        class="mt-3"
        block
        @click.prevent="batch"
      >BatchSync</b-button>
      <b-button
        type="update"
        variant="primary"
        size="lg"
        class="mt-3"
        block
        @click.prevent="update"
      >Update Series</b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  methods: {
    async reload() {
      let notifLoading = null;
      this.$http.post('jobs/reload')
        .then(notifLoading = this.$snotify.info('Reloading', { timeout: 0 }))
        .then((res) => {
          this.$snotify.remove(notifLoading.id);
          if (res.body === 'failed') {
            this.$snotify.error('Loading failed');
          } else {
            this.$snotify.success(res.body);
          }
        });
    },
    async sync() {
      this.$router.push({
        name: 'sync.prep',
      });
    },
    async update() {
      this.$router.push({
        name: 'update',
      });
    },
    async batch() {
      this.$router.push({
        name: 'batch.prep',
      });
    },
  },
};
</script>
