<template>
  <div id="app">
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0">
    <vue-snotify/>
    <the-navigation/>

    <b-container
      class="container-fluid"
      fluid
    >
      <b-row>
        <b-col :cols="1">
          <router-view name="sidebarLeft"/>
        </b-col>

        <b-col :cols="10">
          <router-view id="routerview-main"/>
        </b-col>

        <b-col :cols="1">
          <router-view name="sidebarRight"/>
        </b-col>
      </b-row>
    </b-container>


    <br>
    <hr>

    <the-footer class="container"/>
    <scroll-to-top/>
  </div>
</template>

<script>
import TheNavigation from '@/components/Snippets/TheNavigation';
import TheFooter from '@/components/Snippets/TheFooter';
import ScrollToTop from '@/components/Snippets/ScrollToTop';

export default {
  components: { TheNavigation, TheFooter, ScrollToTop },
  created() {
    this.loadSettings();
  },
  metaInfo: {
    title: 'Series Manager',
    titleTemplate: (titleChunk) => {
      const suffix = '';
      return titleChunk ? `${titleChunk} ${suffix}` : suffix;
    },
  },
};
</script>

<style>
.container-first {
  padding-top: 2rem;
}

.cursor-pointer {
  cursor: pointer;
}

.link-as-text {
  color: #212529;
}

.link-as-text:hover,
.link-as-text:focus {
  text-decoration: none;
}

.overflow-x {
  overflow-x: scroll;
}

input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.td-no-border td {
  border: none;
}

.td-no-wrap td {
  white-space: nowrap;
}

.table-hidden {
  display: none;
}
</style>

<style lang="scss">
@import "node_modules/bootstrap/scss/functions";
@import "node_modules/bootstrap/scss/variables";
@import "node_modules/bootstrap/scss/mixins";

$random-colors: (
  "001f3f": #001f3f,
  "0074D9": #0074d9,
  "7FDBFF": #7fdbff,
  "39CCCC": #39cccc,
  "3D9970": #3d9970,
  "2ECC40": #2ecc40,
  "01FF70": #01ff70,
  "FFDC00": #ffdc00,
  "FF851B": #ff851b,
  "FF4136": #ff4136,
  "85144b": #85144b,
  "F012BE": #f012be,
  "B10DC9": #b10dc9
);

@each $color, $value in $random-colors {
  .badge-#{$color} {
    @include badge-variant($value);
  }
}
</style>
