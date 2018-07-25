<template>
  <div>
    <b-form
      @submit.prevent="submit"
    >
      <b-row>
        <b-col>
          <b-form-select
            v-if="suggestionKey && suggestionValue"
            v-model="selected"
          >
            <optgroup label="Suggested projects">
              <option
                v-for="project in projectsSuggested"
                :key="project.value"
                :value="project.value">
                {{ project.text }}
              </option>
            </optgroup>
            <optgroup label="Other projects">
              <option
                v-for="project in projectsNotSuggested"
                :key="project.value"
                :value="project.value">
                {{ project.text }}
              </option>
            </optgroup>
          </b-form-select>
          <b-form-select
            v-else
            v-model="selected"
            :options="projects"/>
        </b-col>
        <b-col>
          <b-button
            :disabled="!Boolean(selected)"
            type="submit"
            variant="primary"
            block
          >Go!</b-button>
        </b-col>
      </b-row>
    </b-form>
  </div>
</template>
<script>
const _ = require('lodash');
const moment = require('moment');

export default {
  props: {
    suggestionKey: {
      type: String,
      required: false,
      default: null,
    },
    suggestionValue: {
      type: String,
      required: false,
      default: null,
    },
  },
  data: () => ({
    selected: null,
    projects: [],
    projectsSuggested: [],
    projectsNotSuggested: [],
  }),
  created() {
    this.$http.get('projects/').then((res) => {
      const formatProjectSelect = (project) => {
        const date = moment
          .utc(project.created_at)
          .local()
          .format('YYYY-MM-DD HH:mm');
        return {
          text: `${project.friendly_name} (${date} | ${project.uuid})`,
          value: project.uuid,
        };
      };

      if (_.size(res.body) === 0) {
        this.$snotify.info('No projects found');
      }

      if (this.suggestionKey && this.suggestionValue) {
        const suggested = _.chain(res.body)
          // eslint-disable-next-line eqeqeq
          .pickBy(p => p[this.suggestionKey] == this.suggestionValue)
          .value();

        const notSuggested = _.chain(res.body)
          // eslint-disable-next-line eqeqeq
          .pickBy(p => p[this.suggestionKey] != this.suggestionValue)
          .value();

        this.projectsSuggested = _.chain(suggested)
          .map(formatProjectSelect)
          .sortBy(p => p.text.toLowerCase())
          .value();

        this.projectsNotSuggested = _.chain(notSuggested)
          .map(formatProjectSelect)
          .sortBy(p => p.text.toLowerCase())
          .value();
      } else {
        this.projects = _.chain(res.body)
          .map(formatProjectSelect)
          .sortBy(p => p.text.toLowerCase())
          .value();
      }
    });
  },
  mounted() {
    if (this.$router.currentRoute.params.project_uuid !== undefined) {
      this.selected = this.$router.currentRoute.params.project_uuid;
      this.submit('router');
    }
  },
  methods: {
    submit(event = 'user') {
      this.$emit('chosen', {
        actor: _.isObject(event) ? 'user' : event,
        uuid: this.selected,
      });
    },
  },
};
</script>
