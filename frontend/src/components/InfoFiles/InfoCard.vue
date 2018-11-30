<template>
  <div
    v-if="e.length !== 0">
    <b-card
      no-body
      class="px-3 pt-1 pb-2 mt-2">
      <b-row>
        <b-col
          class="px-1 mt-1"
          sm="2"
          order="3"
          order-md="1">
          <b-button
            :pressed.sync="e.delete"
            :variant="'outline-danger'"
            :style="{width: '100%'}"
          >Delete</b-button>
        </b-col>
        <b-col
          :sm="e.origin.length > 0 ? 5 : 10"
          class="px-1 mt-1"
          order="2"
          order-md="2">
          <b-input
            v-model="e.text"
            disabled/>
        </b-col>
        <b-col
          v-if="e.origin.length > 0"
          class="px-1 mt-1"
          sm="5"
          order="1"
          order-md="3">
          <b-input
            v-model="e.origin"
            disabled/>
        </b-col>
      </b-row>
    </b-card>
  </div>
</template>

<script>


// const _ = require('lodash');


export default {
  components: {
  },
  props: {
    e: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
  }),
  computed: {},
  watch: {},
  methods: {},
};
</script>
