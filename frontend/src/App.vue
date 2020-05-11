/*eslint max-len: ["error", { "ignoreStrings": true }]*/
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
    title: 'Atlantis',
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

body {
  background-color: #292929;
  color: #d6d6d6;
}

.card {
  color: #d6d6d6;
  background-color: #353535;
}

.list-group-item {
  color: #d6d6d6;
  background-color: #3f3f3f;
}

.list-group-item-success {
    color: #155724;
    background-color: #c3e6cb;
}

.list-group-item-secondary {
    color: #383d41;
    background-color: #d6d8db;
}

.list-group-item-danger {
    color: #721c24;
    background-color: #f5c6cb;
}


.custom-select {
  color: #d6d6d6;
  background-color: #353535;
}

.custom-select:focus {
  color: #d6d6d6;
  background-color: #353535;
}

.custom-select:after {
 border-color: #d6d6d6;
}

.form-control {
  color: #d6d6d6;
  background-color: #353535;
}

.form-control:focus {
  color: #d6d6d6;
  background-color: #353535;
}

.form-control:disabled {
  color: #d6d6d6;
  background-color: #8a8a8a;
}

.custom-select::-ms-expand {
  display: none;
}

.custom-select {
  background: url(http://bigastro.unige.ch/concrete/images/icons/arrow_down.png) no-repeat right;
  border: 1px solid grey;
  border-radius: 5px;
  overflow: hidden;
  background-size: 11px 6px;
  background-position: right 5px center;
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
