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

        <b-nav-form>
          <b-button
            size="sm"
            class="my-2 my-sm-0"
            type="submit"
            @click="reload">
            <font-awesome-icon icon="sync-alt"/>
          </b-button>
        </b-nav-form>

        <b-nav-item
          :to="{ name: 'sync.prep' }"
          :active="isRoutePrefix('sync')">
          <font-awesome-icon icon="cloud-upload-alt"/>
          Reload
        </b-nav-item>

        <b-nav-item
          :to="{ name: 'sync.prep' }"
          :active="isRoutePrefix('sync')">
          <font-awesome-icon icon="cloud-upload-alt"/>
          Sync
        </b-nav-item>

        <b-nav-item-dropdown>
          <b-dropdown-item :to="{ name: 'batch.prep' }">
            <font-awesome-icon icon="th" /> Batch
          </b-dropdown-item>
          <b-dropdown-item :to="{ name: 'synclog' }">
            <font-awesome-icon icon="th" /> Log
          </b-dropdown-item>
        </b-nav-item-dropdown>


      </b-navbar-nav>

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

export default {
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
