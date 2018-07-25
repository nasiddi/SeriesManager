<template>
  <div class="my-3">
    <b-row class="my-2">
      <b-col>
        <b-button
          :href="getSetDownloadUrl('complete')"
          size="sm"
          variant="outline-secondary">
          <font-awesome-icon icon="download"/> Download comparison
        </b-button>
      </b-col>
    </b-row>
    <b-row>
      <b-col
        v-for="(table, i) in tables"
        v-if="table.items.length > 0"
        :key="i"
      >
        <b-table
          :items="table.items"
          :fields="table.fields"
          foot-clone
        >
          <template
            slot="FOOT_set"
            slot-scope="data">
            Total
          </template>
          <template
            v-for="label in table.sums"
            slot-scope="data"
            :slot="`FOOT_${label}`">
            <span
              v-if="_.has(classifierComparison, 'labels')"
              :key="label">
              {{ classifierComparison.labels[label] }}
            </span>
            <span
              v-else
              :key="label">
              {{ _.chain(table.items).map(i=>i.total).sum().value() }}
            </span>
          </template>
        </b-table>
      </b-col>
    </b-row>
    <b-card
      v-for="sample in samples"
      v-if="_.size(sample.items) > 0"
      :key="sample.key"
      :title="getSetTitle(sample.key)"
      :sub-title="getSetSubTitle(sample.key)"
      body-class="overflow-x"
      class="my-3"
    >
      <span
        slot="footer"
        v-html="getSetFooter(sample.key)"/>
      <b-table
        :items="sample.items"
        :fields="sample.fields"
        tbody-tr-class="td-no-wrap"
        small>
        <template
          slot="correct"
          slot-scope="data">
          <b-badge
            v-if="data.item.correct"
            :variant="color(data.item.correct)">
            {{ data.value }}
          </b-badge>
        </template>
        <template
          v-for="(col, coli) in cols"
          slot-scope="data"
          :slot="col">
          <span
            v-b-tooltip.hover
            :key="coli"
            :title=" data.value.value"
          >
            <b-badge
              v-if="data.value.match === true"
              :variant="color(data.value.value)">
              <font-awesome-icon
                icon="check"
                fixed-width/>
            </b-badge>
            <b-badge
              v-if="data.value.match === false"
              :variant="color(data.value.value)">
              <font-awesome-icon
                icon="exclamation"
                fixed-width/>
            </b-badge>
            <b-badge
              v-if="data.value.match === undefined"
              :variant="color(data.value.value)">
              {{ data.value.value }}
            </b-badge>
          </span>
        </template>
      </b-table>
      <b-button
        :href="getSetDownloadUrl(sample.key)"
        size="sm"
        variant="outline-secondary">
        <font-awesome-icon icon="download"/> Download complete set
      </b-button>
    </b-card>
  </div>
</template>

<script>
const _ = require('lodash');

export default {
  props: {
    uuid: {
      type: String,
      required: true,
    },
    endpoint: {
      type: String,
      required: true,
    },
    classifierComparison: {
      type: Object,
      required: true,
    },
    processes: {
      type: Array,
      required: true,
    },
  },
  data: () => ({}),
  computed: {
    tables() {
      return _.chain([['all_false', 'all_true', 'rest'], ['agree', 'disagree']])
        .map((fields) => {
          const items = _.chain(this.classifierComparison)
            .pick(fields)
            .mapValues(set => set.labels)
            .mapValues((data, set) => {
              const d = data;
              d.set = this.getSetTitle(set);
              return d;
            })
            .values()
            .value();
          const labels = _.chain(items)
            .first()
            .keys()
            .reject(k => _.includes(['total', 'set'], k))
            .value();

          const data = {
            items,
            fields: _.concat('set', labels, 'total'),
            sums: _.concat(labels, 'total'),
          };
          return data;
        })
        .value();
    },
    cols() {
      return _.chain(this.processes)
        .map(p => p.id)
        .value();
    },
    samples() {
      const fieldsStart = [
        {
          key: 'correct',
          label: 'Correct label',
        },
      ];
      const fieldsEnd = [
        {
          key: 'text',
          label: 'Text',
        },
      ];

      const fieldsCols = _.chain(this.classifierComparison.columnMapping)
        .filter((col) => {
          if (col === 'correct' || col === 'text') return false;

          return true;
        })
        .sortBy(v => parseInt(v, 10))
        .map((col) => {
          const procId = parseInt(col, 10);
          const proc = _.chain(this.processes)
            .filter(p => p.id === procId)
            .first()
            .value();

          return {
            key: col,
            label: proc.friendly_name,
          };
        })
        .value();

      const order = ['all_false', 'disagree', 'all_true', 'agree'];
      const data = _.chain(this.classifierComparison)
        .pick(['agree', 'all_false', 'all_true', 'disagree'])
        .pickBy(set => set.samples.length > 0)
        .mapValues(set => set.samples)
        .mapValues((set) => {
          const objectified = _.chain(set)
            .map((sample) => {
              const zipped = _.zipObject(this.classifierComparison.columnMapping, sample);
              return zipped;
            })
            .map((sample) => {
              const mapped = _.chain(sample)
                .mapValues((value, key) => {
                  if (key === 'correct' || key === 'text') return value;
                  return {
                    match: sample.correct ? value === sample.correct : undefined,
                    value,
                  };
                })
                .value();
              return mapped;
            })
            .value();
          return objectified;
        })
        .mapValues((v, set) => ({
          items: v,
          fields: _.concat(
            this.classifierComparison.columnMapping[0] === 'correct' ? fieldsStart : [],
            set !== 'all_true' ? fieldsCols : [],
            fieldsEnd,
          ),
          key: set,
        }))
        .values()
        .sortBy(set => order.indexOf(set.key))
        .value();

      return data;
    },
  },
  methods: {
    getSetTitle(set) {
      const texts = {
        agree: 'Complete agreement',
        disagree: 'Disagreement',
        all_true: 'All correct',
        all_false: 'All incorrect',
        rest: 'Rest',
      };
      return texts[set];
    },
    getSetSubTitle(set) {
      const texts = {
        agree: 'All classifiers agree on labels',
        disagree: 'Classifiers disagree on labels',
        all_true: 'Classified correctly by all classifiers',
        all_false: 'Classified incorrectly by all classifiers',
      };
      return texts[set];
    },
    getSetFooter(set) {
      const setLabels = this.classifierComparison[set].labels;

      const modifier = {
        agree: 'agree',
        disagree: 'disagree',
        all_true: 'are correct',
        all_false: 'are wrong',
      };

      if (_.has(this.classifierComparison, 'labels')) {
        const { labels } = this.classifierComparison;

        const ratioTotal = setLabels.total / labels.total;
        const percentageTotal = (ratioTotal * 100).toFixed(2);

        const texts = _.chain(setLabels)
          .pickBy((setValue, label) => label !== 'total' && label !== 'set')
          .map((setValue, label) => {
            const ratio = setValue / labels[label];
            const percentage = (ratio * 100).toFixed(2);
            const text = `${label}: ${setValue} / ${labels[label]} (${percentage}%)`;
            return text;
          })
          .value();

        const labelsText = texts.join(' | ');

        const text = `All classifiers ${modifier[set]} for <strong>${setLabels.total} out of ${
          labels.total
        }</strong> texts (${percentageTotal}%).<br>${labelsText}`;

        return text;
      }

      const texts = _.chain(setLabels)
        .pickBy((setValue, label) => label !== 'total' && label !== 'set')
        .map((setValue, label) => {
          const text = `${label}: ${setValue}`;
          return text;
        })
        .value();

      const labelsText = texts.join(' | ');

      const text = `All classifiers ${modifier[set]} for <strong>${
        setLabels.total
      }</strong> texts.<br>${labelsText}`;

      return text;
    },
    getSetDownloadUrl(set) {
      return `${this.$globalData.rootUrl}${this.endpoint}/${this.uuid}/download_comparison/${set}`;
    },
    color(str) {
      return this.colorArrayRandom([str])[0].substr(1);
    },
  },
};
</script>


<style>
.overflow-x {
  overflow-x: scroll;
}

.td-no-border td {
  border: none;
}

.td-no-wrap td {
  white-space: nowrap;
}
</style>
