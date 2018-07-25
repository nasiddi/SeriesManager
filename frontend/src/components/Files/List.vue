<template>
  <div>
    <b-list-group>
      <b-list-group-item
        :to="{ name: 'files.upload' }"
        variant="primary">
        <font-awesome-icon icon="upload" /> Upload
      </b-list-group-item>
      <b-list-group-item
        v-for="file in files"
        :key="file.uuid"
        class="flex-column align-items-start">
        <div class="d-flex w-100 justify-content-between">
          <h5 class="mb-1">{{ file.friendly_name }}</h5>
          <small>uploaded {{ formatTimestamp(file.created_at) }}</small>
        </div>
        <b-button-group size="sm">
          <b-button
            v-b-modal="`modal-delete-${file.uuid}`"
            variant="outline-danger">
            Delete
          </b-button>
          <b-button
            v-if="!file.is_parsed"
            :to="{ name:'files.parse', params: { file_uuid: file.uuid } }"
            variant="outline-primary">
            Parse
          </b-button>
          <b-button
            v-if="file.is_parsed"
            variant="outline-warning"
            @click="resetParse(file.uuid)">
            Reset parse options
          </b-button>
          <b-button
            v-if="file.is_parsed"
            :to="{ name:'project.start_from_file', params: { file_uuid: file.uuid } }"
            variant="outline-success"
          >
            Start corpus analysis
          </b-button>
          <b-dropdown
            v-if="
            _.size(file.projects) > 0"
            variant="outline-secondary"
            right
            size="sm">
            <b-dropdown-item
              v-for="project in file.projects"
              :to="{ name: 'corpus.project', params: { project_uuid: project.uuid } }"
              :key="project.uuid">
              {{ project.friendly_name }}
            </b-dropdown-item>
          </b-dropdown>
          <b-button
            v-if="file.is_parsed"
            :to="{ name:'job.start_from_file', params: { file_uuid: file.uuid } }"
            variant="outline-success"
          >
            Start classification
          </b-button>
          <b-dropdown
            v-if="
            _.size(file.jobs) > 0"
            variant="outline-secondary"
            right
            size="sm">
            <b-dropdown-item
              v-for="job in file.jobs"
              :to="{ name: 'monitor.job', params: { job_uuid: job.uuid } }"
              :key="job.uuid">
              {{ job.friendly_name }}
            </b-dropdown-item>
          </b-dropdown>
        </b-button-group>

        <b-modal
          :id="`modal-delete-${file.uuid}`"
          :title="`Do you really want to delete ${file.friendly_name}?`"
          header-bg-variant="warning"
          header-border-variant="warning"
          ok-variant="danger"
          ok-title="Yes, delete file"
          cancel-variant="success"
          cancel-title="No, cancel"
          centered
          @ok="deleteFile(file.uuid)">
          Deleting a file will delete all jobs and corpus analyses associated with it.
        </b-modal>

        <br>
        <small>
          <span v-if="file.row_count">
            {{ file.filename }}, {{ file.row_count }} rows
          </span>
          <span v-if="file.is_parsed">
            <br>
            with the following column types:
            {{ JSON.parse(file.corpus_analysis_config).columnMapping }}
          </span>
        </small>
      </b-list-group-item>
      <b-list-group-item
        v-if="_.size(files) > 0"
        :to="{ name: 'files.upload' }"
        variant="primary">
        <font-awesome-icon icon="upload" /> Upload
      </b-list-group-item>
    </b-list-group>
  </div>
</template>

<script>
const moment = require('moment');

export default {
  data: () => ({
    files: {},
  }),
  mounted() {
    this.loadData();
  },
  methods: {
    loadData() {
      this.$http.get('files/').then((res) => {
        this.files = res.body;
      });
    },
    formatTimestamp(ts) {
      return moment.utc(ts).fromNow();
    },
    deleteFile(uuid) {
      this.$http
        .delete(`files/${uuid}`)
        .then(() => {
          this.$snotify.success('Deleted file');
        })
        .then(() => {
          this.loadData();
        });
    },
    resetParse(uuid) {
      this.$http
        .post(`files/${uuid}/reset`)
        .then(() => {
          this.$snotify.success('Reset file');
        })
        .then(() => {
          this.loadData();
        });
    },
  },
};
</script>
