<template>
  <div>
    <b-form>
      <b-button
        type="sync"
        variant="primary"
        size="lg"
        class="mt-3"
        block
        @click.prevent="sync"
      >Sync</b-button>
      <b-button
        type="update"
        variant="primary"
        size="lg"
        class="mt-3"
        block
        @click.prevent="files"
      >FileTree</b-button>
      <b-button
        type="update"
        variant="primary"
        size="lg"
        class="mt-3"
        block
        @click.prevent="update"
      >Update Series</b-button>
      <b-button
        type="stats"
        variant="primary"
        size="lg"
        class="mt-3"
        block
        @click.prevent="stats"
      >Statistics</b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  methods: {
    async reload() {
      let notifLoading = null;
      this.$http
        .post('jobs/reload')
        .then((notifLoading = this.$snotify.info('Reloading', { timeout: 0 })))
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
    async stats() {
      this.$router.push({
        name: 'stats',
      });
    },
    async update() {
      this.$router.push({
        name: 'update',
      });
    },
    async files() {
      this.$router.push({
        name: 'filetree',
      });
    },
  },
};
</script>
