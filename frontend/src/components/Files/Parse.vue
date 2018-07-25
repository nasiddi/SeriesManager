<template>
  <div>
    <h1>Parse {{ file.friendly_name }}</h1>
    <b-form
      @submit.prevent="submit">
      <b-row v-if="!analyzed">
        <b-col>
          <b-card
            header="Contents">
            <b-form-group>
              <b-form-checkbox
                v-model="header"
                :value="true"
                :unchecked-value="false">Header row</b-form-checkbox>
            </b-form-group>
            <b-form-group>
              <b-form-checkbox
                v-model="smartHeader"
                :value="true"
                :unchecked-value="false">
                Smart columns</b-form-checkbox>
            </b-form-group>
          </b-card>
        </b-col>
        <b-col cols="8">
          <b-card header="CSV Parsing">
            <b-form-group>
              <b-form-checkbox
                v-model="smartCsv"
                :value="true"
                :unchecked-value="false">
                Smart CSV<br>
              </b-form-checkbox>
            </b-form-group>
            <b-row v-if="!smartCsv">
              <b-col>
                <b-form-group label="Column delimiter:">
                  <b-form-radio-group
                    v-model="delimiterSelected"
                    :options="delimiters"
                    stacked
                  />
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group label="Quote character:">
                  <b-form-radio-group
                    v-model="quoteCharSelected"
                    :options="quotes"
                    stacked
                  />
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group label="Escape character:">
                  <b-form-radio-group
                    v-model="escapeCharSelected"
                    :options="escapes"
                    stacked
                  />
                </b-form-group>
              </b-col>
            </b-row>
          </b-card>
        </b-col>
      </b-row>

      <b-row class="mt-3">
        <b-col v-if="!analyzed">
          <b-button
            :disabled="hasPendingRequest"
            variant="primary"
            type="submit"
            block
          >Guess CSV format</b-button>
        </b-col>
        <b-col
          v-if="!analyzed"
          cols="3">
          <b-button
            variant="danger"
            block
            @click="reset"
          >Reset options</b-button>
        </b-col>
      </b-row>

    </b-form>

    <b-form
      @submit.prevent="save">
      <div v-if="analyzed">
        <hr>
        <b-row>
          <b-col>
            <h3>Columns</h3>

            <b-row v-if="!isColumnMappingComplete">
              <b-col>
                <hr>
              </b-col>
            </b-row>
            <b-row v-if="!isColumnMappingComplete">
              <b-col>
                <b-button
                  variant="secondary"
                  block
                  @click="setRemainingColumnsTo('label')"
                >Assume non-mapped columns to be labels</b-button>
              </b-col>
              <b-col>
                <b-button
                  variant="secondary"
                  block
                  @click="setRemainingColumnsTo('ignore')"
                >Ignore non-mapped columns</b-button>
              </b-col>
              <hr>
            </b-row>
            <b-row v-if="!isColumnMappingComplete">
              <b-col>
                <hr>
              </b-col>
            </b-row>
            <b-row v-if="!columnMappingHasText">
              <b-col>
                <hr>
                <b-alert
                  variant="warning"
                  show>
                  At least one column has to be of type <code>text</code>
                </b-alert>
                <hr>
              </b-col>
            </b-row>
            <b-row>
              <b-col cols="7">
                <h4>Column type</h4><br>
              </b-col>
              <b-col>
                <h4>Preview of column</h4><br>
              </b-col>
            </b-row>

            <b-row
              v-for="col in analysis.columns"
              :key="col"
            >
              <b-col :cols="7">
                <b-form-group
                  :label="col"
                  description="Please select the type for this column"
                  horizontal
                >
                  <b-form-select
                    v-model="analysis.columnMapping[col]"
                    :options="columnTypesArray"
                    :state="Boolean(analysis.columnMapping[col])"
                  />
                </b-form-group>
              </b-col>
              <b-col class="overflow-x">
                <b-table
                  :items="getColumnPreview(col)"
                  thead-class="d-none"
                  tbody-tr-class="td-no-border td-no-wrap"
                  bordered
                  striped
                  hover
                  small/>
              </b-col>
            </b-row>

          </b-col>
        </b-row>
        <b-row>
          <b-col >
            <b-button
              :disabled="!isSaveable || hasPendingRequest"
              variant="primary"
              block
              type="submit"
            >Save CSV and columns</b-button>
          </b-col>
          <b-col
            cols="3">
            <b-button
              variant="danger"
              block
              @click="reset"
            >Start over</b-button>
          </b-col>
        </b-row>
      </div>
    </b-form>

    <upload-analysis-results
      v-if="analyzed"
      :analysis="analysis"/>
  </div>
</template>

<script>
import UploadAnalysisResults from './ParseResults';

const _ = require('lodash');

export default {
  components: { UploadAnalysisResults },
  data: () => ({
    file: {},
    analyzed: false,
    analysis: {},
    header: false,
    smartCsv: false,
    smartHeader: false,
    delimiters: [],
    delimiterSelected: '',
    escapes: [],
    escapeCharSelected: '"',
    quotes: [],
    quoteCharSelected: '"',
    columnTypesArray: [],
    hasPendingRequest: false,
  }),
  computed: {
    isColumnMappingComplete() {
      return (
        _.size(this.analysis.columns) === _.size(_.pickBy(this.analysis.columnMapping, _.identity))
      );
    },
    columnMappingHasText() {
      const textCols = _.chain(this.analysis.columnMapping)
        .pickBy(type => type === 'text')
        .size()
        .value();
      return textCols >= 1;
    },
    isSaveable() {
      return this.isColumnMappingComplete && this.columnMappingHasText;
    },
  },
  created() {
    this.initSettings();
    this.$eventHub.$on('settings-update', this.initSettings);

    this.$http.get(`files/${this.$router.currentRoute.params.file_uuid}`).then((res) => {
      this.file = res.body;
    });

    const formatOption = (opt) => {
      if (opt === '') return '(none)';
      if (opt === '\t') return '(tab)';
      return opt;
    };

    this.$http.get('files/parse/options').then((res) => {
      this.delimiters = _.chain(res.body.delimiters)
        .map(v => ({ value: v, text: formatOption(v) }))
        .value();

      this.quotes = _.chain(res.body.quotes)
        .map(v => ({ value: v, text: formatOption(v) }))
        .value();

      this.escapes = _.chain(res.body.escapes)
        .map(v => ({ value: v, text: formatOption(v) }))
        .value();

      this.columnTypesArray = _.chain(res.body.columnTypes)
        .map((v, k) => ({ value: k, text: v }))
        .value();
    });
  },
  mounted() {
    this.resetAnalysisResults();
  },
  beforeDestroy() {
    this.$eventHub.$off('settings-update');
  },
  methods: {
    initSettings() {
      this.header = this.$store.getters.setting('parse.header', true);
      this.smartCsv = this.$store.getters.setting('parse.smartCsv', true);
      this.smartHeader = this.$store.getters.setting('parse.smartHeader', true);
    },
    resetAnalysisResults() {
      this.analyzed = false;
      this.analysis = {
        errorCount: null,
        errorLines: null,
        columns: [],
        columnMapping: {},
        rowCount: null,
        rowLimit: this.$store.getters.setting('parse.previewLines', true),
        rowTable: [],
        hasHeaders: null,
      };
    },
    reset() {
      this.analyzed = false;
      this.hasPendingRequest = false;
    },
    submit() {
      this.resetAnalysisResults();
      this.analyzed = false;
      this.hasPendingRequest = true;
      this.$http
        .post(`files/${this.$router.currentRoute.params.file_uuid}/analyze`, {
          header: JSON.stringify(this.header),
          smartHeader: JSON.stringify(this.smartHeader),
          smartCsv: JSON.stringify(this.smartCsv),
          parseOptions: JSON.stringify({
            delimiter: this.delimiterSelected,
            quoteChar: this.quoteCharSelected,
            escapeChar: this.escapeCharSelected,
          }),
        })
        .then(
          (res) => {
            const csv = res.body.analysis;

            this.analysis.errorCount = csv.errors.length;
            this.analysis.rowCount = _.size(csv.data);
            this.analysis.rowTable = _.take(csv.data, this.analysis.rowLimit);

            this.analysis.columns = _.keys(this.analysis.rowTable[0]);
            this.analysis.columnMapping = _.zipObject(
              this.analysis.columns,
              _.map(this.analysis.columns, col => res.body.guessedHeaders[col]),
            );

            this.analysis.hasHeaders = this.header;

            this.delimiterSelected = res.body.options.delimiter;
            this.quoteCharSelected = res.body.options.quoteChar;
            this.escapeCharSelected = res.body.options.escapeChar;

            if (csv.errors.length > 0) {
              this.$snotify.warning('Finished analysis with errors');
              this.analysis.errorLines = this.formatAnalysisErrors(csv.errors);
            } else {
              this.$snotify.success('Finished analysis without errors');
            }

            this.analyzed = true;
          },
          () => {
            this.$snotify.error('Parsing failed');
          },
        )
        .then(() => {
          this.hasPendingRequest = false;
        });
    },
    save() {
      this.hasPendingRequest = true;
      const notifSaving = this.$snotify.info('Saving... This might take a while.', {
        timeout: 0,
      });
      const columnMappingIndexed = [];
      _.forEach(this.analysis.columns, (col) => {
        const colMap = _.get(this.analysis.columnMapping, col, null);
        columnMappingIndexed.push(colMap);
      });

      this.$http
        .post(`files/${this.$router.currentRoute.params.file_uuid}/save`, {
          config: JSON.stringify({
            columnMapping: columnMappingIndexed,
            header: this.analysis.hasHeaders ? 0 : -1,
          }),
          parseOptions: JSON.stringify({
            delimiter: this.delimiterSelected,
            quoteChar: this.quoteCharSelected,
            escapeChar: this.escapeCharSelected,
          }),
        })
        .then(
          (res) => {
            if (res.body.errors.length > 0) {
              this.$snotify.warning('Saved with errors!');
              _.chain(this.formatAnalysisErrors(res.body.errors))
                .each((err) => {
                  this.$snotify.warning(err);
                })
                .value();
            } else {
              this.$snotify.success('Saved!');
            }

            this.$router.push({ name: 'files.index' });
          },
          () => {
            this.$snotify.error('Could not save on server');
          },
        )
        .then(() => {
          this.hasPendingRequest = false;
          this.$snotify.remove(notifSaving.id);
        });
    },
    formatAnalysisErrors(errors) {
      return (
        _.chain(errors)
          .toPlainObject()
          .groupBy(err => `${err.type}/${err.code} ${err.message}`)
          /* eslint-disable indent */
          .mapValues(errs => _.chain(errs)
              .map('row')
              .uniq()
              // eslint-disable-next-line
              .value(),)
          .mapValues(errs => errs.join(', '))
          .mapValues((rows, type) => `${type} in row(s): ${rows}`)
          .toArray()
          .value()
      );
    },
    setRemainingColumnsTo(x) {
      const mappedKeys = _.chain(this.analysis.columnMapping)
        .pickBy(_.identity)
        .keys()
        .value();

      _.chain(this.analysis.columns)
        .difference(mappedKeys)
        .each((col) => {
          this.analysis.columnMapping[col] = x;
        })
        .value();
    },
    getColumnPreview(col) {
      const x = _.chain(this.analysis.rowTable)
        .take(3)
        .map(row => ({ data: row[col] }))
        .value();
      return x;
    },
  },
  metaInfo: {
    title: 'Parse file',
  },
};
</script>
