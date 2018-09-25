<template>
  <div>
    <div class="ui header"><h3>{{ $t('Secure Parameters (Write Only)') }}</h3></div>
    <div class="fields">
      <div class="five wide field">
        <label>{{ $t('Api Email') }}</label>
        <sui-input :placeholder="$t('Api Email')" v-model="value.api_email"/>
      </div>
      <div class="five wide field">
        <label>{{ $t('Api Password') }}</label>
        <sui-input :placeholder="$t('Api Password')" v-model="value.api_password"/>
      </div>
      <div class="five wide field">
        <label>{{ $t('Api Company') }}</label>
        <sui-input :placeholder="$t('Api Company')" v-model="value.api_company"/>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'paperlit-secure-parameters',
  props: ['value'],
  data() {
    return {};
  },
  computed: {
    parameters: () => {
      return {
        api_email: this.value.api_email,
        api_password: this.value.api_password,
        api_company: this.value.api_company,
      };
    },
  },
};
</script>

<style scoped>

</style>
