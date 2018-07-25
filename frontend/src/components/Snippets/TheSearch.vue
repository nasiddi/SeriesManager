<template>
  <div>
    <b-nav-form
      class="mx-auto"
      @submit="submit">
      <b-form-input
        :value="query"
        size="sm"
        class="mr-sm-2"
        type="text"
        required
        placeholder="Search"
        @change="change"/>
      <b-button
        v-b-modal.modal-search
        size="sm"
        class="my-2 my-sm-0"
      >
        <font-awesome-icon icon="search" />
      </b-button>
    </b-nav-form>
    <b-modal
      id="modal-search"
      ref="searchModal"
      :title="`Search results for ${query}`"
      @hidden="clearQuery"/>
  </div>
</template>

<script>
export default {
  computed: {
    query() {
      return this.$store.getters.searchQuery;
    },
  },
  created() {
    this.$eventHub.$on('trigger-search', this.showModal);
  },
  beforeDestroy() {
    this.$eventHub.$off('trigger-search');
  },
  methods: {
    submit(evt) {
      evt.preventDefault();
      this.showModal();
    },
    change(value) {
      this.$store.commit('searchQuery', value);
    },
    clearQuery() {
      this.$store.commit('searchQuery', '');
    },
    showModal() {
      if (this.query !== '') this.$refs.searchModal.show();
    },
    hideModal() {
      this.$refs.searchModal.hide();
    },
  },
};
</script>
