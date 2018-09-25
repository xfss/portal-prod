<template>
  <div class="ui middle aligned center aligned grid">
    <div class="column">
      <div class="ui center aligned page grid">
        <div class="row">
          <div class="ui large header">{{ $t('Signing out') }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import coreapi from 'coreapi/dist/coreapi';

export default {
  name: 'logout',
  mounted() {
    let client = this.$store.getters.client || new coreapi.Client();
    let action = ['auth', 'logout', 'create'];
    let schema = this.$store.getters.coreapiSchema;
    client.action(schema, action).then((result) => {
      this.$store.commit('setCurrentUser', {token: '', user: {}});
      this.$router.push({name: 'Login'});
    });
  }
};
</script>

<style scoped>
  .center.aligned.grid {
    height: 100%;
  }
</style>
