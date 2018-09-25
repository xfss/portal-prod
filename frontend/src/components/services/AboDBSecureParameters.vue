<template>
  <div>
    <div class="ui header"><h3>{{ $t('Secure Parameters (Write Only)') }}</h3></div>
    <div class="two fields">
      <sui-form-field>
        <label>{{ $t('Username') }}</label>
        <sui-input :placeholder="$t('Username')" v-model="value.username"/>
      </sui-form-field>
      <sui-form-field>
        <label>{{ $t('Api Key') }}</label>
        <sui-input :placeholder="$t('Api Key')" v-model="value.api_key"/>
      </sui-form-field>
    </div>
  </div>
</template>

<script>
export default {
  name: 'abodb-secure-parameters',
  props: ['value'],
  data() {
    return {};
  },
  computed: {
    parameters: () => {
      return {
        api_key: this.value.api_key,
      };
    },
  },
};
</script>

<style scoped>

</style>
