// https://alligator.io/vuejs/creating-custom-plugins/ ??
import Router from 'vue-router';
import Cookies from 'js-cookie';

const jwt = require('jsonwebtoken');
const moment = require('moment');

const config = require('./../../config');

const COOKIE_NAME = config.authTokenCookie;

let init = false;

const router = new Router({
  mode: 'history',
});

function clearCookie() {
  Cookies.remove(COOKIE_NAME);
}

function getToken() {
  return Cookies.get(COOKIE_NAME);
}

function setToken(value, params) {
  Cookies.set(COOKIE_NAME, value, params);
}

function setTokenFromResponse(res) {
  setToken(res.headers.get('X-Access-Token'), { expires: moment(res.headers.get('X-Access-Token-Expiry')).toDate() });
}

function getTokenExpirationDate() {
  const token = jwt.decode(getToken());
  if (!token.exp) { return null; }

  return moment.unix(token.exp);
}

function isTokenExpired() {
  return getTokenExpirationDate().isBefore();
}

function isTokenEpxiringSoon(seconds = 10800) {
  return getTokenExpirationDate().diff(moment(), 'seconds') < seconds;
}
// eslint-disable-next-line
/* eslint no-param-reassign: ["error", { "props": true, "ignorePropertyModificationsFor": ["Vue"] }] */
function install(Vue) {
  Vue.mixin({
    created() {
      if (!init) {
        init = true;
        Vue.https
          .get('auth/check')
          .then(() => {
            if (isTokenEpxiringSoon()) {
              Vue.prototype.$auth.refresh();
            }
          }, () => {
            Vue.prototype.$auth.logoutAuto();
          });
      }
    },
  });

  const logoutAuto = () => {
    if (!getToken()) {
      return Vue.prototype.$auth.logoutSoft();
    }
    return Vue.prototype.$auth.logoutHard();
  };

  const logoutHard = () => {
    Vue.prototype.$auth.logoutSoft();
    router.push('/');
  };

  const logoutSoft = () => {
    clearCookie();
  };

  const isLoggedIn = () => !!getToken() && !isTokenExpired();

  const login = (params, failure) => {
    Vue.prototype.$auth.logoutSoft();
    Vue.https
      .post('auth/authenticate', params)
      .then((res) => {
        setTokenFromResponse(res);

        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('redirect')) {
          window.location.replace(urlParams.get('redirect'));
        } else {
          window.location.replace('/dashboard');
        }
      }, () => {
        failure();
      });
  };

  const refresh = () => {
    Vue.https
      .post('auth/refresh')
      .then((res) => {
        setTokenFromResponse(res);
      });
  };

  const requireAuth = (to, from, next) => {
    if (!Vue.prototype.$auth.isLoggedIn()) {
      next({
        path: '/login',
        query: { redirect: to.fullPath },
      });
    } else {
      next();
    }
  };


  const getTokenDecoded = () => {
    const decoded = jwt.decode(getToken());
    decoded.exp_moment = getTokenExpirationDate();
    return decoded;
  };

  Vue.prototype.$auth = {
    logoutAuto,
    logoutHard,
    logoutSoft,
    isLoggedIn,
    login,
    refresh,
    requireAuth,
    getTokenDecoded,
  };
}

export default install;

if (typeof window !== 'undefined' && window.Vue) {
  window.Vue.use(install);
}
