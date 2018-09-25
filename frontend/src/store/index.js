import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';
import get from 'lodash/get';

Vue.use(Vuex);

const store = new Vuex.Store({
  plugins: [
    createPersistedState({
      paths: [
        'currentUser.token',
      ],
    })
  ],
  state: {
    coreapiClient: null,
    coreapiSchema: null,
    axiosClient: null,
    currentUser: {
      token: '',
      data: {},
    },
    languages: [],
    timezones: [],
  },
  mutations: {
    setCoreapiClient(state, {client}) {
      state.coreapiClient = client;
    },
    setCoreapiSchema(state, {schema}) {
      state.coreapiSchema = schema;
    },
    setAxiosClient(state, {client}) {
      state.axiosClient = client;
    },
    setCurrentUser(state, {token, user}) {
      state.currentUser.token = token;
      state.currentUser.data = user;
    },
    setLanguages(state, {languages}) {
      state.languages = languages;
    },
    setTimezones(state, {timezones}) {
      state.timezones = timezones;
    },
  },
  actions: {
    loadLocales({commit, state}) {
      let client = state.coreapiClient;
      let schema = state.coreapiSchema;

      client.action(schema, ['languages', 'list']).then((result) => {
        commit('setLanguages', {languages: result});
      });

      client.action(schema, ['timezones', 'list']).then((result) => {
        commit('setTimezones', {timezones: result});
      });
    }
  },
  getters: {
    coreapiClient: state => {
      return state.coreapiClient;
    },
    coreapiSchema: state => {
      return state.coreapiSchema;
    },
    axiosClient: state => {
      return state.axiosClient;
    },
    currentUser: state => {
      return state.currentUser;
    },
    publicationOptions: state => {
      let publications = get(state.currentUser, 'data.publications');
      let options = [];
      if (publications) {
        for (let publication of publications) {
          options.push({
            text: publication.name,
            value: publication.id
          });
        }
      }
      return options;
    },
    languages: state => {
      return state.languages;
    },
    timezones: state => {
      return state.timezones;
    },
  }
});

export {store};
export default store;
