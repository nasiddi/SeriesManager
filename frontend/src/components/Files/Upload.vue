<template>
  <div>
    <h1>Upload</h1>

    <b-form
      @submit.prevent="submit">
      <b-form-group
        horizontal
        label="File"
        description="Accepted formats are csv, tsv, txt up to 100 GB">
        <b-form-file
          v-model="file"
          :state="Boolean(file)"
          placeholder="Choose a file..."
          accept=".csv,.tsv,.txt"
          @input="fileChanged"
        />
      </b-form-group>
      <b-form-group
        horizontal
        label="Name"
        description="You should give your file a name to be able to (better) re-use it later">
        <b-form-input
          v-model="name"
          :state="Boolean(name)"
        />
      </b-form-group>
      <b-button
        :disabled="!isSaveable || hasPendingRequest"
        variant="primary"
        block
        type="submit">
        Save file on server
      </b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  data: () => ({
    file: null,
    name: null,
    hasPendingRequest: false,
  }),
  computed: {
    isSaveable() {
      return Boolean(this.file) && Boolean(this.name);
    },
  },
  methods: {
    fileChanged(file) {
      this.name = file.name;
    },
    submit() {
      this.hasPendingRequest = true;

      const notifUploading = this.$snotify.info('Uploading...', { timeout: 0 });

      const formData = new FormData();
      formData.append('file', this.file);
      formData.append('name', this.name);

      this.$http
        .post('files/upload', formData)
        .then(
          (res) => {
            this.$snotify.success('Uploaded!');
            this.$router.push({
              name: 'files.parse',
              params: { file_uuid: res.body },
            });
          },
          () => {
            this.$snotify.error('Could not save on server');
          },
        )
        .then(() => {
          this.hasPendingRequest = false;
          this.$snotify.remove(notifUploading.id);
        });
    },
  },
  metaInfo: {
    title: 'Upload',
  },
};
</script>
