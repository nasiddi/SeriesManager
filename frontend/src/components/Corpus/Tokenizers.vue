<template>
  <div id="corpus-tokenizers">
    <h2>Tokenizers</h2>
    <b-row>
      <b-col>
        <b-table
          :items="tokenizerOverlapItems"
          hover
          small
        />
      </b-col>
      <b-col>
        <h4>Tokenizer Overlap</h4>
        <bar-chart
          :chart-data="tokenizerChartData"
          :options="tokenizerChartOptions"
          :height="200"/>
      </b-col>
    </b-row>

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
      v-for="(sample, overlap) in tokenizers"
      :key="overlap"
      :header="sample.original"
      :footer="`Difference between the samples: ${formatPercentage(overlap)}`"
      class="my-3"
      body-class="overflow-x">
      <b-table
        :items="formatSampleAsTable(sample)"
        :outlined="false"
        tbody-tr-class="td-no-border td-no-wrap"
        thead-class="d-none"
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
import BarChart from '@/components/Snippets/BarChart';

const _ = require('lodash');

export default {
  components: { BarChart },
  props: {
    tokenizers: {
      type: Object,
      required: true,
    },
    tokenizerOverlap: {
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
    tokenizerChartOptions: {
      legend: {
        display: false,
      },
      scales: {
        yAxes: [
          {
            scaleLabel: {
              display: true,
              labelString: 'Overlap',
            },
            ticks: {
              min: 0,
              max: 1,
              callback(value) {
                return `${value * 100}%`;
              },
            },
          },
        ],
        xAxes: [
          {
            scaleLabel: {
              display: true,
              labelString: 'Tokenizers',
            },
          },
        ],
      },
      tooltips: {
        callbacks: {
          label(a) {
            return `Overlap: ${(a.yLabel * 100).toFixed(2)}%`;
          },
        },
      },
    },
  }),
  computed: {
    tokenizerChartData() {
      const keys = _.keys(this.tokenizerOverlapHumanized);
      return {
        labels: keys,
        datasets: [
          {
            data: _.values(this.tokenizerOverlap),
            backgroundColor: this.colorArrayRandom(keys),
          },
        ],
      };
    },
    tokenizerOverlapHumanized() {
      return _.chain(this.tokenizerOverlap)
        .mapKeys((overlap, tokenizers) => tokenizers.replace('_', ' ↔ '))
        .mapValues(overlap => this.formatPercentage(overlap))
        .value();
    },
    tokenizerOverlapItems() {
      const arr = [];
      _.chain(this.tokenizerOverlapHumanized)
        .forEach((overlap, tokenizers) => {
          arr.push({
            tokenizers,
            overlap,
          });
        })
        .value();
      return arr;
    },
  },
  methods: {
    formatSampleAsTable(sample) {
      const arr = [];
      // eslint-disable-next-line no-param-reassign
      _.chain(sample)
        .pickBy((phrase, tokenizer) => tokenizer !== 'original')
        .forEach((phrase, tokenizer) => {
          const tokens = _.chain(phrase)
            .toPlainObject()
            .mapKeys((x, index) => `token ${index}`)
            .value();
          const el = _.merge({ tokenizer }, tokens);
          // eslint-disable-next-line no-underscore-dangle
          el._cellVariants = _.chain(tokens)
            .mapValues(() => null)
            .merge({ tokenizer: null })
            .value();
          arr.push(el);
        })
        .value();

      const numTokenizers = arr.length;
      _.forEach(arr, (row, i) => {
        const otherRows = _.reject(arr, (value, key) => key === i);
        _.forEach(row, (value, key) => {
          if (key === 'tokenizer') return;
          // eslint-disable-next-line
          const matches =
            _.chain(otherRows)
              .map(o => _.get(o, key))
              .reduce((count, otherValue) => count + (otherValue === value ? 1 : 0), 0)
              .value()
            / (numTokenizers - 1);

          const variant = this.tokenVariant(matches);
          // eslint-disable-next-line no-underscore-dangle
          arr[i]._cellVariants[key] = variant;
          if (this.shouldFilterToken(matches)) {
            if (this.filterEffectSelected === 'de-colorize') {
              // eslint-disable-next-line no-underscore-dangle
              arr[i]._cellVariants[key] = 'default';
            } else if (this.filterEffectSelected === 'hide') {
              // eslint-disable-next-line no-underscore-dangle
              arr[i]._cellVariants[key] = 'hidden';
            }
          }
        });
      });
      return arr;
    },
    tokenVariant(matches) {
      if (matches === 1) {
        return 'success';
      }
      if (matches === 0) {
        return 'danger';
      }
      return 'warning';
    },
    shouldFilterToken(matches) {
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
