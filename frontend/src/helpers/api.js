import axios from 'axios';
import coreapi from 'coreapi/dist/coreapi';
import store from '../store';

function saveApiClients(token) {
  let auth = new coreapi.auth.TokenAuthentication({
    scheme: 'Token',
    token: token
  });
  let coreapiClient = new coreapi.Client({auth: auth});
  store.commit('setCoreapiClient', {client: coreapiClient});

  // Load locale after loading core api client with an action
  store.dispatch('loadLocales');

  let axiosClient = axios.create({
    baseURL: `${process.env.BACKEND_URL}/api/`,
    timeout: process.env.AXIOS_TIMEOUT,
    headers: {'Authorization': `Token ${token}`}
  });
  store.commit('setAxiosClient', {client: axiosClient});
}

function loadCurrentUser(token, schema) {
  let action = ['auth', 'user', 'read'];

  // Return promise so we can wait for the api call to end
  return store.getters.coreapiClient.action(schema, action).then((result) => {
    store.commit('setCurrentUser', {token: token, user: result});
  });
}

export {saveApiClients, loadCurrentUser};
