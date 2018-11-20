<template>
  <div>
    <h1>Settings</h1>
    <b-alert
      variant="info"
      show>Settings are saved automatically.</b-alert>
    <b-row>
      <b-col>
        <navbar-settings/>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import NavbarSettings from './Navbar';

export default {
  components: { NavbarSettings },
  data: () => ({}),
  metaInfo: {
    title: 'Settings',
  },
};
</script>
