<template>
  <div>
    <h1>Files</h1>
    <files-list/>
  </div>
</template>

<script>
import FilesList from '@/components/Files/List';

export default {
  components: { FilesList },
  data: () => ({}),
  metaInfo: {
    title: 'Files',
  },
};
</script>
