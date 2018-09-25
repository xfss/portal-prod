<template>
  <div>
    <div class="ui header"><h3>{{ $t('Parameters') }}</h3></div>
    <sui-form-field>
      <label>{{ $t('Publisher Code') }}</label>
      <sui-input :placeholder="$t('Publisher Code')" v-model="value.publisher_code"/>
    </sui-form-field>
  </div>
</template>

<script>
export default {
  name: 'abodb-parameters',
  props: ['value'],
  data() {
    return {};
  },
  computed: {
    parameters: () => {
      return {
        publisher_code: this.value.publisher_code,
      };
    },
  },
};
</script>

<style scoped>

</style>
