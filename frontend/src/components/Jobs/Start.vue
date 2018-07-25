<template>
  <div>
    <b-alert
      v-if="hasLoadingError"
      variant="danger"
    >Failed to load data from server</b-alert>

    <h1>
      Start a Classification
    </h1>

    <b-form @submit.prevent="submit">
      <b-card
        :border-variant="card1Variant"
        class="m-4"
      >
        <h4 slot="header">Data set</h4>
        <b-form-group label="Choose your type of file input">
          <b-form-radio-group
            v-model="fileInputType"
            :options="fileInputTypes"
            buttons
            button-variant="outline-primary"/>
        </b-form-group>

        <b-row v-if="fileInputType === 'data'">
          <b-col>
            <b-form-group
              horizontal
              label="Choose a file">
              <b-form-select
                v-model="filesSelected.data"
                :options="files"
                :state="Boolean(filesSelected.data)"/>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row v-if="fileInputType === 'train_test'">
          <b-col>
            <b-form-group
              horizontal
              label="Training file">
              <b-form-select
                v-model="filesSelected.train"
                :options="files"
                :state="Boolean(filesSelected.train)"/>
            </b-form-group>
          </b-col>

          <b-col>
            <b-form-group
              v-if="filesSelected.train"
              horizontal
              label="Test file">
              <b-form-select
                v-model="filesSelected.test"
                :options="filesTest"
                :state="Boolean(filesSelected.test)"/>
            </b-form-group>
            <p v-else>Select train file first.</p>
          </b-col>
        </b-row>
        <b-row v-if="fileInputType === 'train_test'">
          <b-col>
            <p>
              <small>
                <strong>Please note:</strong>
                The column mapping of the two file has to be identical.
                <br>
                Files with non-matching mappings will appear as disabled options.
                <br>
                You can also <b-link :to="{name: 'files.upload'}">upload a file</b-link>
              </small>
            </p>
          </b-col>
        </b-row>
      </b-card>

      <b-card
        :border-variant="card2Variant"
        class="m-4"
      >
        <h4 slot="header">Tokenizers</h4>
        <b-row>
          <b-col>
            <b-form-group
              horizontal
              label="Word tokenizer">
              <b-form-select
                v-model="wordTokenizer"
                :options="wordTokenizers"
                :state="Boolean(wordTokenizer)"/>
            </b-form-group>
          </b-col>
          <b-col>
            <b-form-group
              horizontal
              label="Sentence tokenizer">
              <b-form-select
                v-model="sentenceTokenizer"
                :options="sentenceTokenizers"
                :state="Boolean(sentenceTokenizer)"/>
            </b-form-group>
          </b-col>
        </b-row>
      </b-card>

      <b-card
        :border-variant="card3Variant"
        class="m-4"
      >
        <div slot="header">
          <h4 class="float-left">Algorithms</h4>
          <b-button-toolbar class="float-right">
            <b-button-group
              size="sm"
              class="mx-1"
            >
              <b-button
                :pressed="allConfigsChecked"
                variant="outline-secondary"
                @click="checkAllConfigs"
              >All</b-button>
              <b-button
                :pressed="noConfigsChecked"
                variant="outline-secondary"
                @click="uncheckAllConfigs"
              >None</b-button>
            </b-button-group>
          </b-button-toolbar>
        </div>
        <p>Please choose the algorithms you'd like to run on your data.</p>
        <b-list-group>
          <b-list-group-item
            v-for="algorithm in algorithms"
            v-if="algorithmConfigs[algorithm.id]"
            :key="algorithm.id"
          >
            <b-row>
              <b-col>
                <h5>
                  {{ algorithm.name }}
                </h5>
                <b-row>
                  <b-col md="9">
                    <p>
                      {{ algorithm.description }}
                      <br>
                      <small v-if="algorithm.description_source">
                        <b-link :href="algorithm.description_source">
                          [Source]
                        </b-link>
                      </small>
                    </p>
                  </b-col>
                  <b-col>
                    <div
                      v-for="algorithmConfig in algorithmConfigs[algorithm.id]"
                      :key="algorithmConfig.id"
                    >
                      <b-form-checkbox v-model="algorithmConfigsInUse[algorithmConfig.id]">
                        {{ algorithmConfig.name }}
                      </b-form-checkbox>
                    </div>
                  </b-col>
                </b-row>
              </b-col>
            </b-row>
          </b-list-group-item>
        </b-list-group>
      </b-card>

      <b-card
        :border-variant="card4Variant"
        class="m-4"
      >
        <h4 slot="header">Name</h4>
        <p>
          You may give your job a name.
          This allows you to better identify your job.
        </p>
        <b-form-group
          for="input-friendly_name"
        >
          <b-form-input
            id="input-friendly_name"
            v-model="friendly_name"
            name="friendly_name"
            type="text"/>
        </b-form-group>
      </b-card>

      <b-button
        :variant="submittable ? 'primary' : 'warning'"
        :disabled="!submittable"
        type="submit"
        size="lg"
        block
      >
        <span
          v-if="submittable"
          key="submittable">Start job on server</span>
        <span
          v-else
          key="submittable">Some required fields are empty.</span>
      </b-button>
    </b-form>

    <div v-if="hasSubmitError">
      <hr>
      <b-alert
        variant="warning"
        show>
        <h4 class="alert-heading">Something went wrong</h4>
        <pre
          id="output"
          class="pre-scrollable">{{ output }}</pre>
      </b-alert>
    </div>
  </div>
</template>


<script>
const _ = require('lodash');

export default {
  data: () => ({
    fileInputType: 'data',
    fileInputTypes: [
      { text: 'Automatic split', value: 'data' },
      { text: 'Separate train and test files', value: 'train_test' },
    ],
    files: [],
    filesSelected: { train: null, test: null, data: null },
    friendly_name: null,
    hasLoadingError: false,
    hasSubmitError: false,
    jobInfo: '',
    output: 'Unfortunately, no details are available',
    algorithms: {},
    algorithmConfigs: {},
    algorithmsInUse: {},
    algorithmConfigsInUse: {},
    project: {},
    wordTokenizer: null,
    wordTokenizers: [],
    sentenceTokenizer: null,
    sentenceTokenizers: [],
  }),
  computed: {
    allConfigsChecked() {
      return (
        _.chain(this.algorithmConfigsInUse)
          .filter(pc => pc)
          .size()
          .value() === _.size(this.algorithmConfigsInUse)
      );
    },
    noConfigsChecked() {
      return (
        _.chain(this.algorithmConfigsInUse)
          .filter(pc => pc)
          .size()
          .value() === 0
      );
    },
    submittable() {
      return this.card1Check && this.card2Check && this.card3Check && this.card4Check;
    },
    card1Check() {
      return (
        (this.fileInputType === 'train_test'
          && this.filesSelected.train
          && this.filesSelected.test)
        || (this.fileInputType === 'data' && this.filesSelected.data)
      );
    },
    card2Check() {
      return Boolean(this.wordTokenizer) && Boolean(this.sentenceTokenizer);
    },
    card3Check() {
      return (
        _.chain(this.algorithmConfigsInUse)
          .reduce((count, el) => (el ? count + 1 : count), 0)
          .value() > 0
      );
    },
    card4Check() {
      return Boolean(this.friendly_name);
    },
    card1Variant() {
      return this.card1Check ? 'success' : 'danger';
    },
    card2Variant() {
      return this.card2Check ? 'success' : 'danger';
    },
    card3Variant() {
      return this.card3Check ? 'success' : 'danger';
    },
    card4Variant() {
      return this.friendly_name ? 'success' : 'danger';
    },
    filesTest() {
      const train = _.chain(this.files)
        .filter(f => f.value === this.filesSelected.train)
        .map(f => f.extra)
        .first()
        .value();

      if (!train) {
        return [];
      }
      const trainColMap = JSON.parse(train.corpus_analysis_config).columnMapping;
      const formatfileSelect = (file) => {
        const colMap = JSON.parse(file.extra.corpus_analysis_config).columnMapping;

        return {
          text: `${file.extra.friendly_name} (${file.extra.uuid})`,
          value: file.extra.uuid,
          disabled: !_.isEqual(trainColMap, colMap),
          extra: file,
        };
      };

      const filesTest = _.chain(this.files)
        .filter(f => f.extra.is_parsed === 1)
        .map(formatfileSelect)
        .value();

      // eslint-disable-next-line vue/no-side-effects-in-computed-properties
      this.filesSelected.test = _.chain(filesTest)
        .filter(f => !f.disabled)
        .map(f => f.value)
        .first()
        .value();

      return filesTest;
    },
  },
  watch: {
    filesSelected: {
      handler() {
        this.setFriendlyName();
      },
      deep: true,
    },
    fileInputType() {
      this.setFriendlyName();
    },
  },
  metaInfo: {
    title: 'Start a new job',
  },
  created() {
    this.$http.get('files/').then((res) => {
      const formatfileSelect = file => ({
        text: `${file.friendly_name} (${file.uuid})`,
        value: file.uuid,
        extra: file,
      });

      if (_.size(res.body) === 0) {
        this.$snotify.info('No files found');
      }

      this.files = _.chain(res.body)
        .filter(f => f.is_parsed === 1)
        .map(formatfileSelect)
        .sortBy(f => f.text.toLowerCase())
        .value();
      if (this.$router.currentRoute.params.file_uuid) {
        this.filesSelected.data = this.$router.currentRoute.params.file_uuid;
        this.filesSelected.train = this.$router.currentRoute.params.file_uuid;
      }
    });

    this.$http.get('algorithms').then(
      (res) => {
        this.algorithms = _.keyBy(res.body, 'id');
        this.algorithmsInUse = _.mapValues(this.algorithms, () => true);
      },
      () => {
        this.hasLoadingError = true;
      },
    );

    this.$http.get('algorithms/configs').then(
      (res) => {
        this.algorithmConfigs = _.groupBy(res.body, el => el.algorithm_id);
        this.algorithmConfigs = _.chain(this.algorithmConfigs)
          .mapValues(configs => _.keyBy(configs, 'id'))
          .value();
        this.algorithmConfigsInUse = _.chain(res.body)
          .map(el => el.id)
          .invert()
          .mapValues(() => true)
          .value();
      },
      () => {
        this.hasLoadingError = true;
      },
    );

    this.$http.get('algorithms/tokenizers').then(
      (res) => {
        this.wordTokenizers = res.body.word;
        this.sentenceTokenizers = res.body.sentence;
        [this.wordTokenizer] = this.wordTokenizers;
        [this.sentenceTokenizer] = this.sentenceTokenizers;
      },
      () => {
        this.hasLoadingError = true;
      },
    );
  },
  methods: {
    checkAllConfigs() {
      this.algorithmConfigsInUse = _.chain(this.algorithmConfigsInUse)
        .mapValues(() => true)
        .value();
    },
    uncheckAllConfigs() {
      this.algorithmConfigsInUse = _.chain(this.algorithmConfigsInUse)
        .mapValues(() => false)
        .value();
    },
    submit() {
      this.jobInfo = null;
      this.output = null;

      this.$http
        .post('jobs', {
          algorithmConfigs: _.chain(this.algorithmConfigsInUse)
            .mapValues((el, k) => (el ? k : false))
            .filter()
            .map(el => parseInt(el, 10))
            .value(),
          friendly_name: this.friendly_name,
          files: JSON.stringify(this.filesSelected),
          fileInputType: this.fileInputType,
          wordTokenizer: this.wordTokenizer,
          sentenceTokenizer: this.sentenceTokenizer,
          project_uuid: this.$router.currentRoute.params.project_uuid,
        })
        .then(
          (res) => {
            this.$router.push({
              name: 'monitor.job',
              params: { job_uuid: res.body.uuid },
            });
          },
          (res) => {
            this.hasSubmitError = true;
            if (res.body) this.output = res.body;
          },
        );
    },
    setFriendlyName() {
      if (this.fileInputType === 'data') {
        const data = _.chain(this.files)
          .filter(f => f.value === this.filesSelected.data)
          .map(f => f.extra)
          .first()
          .value();
        if (data) {
          this.friendly_name = `Classification of ${data.friendly_name}`;
        }
      } else {
        const train = _.chain(this.files)
          .filter(f => f.value === this.filesSelected.train)
          .map(f => f.extra)
          .first()
          .value();
        const test = _.chain(this.files)
          .filter(f => f.value === this.filesSelected.test)
          .map(f => f.extra)
          .first()
          .value();
        if (train && test) {
          this.friendly_name = `Classification of ${train.friendly_name} / ${test.friendly_name}`;
        } else if (train) {
          this.friendly_name = `Classification of ${train.friendly_name}`;
        }
      }
    },
  },
};
</script>
