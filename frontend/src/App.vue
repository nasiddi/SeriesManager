<template>
  <div id="app">

    <vue-snotify/>
    <the-navigation/>

    <b-container
      class="container-first"
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
    title: 'GUI',
    titleTemplate: (titleChunk) => {
      const suffix = 'texploration by siddinad & metzllin';
      return titleChunk ? `${titleChunk} | ${suffix}` : suffix;
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

input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
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
  "e6194b": #e6194b,
  "3cb44b": #3cb44b,
  "ffe119": #ffe119,
  "0082c8": #0082c8,
  "f58231": #f58231,
  "911eb4": #911eb4,
  "46f0f0": #46f0f0,
  "f032e6": #f032e6,
  "d2f53c": #d2f53c,
  "fabebe": #fabebe,
  "008080": #008080,
  "e6beff": #e6beff,
  "aa6e28": #aa6e28,
  "fffac8": #fffac8,
  "800000": #800000,
  "aaffc3": #aaffc3,
  "808000": #808000,
  "ffd8b1": #ffd8b1,
  "000080": #000080,
  "808080": #808080
);

@each $color, $value in $random-colors {
  .badge-#{$color} {
    @include badge-variant($value);
  }
}
</style>
