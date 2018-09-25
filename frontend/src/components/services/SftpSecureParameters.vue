<template>
  <div>
    <div class="ui header"><h3>{{ $t('Secure Parameters (Write Only)') }}</h3></div>
    <sui-form-field>
      <label>{{ $t('Username') }}</label>
      <sui-input :placeholder="$t('Username')" v-model="value.username"/>
    </sui-form-field>
    <sui-form-field>
      <label>{{ $t('Private Key') }}</label>
      <textarea class="two wide column" :placeholder="$t('Private Key')" v-model="value.private_key"/>
    </sui-form-field>
  </div>
</template>

<script>
export default {
  name: 'sftp-secure-parameters',
  props: ['value'],
  data() {
    return {};
  },
  computed: {
    parameters: () => {
      return {
        username: this.value.username,
        private_key: this.value.private_key,
      };
    },
  },
};
</script>

<style scoped>

</style>
