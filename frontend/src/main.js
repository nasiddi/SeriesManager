// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import Vuex from 'vuex';
import VuePromiseBtn from 'vue-promise-btn';
import Sticky from 'vue-sticky-directive';
import App from './App';
import router from './router';

const _ = require('lodash');
const md5 = require('md5');
const config = require('./config');

Vue.config.productionTip = false;
Vue.use(VuePromiseBtn, {});

const shared = {
  rootUrl: config.rootUrl,
};

shared.install = () => {
  Object.defineProperty(Vue.prototype, '$globalData', {
    get() {
      return shared;
    },
  });
};

Vue.use(shared);

Vue.mixin({
  methods: {
    formatPercentage(number) {
      return number > 0 ? `${(number * 100).toFixed(2)}%` : '0%';
    },
    f1ScoreFormatted(f1) {
      return f1 > 0 ? `${(f1 * 100).toFixed(2)}%` : '0%';
    },
    loadSettings() {
      if (this.$auth.isLoggedIn()) {
        this.$http.get('settings').then(
          (res) => {
            this.$store.commit('allSettings', res.body);
          },
          () => {
            this.$snotify.error('Failed to load settings');
          },
        );
      }
    },

    getGenres() {
      return [
        '',
        'Action',
        'Animation',
        'Comedy',
        'Comics',
        'Crime',
        'Documentary',
        'Drama',
        'Fantasy',
        'Game Show',
        'Historical',
        'Hospital',
        'Sci-Fi',
      ];
    },
    // Basically, this function returns predictable, "random" colors
    // and for extra fun it does so by finding the smallest hamming distance
    // to any one of Google's Material Design 500 colors
    // and once it runs out of colors, it switches to MD5 hashes.
    colorArrayRandom(strs) {
      // https://codereview.stackexchange.com/a/154343/56118
      const hammingDistance = (x, y) => {
        // eslint-disable-next-line no-bitwise
        let val = x ^ y;

        let distance;
        for (distance = 0; val > 0; distance += 1) {
          // eslint-disable-next-line no-bitwise
          val &= val - 1;
        }

        return distance;
      };
      const colors = [
        '001f3f',
        '0074D9',
        '7FDBFF',
        '3D9970',
        '2ECC40',
        '01FF70',
        'FFDC00',
        'FF851B',
        'FF4136',
        '85144b',
        'F012BE',
        'B10DC9',
      ];

      return _.chain(strs)
        .map(str => md5(str))
        .map(str => str.substring(0, 6))
        .map((str) => {
          const strNum = parseInt(str, 16);
          const distances = _.chain(colors)
            .zipObject(colors)
            .mapValues(color => parseInt(color, 16))
            .mapValues(color => hammingDistance(strNum, color))
            .value();

          if (_.size(distances) > 0) {
            const color = Object.keys(distances)
              .reduce((a, b) => (distances[a] < distances[b] ? a : b));

            _.remove(colors, val => val === color);
            return color;
          }

          return str;
        })
        .map(str => `#${str}`)
        .value();
    },
  },
});

Vue.http.options.root = config.rootUrl;
Vue.http.interceptors.push((request) => {
  request.headers.set('X-Access-Token', Vue.cookie.get(config.authTokenCookie));
  return (response) => {
    if (response.status === 404) {
      window.vm.$snotify.error('404', { timeout: 0 });
    }
  };
});

Vue.use(Vuex);
Vue.use(Sticky);

const store = new Vuex.Store({
  /* eslint-disable no-param-reassign */
  state: {
    searchQuery: null,
    settings: {},
  },
  getters: {
    searchQuery: state => state.searchQuery,
    setting(state) {
      return (key, defaultValue = null) => {
        const setting = state.settings[key];
        if (setting) {
          return setting.value;
        }
        return defaultValue;
      };
    },
  },
  mutations: {
    searchQuery: (state, query) => {
      state.searchQuery = query;
      window.vm.$eventHub.$emit('trigger-search');
    },
    allSettings: (state, allSettings) => {
      state.settings = allSettings;
      window.vm.$eventHub.$emit('settings-update');
    },
    singleSetting: (state, singleSetting) => {
      const { key, value } = singleSetting;
      state.settings[key] = { value };
      window.vm.$eventHub.$emit('settings-update');
    },
  },
  actions: {
    saveSetting: (state, payload) => {
      const { key, value } = payload;

      Vue.http.post('settings', { key, value });
      state.commit('singleSetting', { key, value });
    },
  },
});

Vue.prototype.$eventHub = new Vue(); // Global event bus

// eslint-disable-next-line
const vm = new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
  store,
});
window.vm = vm;
