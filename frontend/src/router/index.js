import Vue from 'vue';
import Router from 'vue-router';

import BootstrapVue from 'bootstrap-vue';
import VueResource from 'vue-resource';
import VueCharts from 'vue-chartjs';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { fab } from '@fortawesome/free-brands-svg-icons';

import { library as faLibrary } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import Snotify, { SnotifyPosition } from 'vue-snotify';
import VueLodash from 'vue-lodash';
import Meta from 'vue-meta';

import 'vue-snotify/styles/material.scss';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootstrap/dist/css/bootstrap.css';

import DashboardIndex from '@/components/Dashboard/Index';
import About from '@/components/About';
import Home from '@/components/Home';
import Sync from '@/components/Sync';
import Update from '@/components/Update';
import UpdateNav from '@/components/UpdateNav';
import SyncReport from '@/components/SyncReport';
import BatchPrep from '@/components/BatchPrep';
import BatchValidate from '@/components/BatchValidate';
import BatchReport from '@/components/BatchReport';
import Stats from '@/components/Stats';
import FileTree from '@/components/FileTree';
import SyncLog from '@/components/SyncLog';
import MissingFiles from '@/components/MissingFiles';
import Dictionary from '@/components/Dictionary';

import Login from '@/components/Auth/Login';
import Auth from '@/components/Auth/utils';

const VueMoment = require('vue-moment');
const VueCookie = require('vue-cookie');

const config = require('./../config');

faLibrary.add(fas);
faLibrary.add(fab);
Vue.component('font-awesome-icon', FontAwesomeIcon);

Vue.use(Router);
Vue.use(BootstrapVue);
Vue.use(VueResource);
Vue.use(VueCharts);
Vue.use(Meta);
Vue.use(VueMoment);
Vue.use(VueCookie);

Vue.use(VueLodash, { name: '_' });

Vue.http.options.root = config.rootUrl;
Vue.http.interceptors.push((request) => {
  request.headers.set('X-Access-Token', Vue.cookie.get(config.authTokenCookie));
});

Vue.use(Auth);

Vue.use(Snotify, {
  toast: {
    position: SnotifyPosition.rightTop,
  },
});

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/update',
      name: 'update',
      components: {
        default: Update,
        sidebarLeft: UpdateNav,
      },
      beforeEnter: Vue.prototype.$auth.requireAuth,
    },
    {
      path: '/synclog',
      name: 'synclog',
      component: SyncLog,
      beforeEnter: Vue.prototype.$auth.requireAuth,
    },
    {
      path: '/batch/prep',
      name: 'batch.prep',
      component: BatchPrep,
      beforeEnter: Vue.prototype.$auth.requireAuth,
    },
    {
      path: '/filetree',
      name: 'filetree',
      component: FileTree,
      beforeEnter: Vue.prototype.$auth.requireAuth,
    },
    {
      path: '/filetree/missing',
      name: 'filetree.missing',
      component: MissingFiles,
      beforeEnter: Vue.prototype.$auth.requireAuth,
    },
    {
      path: '/filetree/dictionary',
      name: 'filetree.dictionary',
      component: Dictionary,
      beforeEnter: Vue.prototype.$auth.requireAuth,
    },
    {
      path: '/reroute',
      name: 'reroute',
      component: About,
      beforeEnter: Vue.prototype.$auth.requireAuth,
    },
    {
      path: '/batch/validate',
      name: 'batch.validate',
      component: BatchValidate,
      beforeEnter: Vue.prototype.$auth.requireAuth,
    },
    {
      path: '/batch/report',
      name: 'batch.report',
      component: BatchReport,
      beforeEnter: Vue.prototype.$auth.requireAuth,
    },
    {
      path: '/sync/prep',
      name: 'sync.prep',
      component: Sync,
      beforeEnter: Vue.prototype.$auth.requireAuth,
    },
    {
      path: '/sync/report',
      name: 'sync.report',
      component: SyncReport,
      beforeEnter: Vue.prototype.$auth.requireAuth,
    },
    {
      path: '/stats',
      name: 'stats',
      component: Stats,
      beforeEnter: Vue.prototype.$auth.requireAuth,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardIndex,
      beforeEnter: Vue.prototype.$auth.requireAuth,
    },
  ],
});
