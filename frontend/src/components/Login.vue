<template>
  <div class="ui middle aligned center aligned grid">
    <div class="column">
      <div class="ui center aligned page grid">
        <div class="row">
          <div class="sixteen wide mobile eight wide tablet six wide computer column">
            <img src="/static/images/localpoint-logo.svg" class="image">
          </div>
        </div>
        <div class="row">
          <form id="login-view--form" v-on:submit.prevent="login" class="ui large form sixteen wide mobile eight wide tablet six wide computer column" v-bind:class="[success ? 'success' : 'error']">
            <div class="ui segment">
              <div class="field">
                <div class="ui left icon input">
                  <i class="user icon"></i>
                  <input id="login--email" name="email" :placeholder="$t('Username')" v-model="username">
                </div>
              </div>
              <div class="field">
                <div class="ui left icon input">
                  <i class="lock icon"></i>
                  <input id="login--password" name="password" type="password" :placeholder="$t('Password')" v-model="password">
                </div>
              </div>
              <sui-button class="ui fluid large submit button" type="submit" v-bind:class="{ loading:loading }">{{ $t('Sign in') }}</sui-button>
            </div>
            <div class="ui error message">{{ message }}</div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {saveApiClients, loadCurrentUser} from '../helpers/api';
import coreapi from 'coreapi/dist/coreapi';
import get from 'lodash/get';

export default {
  name: 'login',
  data() {
    return {
      username: '',
      password: '',
      message: '',
      success: null,
      loading: false
    };
  },
  methods: {
    login(e) {
      e.preventDefault();
      this.loading = true;
      if (!this.username || !this.password) {
        if (!this.username) {
          this.message = this.$t('Username must not be empty');
        } else if (!this.password) {
          this.message = this.$t('Password must not be empty');
        }
        this.success = false;
        this.loading = false;
        return;
      }
      // let axiosClient = this.$store.getters.axiosClient;
      let client = this.$store.getters.client || new coreapi.Client();
      let action = ['auth', 'login', 'create'];
      let params = {
        username: this.username,
        password: this.password,
      };
      let schema = this.$store.getters.coreapiSchema;
      client.action(schema, action, params).then((result) => {
        this.success = true;
        this.message = this.$t('Logging you in');
        let token = result.key;
        saveApiClients(token);
        loadCurrentUser(token, schema).then(() => {
          this.$router.push({name: 'File Upload'});
        });
      }).catch((error) => {
        this.success = false;
        if (get(error.content, 'non_field_errors')) {
          this.message = error.content.non_field_errors[0];
          this.loading = false;
        }
      });
    },
    clearMessage() {
      this.message = '';
    }
  }
};
</script>

<style scoped>
  .center.aligned.grid {
    height: 100%;
  }
</style>
