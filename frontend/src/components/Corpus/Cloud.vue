<template>
  <div id="corpus-cloud">
    <h2>Word cloud</h2><b-row>
      <b-col>
        <wordcloud
          :data="tokensCloud"
          :rotate="{ from: -90, to: 90, numOfOrientation: 8 }"
          :word-click="wordClick"
          name-key="token"
          value-key="count"
        />
      </b-col>
      <b-col cols="3">
        <b-card
          :footer="filterStatus"
          header="Labels"
        >
          <b-form-group>
            <b-form-radio-group
              v-model="labelsMetaModel"
              :options="labelsMetaOptions"
              stacked
            />
            <hr>
            or only tokens which occur with <em>all</em> of the following labels:
            <b-form-checkbox-group
              v-model="labelsSelected"
              :options="labelsCheckboxes"
              stacked
            />
          </b-form-group>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>

<script>
// https://github.com/feifang/vue-wordcloud
import wordcloud from 'vue-wordcloud';

const _ = require('lodash');

export default {
  components: {
    wordcloud,
  },
  props: {
    labels: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    labelsMetaOptions: [{ value: 'all', text: 'All labels' }],
    labelsSelected: [],
  }),
  computed: {
    tokensByLabels() {
      return _.chain(this.labels)
        .mapValues(label => label.tokens)
        .value();
    },
    labelsMetaModel: {
      get() {
        return _.size(this.labelsSelected) === 0 ? 'all' : false;
      },
      set(newValue) {
        if (newValue === 'all') {
          this.labelsSelected = [];
        }
      },
    },
    labelsCheckboxes() {
      const arr = [];
      _.chain(this.labels)
        .pickBy((x, label) => label !== 'total')
        .forEach((data, label) => {
          const sum = data.count;
          arr.push({
            text: `${label}<br><small>${sum} tokens</small>`,
            value: label,
          });
        })
        .value();
      return arr;
    },
    activeTokens() {
      if (this.labelsSelected.length === 0) {
        return this.tokensByLabels.total;
      }

      return _.chain(this.tokensByLabels)
        .pick(this.labelsSelected)
        .reduce(_.merge)
        .value();
    },
    filterStatus() {
      const activeLabels = _.size(this.labelsSelected);
      const totalLabels = _.size(this.labels) - 1;

      return `${activeLabels} / ${totalLabels}`;
    },
    tokensCloud() {
      const arr = [];
      _.chain(this.activeTokens)
        .forEach((token, count) => {
          arr.push({
            token,
            count,
          });
        })
        .value();
      return arr;
    },
  },
  methods: {
    wordClick(word) {
      this.$store.commit('searchQuery', word);
    },
  },
};
</script>
