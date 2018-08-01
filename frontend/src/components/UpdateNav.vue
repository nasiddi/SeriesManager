<template>
  <div
    class="sticky-top">
    <b-nav
      vertical>
      <b-nav-item
        v-for="r in refs"
        :key="r"
        :href="r">{{ r.slice(1, 2) }}</b-nav-item>
  </b-nav></div>
</template>

<script>

export default {
  data: () => ({
    refs: [
      '##',
      '#A',
      '#B',
      '#C',
      '#D',
      '#E',
      '#F',
      '#G',
      '#H',
      '#I',
      '#J',
      '#K',
      '#L',
      '#M',
      '#N',
      '#O',
      '#P',
      '#Q',
      '#R',
      '#S',
      '#T',
      '#U',
      '#V',
      '#W',
      '#X',
      '#Y',
      '#Z',
    ],
  }),
};

</script>
