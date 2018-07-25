<template>
  <div >
    <h2>Columns</h2>
    <div class="overflow-x">
      <b-table
        :items="items"
        tbody-tr-class="td-no-wrap"
        small
        stacked
      >
        <template
          slot="sample"
          slot-scope="data">
          <span v-html="data.value"/>
        </template>
      </b-table>
    </div>
  </div>
</template>

<script>
const _ = require('lodash');

export default {
  data: () => ({
    project: {},
    analysis: {},
    items: [],
    timeoutId: null,
    refreshTimeout: 1000,
    lastHash: null,
  }),
  mounted() {
    this.refreshData();
    this.refresh();
  },
  destroyed() {
    window.clearTimeout(this.timeoutId);
  },
  methods: {
    refresh() {
      if (!this.project || this.project.is_corpus_analyzed !== 1) {
        this.timeoutId = setTimeout(() => {
          const url = `projects/${
            this.$router.currentRoute.params.project_uuid
          }/corpus_analysis/check`;
          this.$http.get(url).then((res) => {
            const hash = res.headers.get('X-File-Hash');
            if (hash !== this.lastHash) {
              this.lastHash = hash;
              this.refreshData();
            }
          });
          this.refresh();
        }, this.refreshTimeout);
      }
    },
    refreshData() {
      this.$http
        .get(`projects/${this.$router.currentRoute.params.project_uuid}`)
        .then((resProject) => {
          this.project = resProject.body;

          const url = `projects/${this.$router.currentRoute.params.project_uuid}/corpus_analysis`;
          this.$http.get(url).then((resAnalysis) => {
            this.analysis = resAnalysis.body;

            const preview = this.analysis.columns;

            this.items = _.chain(preview)
              .map(data => ({
                column: data.name,
                type: data.type,
                sample: data.preview.join('<br>'),
              }))
              .value();
          });
        });
    },
  },
};
</script>
