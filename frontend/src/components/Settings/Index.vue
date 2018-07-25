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
      <b-col>
        <parse-settings/>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import NavbarSettings from './Navbar';
import ParseSettings from './Parse';

export default {
  components: { NavbarSettings, ParseSettings },
  data: () => ({}),
  metaInfo: {
    title: 'Settings',
  },
};
</script>
