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
      <b-button
        type="stats"
        variant="primary"
        size="lg"
        class="mt-3"
        block
        @click.prevent="backup"
      >BackUp</b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  methods: {
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
    async backup() {
      this.$router.push({
        name: 'backup',
      });
    },
  },
};
</script>
