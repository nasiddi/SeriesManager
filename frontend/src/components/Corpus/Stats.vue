<template>
  <div id="corpus-stats">
    <h2>Stats</h2>
    <b-row>
      <b-col>
        <b-table
          :items="generalStatsItems"
          thead-class="d-none"
          hover
          small
        />
      </b-col>
      <b-col
        v-if="_.size(labels) > 0"
        :cols="8"
      >
        <b-table
          :items="labelItems"
          :fields="labelFields"
          hover
          small
        />
      </b-col>
    </b-row>
    <b-row>
      <b-col
        v-if="_.size(labels) > 0"
        :cols="6">
        <h4>Label distribution</h4>
        <bar-chart
          :chart-data="labelChartData"
          :options="labelChartOptions"
          :height="200"/>
        <span v-if="instances.none">
          {{ instances.none }} instances with no label are not shown.
        </span>
        There are {{ instances.total }} instances in total.
      </b-col>
      <b-col
        v-if="_.size(instances) > 0"
        :cols="6">
        <h4>Instance distribution</h4>
        <pie-chart
          :chart-data="instanceChartData"
          :options="instanceChartOptions"
          :height="200"/>
        <span v-if="instances.none">
          {{ instances.none }} instances with no label are not shown.
        </span>
        There are {{ instances.total }} instances in total.
      </b-col>
    </b-row>
  </div>
</template>

<script>
import BarChart from '@/components/Snippets/BarChart';
import PieChart from '@/components/Snippets/PieChart';

const _ = require('lodash');

export default {
  components: { BarChart, PieChart },
  props: {
    instances: {
      type: Object,
      required: true,
    },
    labels: {
      type: Object,
      required: true,
    },
    rowCount: {
      type: Number,
      required: true,
    },
  },
  data: () => ({
    instanceChartOptions: {
      legend: {
        display: false,
      },
    },
    labelChartOptions: {
      legend: {
        display: false,
      },
      scales: {
        yAxes: [
          {
            ticks: {
              min: 0,
            },
          },
        ],
      },
    },
    labelFields: [
      { key: 'label', label: 'Label' },
      { key: 'type', label: 'Type' },
      { key: 'count', label: 'Texts with label' },
      { key: 'chars', label: 'characters (min|avg|max)' },
      { key: 'words', label: 'words (min|avg|max)' },
    ],
  }),
  computed: {
    generalStatsItems() {
      return [
        { key: 'Number of texts', value: this.rowCount },
        {
          key: 'Characters (min|avg|max)',
          value: this.getTextLengthForLabel('total', 'char_count'),
        },
        {
          key: 'Words (min|avg|max)',
          value: this.getTextLengthForLabel('total', 'word_count'),
        },
      ];
    },
    instanceChartData() {
      return {
        labels: _.chain(this.realInstances)
          .keys()
          .map(l => l.split('\u035b').join(', '))
          .value(),
        datasets: [
          {
            data: _.values(this.realInstances),
            backgroundColor: this.colorArrayRandom(_.keys(this.realInstances)),
          },
        ],
      };
    },
    labelChartData() {
      const labels = _.chain(this.labels)
        .pickBy((data, label) => label !== 'total' && label !== 'none')
        .orderBy(['count'], ['desc'])
        .value();

      const keysForColoring = _.chain(labels)
        .map((x) => {
          if (x.type === 'binary') {
            return x.label;
          }
          return x.value;
        })
        .value();

      const keys = _.chain(labels)
        .map(x => x.name)
        .value();

      return {
        labels: keys,
        datasets: [
          {
            data: _.chain(labels)
              .map(label => label.count)
              .value(),
            backgroundColor: this.colorArrayRandom(keysForColoring),
          },
        ],
      };
    },
    realInstances() {
      return _.chain(this.instances)
        .pickBy((count, inst) => inst !== 'total' && inst !== 'none')
        .value();
    },
    labelItems() {
      const arr = [];
      _.chain(this.labels)
        .forEach((details, label) => {
          if (label === 'total') {
            return;
          }
          arr.push({
            label,
            type: details.type,
            count: details.count,
            chars: this.getTextLengthForLabel(label, 'char_count'),
            words: this.getTextLengthForLabel(label, 'word_count'),
          });
        })
        .value();
      return arr;
    },
  },
  methods: {
    getTextLengthForLabel(label, type) {
      const avg = _.defaultTo(
        _.isObject(this.labels[label]) ? this.labels[label][type].average : undefined,
        0,
      ).toFixed(0);
      const min = _.defaultTo(
        _.isObject(this.labels[label]) ? this.labels[label][type].min : undefined,
        0,
      ).toFixed(0);
      const max = _.defaultTo(
        _.isObject(this.labels[label]) ? this.labels[label][type].max : undefined,
        0,
      ).toFixed(0);

      return `${min} | ${avg} | ${max}`;
    },
  },
};
</script>
