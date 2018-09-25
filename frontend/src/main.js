// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import coreapi from 'coreapi/dist/coreapi';
import SuiVue from 'semantic-ui-vue';
import Vue from 'vue';
import VueI18n from 'vue-i18n';

import App from './App';
import {dateTimeFormats} from './localization/datetime';
import router from './router';
import store from './store';
import {loadCurrentUser, saveApiClients} from './helpers/api';

const messages = require('./localization/translations.json');

Vue.config.productionTip = false;
Vue.use(SuiVue);
Vue.use(VueI18n);

async function init() {
  // Get schema
  let client = new coreapi.Client(
    {headers: {Accept: 'application/coreapi+json'}}
  );
  let schema = await client.get(`${process.env.BACKEND_URL}/api/docs/`);
  store.commit('setCoreapiSchema', {schema: schema});

  let currentUser = store.getters.currentUser;
  if (currentUser.token) {
    await saveApiClients(currentUser.token);
    try {
      await loadCurrentUser(currentUser.token, schema);
    } catch (err) {
      if (err.content.detail === 'Invalid token.') {
        store.commit('setCurrentUser', {token: '', user: {}});
      }
    }
  }

  // The language endpoint does not return the language
  // if the request has the `application/coreapi+json` header
  client = new coreapi.Client();

  // Get language and translations
  let getLang = await client.get(`${process.env.BACKEND_URL}/api/language/`);

  const i18n = new VueI18n({
    locale: getLang.language,
    silentTranslationWarn: true,
    dateTimeFormats,
    messages: messages
  });
  return i18n;
}

init().then((i18n) => {
  /* eslint-disable no-new */
  new Vue({
    el: '#app',
    store,
    router,
    i18n,
    components: {App},
    template: '<App/>'
  });
});
