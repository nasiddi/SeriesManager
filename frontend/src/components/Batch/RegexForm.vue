<template>
  <div>
    <b-row class="mb-2">
      <b-col
        sm="3"
        class="px-2">
        <b-input
          v-model.lazy="regex.regex"
          class="mt-2"
          placeholder="Regex" />
      </b-col>
      <b-col
        sm="3"
        align="center"
        class="px-2 py-3 text-xs-center">
        <text-highlight
          v-if="regex.matches.length !== 0"
          :queries="regex.sxe"
          class="mt-2 text-xs-center">
          {{ regex.matches[0] }}
        </text-highlight>
      </b-col>
      <b-col
        sm
        class="px-2">
        <b-input-group
          :style="{width: '100%'}"
          left="@"
          class="mt-2">
          <b-input
            v-model.number="regex.s_start"
            type="number"
            placeholder="S" />
          <b-input
            v-model.number="regex.s_end"
            type="number"
            placeholder="S" />
        </b-input-group>
      </b-col>
      <b-col
        sm
        class="px-2">
        <b-input-group
          :style="{width: '100%'}"
          left="@"
          class="mt-2">
          <b-input
            v-model.number="regex.e_start"
            type="number"
            placeholder="E" />
          <b-input
            v-model.number="regex.e_end"
            type="number"
            placeholder="E" />
        </b-input-group>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import TextHighlight from 'vue-text-highlight';

export default {
  components: {
    TextHighlight,
  },
  props: {
    regex: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
  }),
  watch: {
  },
  created() {
  },
  mounted() {
  },
  methods: {
  },
};
</script>
