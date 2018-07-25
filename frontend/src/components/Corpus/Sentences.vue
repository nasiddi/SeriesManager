<template>
  <div id="corpus-sentences">
    <h2>Sentence Splitting</h2>
    <b-row>
      <b-col>
        <b-form-group>
          <b-form-radio-group
            v-model="filterEffectSelected"
            :options="filterEffects"/>
        </b-form-group>
      </b-col>
      <b-col class="text-right">
        <b-form-group>
          <b-form-radio-group
            v-model="filterSelected"
            :options="filters"/>
        </b-form-group>
      </b-col>
    </b-row>

    <b-card
      v-for="(sample, difference) in sentences"
      :key="difference"
      :header="sample.original"
      :footer="`Difference between the samples: ${Math.floor(difference)} lines`"
      class="my-3">
      <b-table
        :items="formatSampleAsTable(sample)"
        striped
        small>
        <template
          slot="tokenizer"
          slot-scope="data">
          <b-badge variant="info">{{ data.item.tokenizer }}</b-badge>
        </template>
      </b-table>
    </b-card>
  </div>
</template>

<script>
const _ = require('lodash');

export default {
  props: {
    sentences: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    filterSelected: 'all',
    filters: [
      { text: 'all differences', value: 'all' },
      { text: 'non-agreement', value: 'no' },
      { text: 'full agreement', value: 'full' },
    ],
    filterEffectSelected: 'de-colorize',
    filterEffects: [{ text: 'Show', value: 'hide' }, { text: 'Highlight', value: 'de-colorize' }],
  }),
  methods: {
    formatSampleAsTable(sample) {
      const sampleTokenizers = _.chain(sample)
        .pickBy((paragraph, tokenizer) => tokenizer !== 'original')
        .value();

      const rowCount = _.chain(sampleTokenizers)
        .map(x => x.length)
        .max()
        .value();

      const keys = _.chain(sampleTokenizers)
        .keys()
        .zipObject()
        .value();

      const cols = _.times(rowCount, () => keys);
      const arr = [];
      _.chain(cols)
        .mapValues((data, colIndexStr) => {
          const colIndex = _.parseInt(colIndexStr);
          const s = _.chain(data)
            .mapValues((x, tokenizer) => sample[tokenizer][colIndex])
            .value();

          // eslint-disable-next-line no-underscore-dangle
          s._cellVariants = {};
          return s;
        })
        .mapValues((data) => {
          const d = data;
          _.chain(data)
            .pickBy((value, key) => key !== '_cellVariants')
            .each((value, key) => {
              const others = _.chain(data)
                .pickBy((v, k) => k !== '_cellVariants')
                .pickBy((v, k) => k !== key)
                .value();

              // eslint-disable-next-line
              const matches =
                _.chain(others)
                  .reduce((count, otherValue) => count + (otherValue === value ? 1 : 0), 0)
                  .value() / _.size(others);

              // eslint-disable-next-line no-underscore-dangle
              d._cellVariants[key] = this.sentenceVariant(matches);

              if (this.shouldFilterSentence(matches)) {
                if (this.filterEffectSelected === 'de-colorize') {
                  // eslint-disable-next-line no-underscore-dangle
                  d._cellVariants[key] = 'default';
                } else if (this.filterEffectSelected === 'hide') {
                  // eslint-disable-next-line no-underscore-dangle
                  d._cellVariants[key] = 'hidden';
                }
              }
            })
            .value();

          return d;
        })
        .each((value) => {
          arr.push(value);
        })
        .value();
      return arr;
    },
    sentenceVariant(matches) {
      if (matches === 1) {
        return 'success';
      }
      if (matches === 0) {
        return 'danger';
      }
      return 'warning';
    },
    shouldFilterSentence(matches) {
      if (this.filterSelected === 'all') {
        return false;
      }
      if (this.filterSelected === 'full') {
        return !(matches === 1);
      }
      if (this.filterSelected === 'no') {
        return !(matches !== 1);
      }
      return true;
    },
  },
};
</script>
