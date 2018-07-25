<template>
  <div>
    <choose-project
      suggestion-key="is_corpus_analyzed"
      suggestion-value="1"
      @chosen="chosen"/>
  </div>
</template>
<script>
import ChooseProject from '@/components/Snippets/ChooseProject';

export default {
  components: { ChooseProject },
  data: () => ({
    chosenUuid: null,
  }),
  methods: {
    chosen(payload) {
      this.chosenUuid = payload.uuid;
      this.$router.push({
        name: 'corpus.project',
        params: { project_uuid: this.chosenUuid },
      });
    },
  },
};
</script>
