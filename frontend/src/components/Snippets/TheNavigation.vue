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
      <b-navbar-nav
        v-if="loggedIn">

        <b-button
          size="sm"
          class="my-2 my-sm-0"
          type="submit"
          @click="reload">
          <font-awesome-icon icon="sync-alt"/>
        </b-button>

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
            <font-awesome-icon icon="list" /> Log
          </b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item
          :to="{ name: 'filetree' }"
          :active="isRoutePrefix('filetree')">
          <font-awesome-icon :icon="['fab', 'elementor']"/>
          FileTree
        </b-nav-item>

        <b-nav-item-dropdown left>
          <b-dropdown-item :to="{ name: 'filetree.dictionary' }">
            <font-awesome-icon icon="atlas" /> Dictionary
          </b-dropdown-item>
          <b-dropdown-item :to="{ name: 'filetree.missing' }">
            <font-awesome-icon icon="ghost" /> Missing Files
          </b-dropdown-item>
          <b-dropdown-item :to="{ name: 'filetree.exceptionfile' }">
            <font-awesome-icon icon="exclamation-circle" /> Exception File
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
    async reload() {
      let notifLoading = null;
      this.$http
        .post('python/reload')
        .then((notifLoading = this.$snotify.info('Reloading', { timeout: 0 })))
        .then((res) => {
          this.$snotify.remove(notifLoading.id);
          if (res.body === 'failed') {
            this.$snotify.error('Loading failed');
          } else {
            this.$snotify.success(res.body);
            this.$router.push({
              name: 'dashboard',
            });
          }
        });
    },
  },
};
</script>
