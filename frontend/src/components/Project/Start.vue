<template>
  <div>
    <h1>Start</h1>

    <b-form
      @submit.prevent="submit">
      <b-form-group
        horizontal
        label="Choose a file">
        <template slot="description">
          You can also <b-link :to="{name: 'files.upload'}">upload a file</b-link>
        </template>
        <b-form-select
          v-model="file"
          :options="files"
          :state="Boolean(file)"
          @change="fileSelected"/>
      </b-form-group>
      <b-form-group
        horizontal
        label="Name"
        description="You should give your corpus a name to be able to (better) re-use it later">
        <b-form-input
          v-model="name"
          :state="Boolean(name)"
        />
      </b-form-group>

      <b-form-group
        horizontal
        label="Advanced options"
        description="Would you like to set advanced options for the analysis?">
        <b-form-checkbox
          v-model="advancedOptions"
        />
      </b-form-group>


      <b-row v-if="advancedOptions">
        <b-col>
          <b-card
            header="Analyzers"
          >
            <b-form-group
              label="Choose analyzers to run"
              horizontal>
              <b-form-checkbox-group
                v-model="analyzersSelected"
                :options="analyzersAvailable"
                stacked/>
            </b-form-group>
          </b-card>
        </b-col>
        <b-col>
          <b-card
            header="Parameters for topic modeling"
          >
            <b-form-group
              label="Number of topics"
            >
              <b-form-input
                :min="2"
                v-model.number="topic_modeling.n_topics"
                type="number"
                required
              />
            </b-form-group>

            <b-form-group
              label="Number of words per topic"
            >
              <b-form-input
                :min="1"
                v-model.number="topic_modeling.n_words_per_topic"
                type="number"
                required
              />
            </b-form-group>

            <b-form-group
              label="Number of features"
              description="enter 0 for no features"
            >
              <b-form-input
                :min="0"
                v-model.number="topic_modeling.n_features"
                type="number"
                required
              />
            </b-form-group>

            <b-form-group
              label="Max. size of n-grams"
            >
              <b-form-input
                :min="1"
                :max="4"
                v-model.number="topic_modeling.n_grams"
                type="number"
                required
              />
            </b-form-group>
          </b-card>
        </b-col>
      </b-row>

      <b-button
        :disabled="!isSaveable || hasPendingRequest"
        variant="primary"
        class="mt-4"
        type="submit"
        block>
        Start
      </b-button>
    </b-form>
  </div>
</template>

<script>
const _ = require('lodash');

export default {
  data: () => ({
    hasPendingRequest: false,
    files: [],
    file: null,
    name: null,
    advancedOptions: false,
    topic_modeling: {
      n_topics: 10,
      n_words_per_topic: 10,
      n_features: 1000,
      n_grams: 1,
    },
    analyzersSelected: ['topic_modeling', 'general_stats', 'sentence_tokenizer', 'word_tokenizer'],
    analyzersAvailable: [
      { value: 'general_stats', text: 'general stats' },
      { value: 'topic_modeling', text: 'topic modeling' },
      { value: 'sentence_tokenizer', text: 'sentence tokenizer' },
      { value: 'word_tokenizer', text: 'word tokenizer' },
    ],
  }),
  computed: {
    isSaveable() {
      return Boolean(this.file) && Boolean(this.name);
    },
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
        .map(formatfileSelect)
        .sortBy(f => f.text.toLowerCase())
        .value();

      if (this.$router.currentRoute.params.file_uuid) {
        this.file = this.$router.currentRoute.params.file_uuid;
        this.fileSelected(this.file);
      }
    });
  },
  methods: {
    fileSelected(uuid) {
      const file = _.chain(this.files)
        .filter(f => f.value === uuid)
        .map(f => f.extra)
        .first()
        .value();

      this.name = `Analysis of ${file.friendly_name}`;
    },
    submit() {
      this.hasPendingRequest = true;
      this.$http
        .post('projects/', {
          file_uuid: this.file,
          name: this.name,
          config: JSON.stringify({
            analyse: _.chain(this.analyzersAvailable)
              .map(v => v.value)
              .zipObject()
              .mapValues((v, k) => _.includes(this.analyzersSelected, k))
              .mapValues(v => (v ? 1 : 0))
              .value(),
            topic_modeling: this.topic_modeling,
          }),
        })
        .then(
          (res) => {
            this.$snotify.success('Started analysis');
            this.$router.push({
              name: 'corpus.project',
              params: {
                project_uuid: res.body,
              },
            });
          },
          () => {
            this.$snotify.error('Starting analysis failed');
          },
        )
        .then(() => {
          this.hasPendingRequest = false;
        });
    },
  },
  metaInfo: {
    title: 'Start',
  },
};
</script>
