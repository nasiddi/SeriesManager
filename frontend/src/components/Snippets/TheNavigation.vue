<template>
  <b-navbar
    :type="navbarType"
    :variant="navbarVariant"
    toggleable="md"
  >

    <b-nav-toggle target="nav_collapse"/>

    <b-navbar-brand
      v-if="loggedIn"
      :to="{ name: 'dashboard' }"
    >
      <font-awesome-icon icon="tv" /> Dashboard
    </b-navbar-brand>
    <b-navbar-brand
      v-else
      :to="{ name: 'home' }"
    >
      Login
    </b-navbar-brand>

    <b-collapse
      id="nav_collapse"
      is-nav
    >
      <b-navbar-nav v-if="loggedIn">

        <b-nav-item
          :to="{ name: 'files.index' }"
          :active="isRoutePrefix('files')">
          <font-awesome-icon icon="hdd"/>
          Files
        </b-nav-item>

        <b-nav-item-dropdown>
          <b-dropdown-item :to="{ name: 'files.upload' }">
            <font-awesome-icon icon="upload" /> Upload
          </b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item
          :to="{ name: 'project.start' }"
          :active="isRoutePrefix('corpus-analysis')">
          <font-awesome-icon icon="play" /> Corpus Analysis
        </b-nav-item>

        <b-nav-item-dropdown>
          <b-dropdown-item :to="{ name: 'corpus.choose' }">
            <font-awesome-icon icon="folder" /> Corpus
          </b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item
          :to="{ name: 'job.start' }"
          :active="isRoutePrefix('classification')">
          <font-awesome-icon icon="play"/>
          Classification
        </b-nav-item>

        <b-nav-item-dropdown>
          <b-dropdown-item :to="{ name: 'job.start' }">
            <font-awesome-icon icon="play"/>
            Start
          </b-dropdown-item>
          <b-dropdown-item :to="{ name: 'monitor.choose' }">
            <font-awesome-icon icon="terminal"/>
            Monitor
          </b-dropdown-item>
          <b-dropdown-item :to="{ name: 'evaluate.choose' }">
            <font-awesome-icon icon="check"/>
            Evaluate
          </b-dropdown-item>
        </b-nav-item-dropdown>

      </b-navbar-nav>

      <b-navbar-nav v-else>
        <b-nav-item :to="{ name: 'about' }">About</b-nav-item>
      </b-navbar-nav>

      <the-search v-if="false" />

      <b-navbar-nav
        v-if="loggedIn"
        class="ml-auto"
      >
        <b-nav-item-dropdown right>
          <template slot="button-content">
            <font-awesome-icon icon="user" /> {{ tokenDetails.name }}
          </template>
          <b-dropdown-item :to="{ name: 'settings' }">
            <font-awesome-icon icon="cogs" /> Settings
          </b-dropdown-item>
          <b-dropdown-divider/>
          <b-dropdown-item @click="logout">
            <font-awesome-icon icon="sign-out-alt" /> Logout
          </b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
      <b-navbar-nav
        v-else
        class="ml-auto"
      >
        <b-nav-item :to="{ name: 'login' }">
          <font-awesome-icon icon="sign-in-alt" /> Login
        </b-nav-item>
      </b-navbar-nav>

    </b-collapse>
  </b-navbar>
</template>

<script>
import TheSearch from './TheSearch';

export default {
  components: { TheSearch },
  computed: {
    loggedIn() {
      return this.$auth.isLoggedIn();
    },
    tokenDetails() {
      return this.$auth.getTokenDecoded();
    },
    navbarType() {
      return this.$store.getters.setting('navbar.type', 'dark');
    },
    navbarVariant() {
      return this.$store.getters.setting('navbar.variant', 'dark');
    },
  },
  created() {
    this.$router.afterEach(() => {
      this.$forceUpdate();
    });
  },
  methods: {
    logout() {
      this.$auth.logoutHard();
    },
    isRoutePrefix(prefix) {
      return this.$router.currentRoute.path.split('/')[1] === prefix;
    },
  },
};
</script>
