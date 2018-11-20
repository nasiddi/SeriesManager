<template>
  <div/>
</template>

<script>
export default {
  metaInfo: {
    title: 'About',
  },
  created() {
    this.reroute();
  },
  methods: {
    async reroute() {
      this.$router.push({
        name: 'filetree',
        params: this.$route.params,
      });
    },
  },
};
</script>
