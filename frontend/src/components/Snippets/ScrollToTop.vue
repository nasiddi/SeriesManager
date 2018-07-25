<template>
  <b-button
    v-if="showButton"
    key="show-button"
    class="cursor-pointer scroll-to-top"
    variant="outline-secondary"
    size="sm"
    @click="scrollToTop"
  >
    <font-awesome-icon icon="chevron-up" />
  </b-button>
</template>

<script>
export default {
  data: () => ({
    showButton: false,
  }),
  created() {
    setInterval(() => this.checkShowButton(), 500);
  },
  methods: {
    scrollToTop() {
      window.scrollTo(0, 0);
      this.checkShowButton();
    },
    checkShowButton() {
      const offset = 100;
      const tallEnough = window.innerHeight + offset < document.body.clientHeight;
      const getScrollPosition = () => document.documentElement.scrollTop || 0;
      const scrolledDown = getScrollPosition() > offset;
      this.showButton = tallEnough && scrolledDown;
    },
  },
};
</script>

<style scoped>
.scroll-to-top {
  position: fixed;
  bottom: 10px;
  right: 10px;
}
</style>
