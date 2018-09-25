<template>
  <div>
    <div class="ui header"><h3>{{ $t('Parameters') }}</h3></div>
    <sui-form-field>
      <label>{{ $t('Target Directory') }}</label>
      <sui-input :placeholder="$t('Target Directory')" v-model="value.target_directory"/>
    </sui-form-field>
    <sui-form-field>
      <sui-checkbox :placeholder="$t('Create Subdirectory')" v-model="value.create_subdirectory" label="Create Subdirectory"/>
    </sui-form-field>
  </div>
</template>

<script>
export default {
  name: 'sftp-parameters',
  props: ['value'],
  data() {
    return {};
  },
  computed: {
    parameters: () => {
      return {
        target_directory: this.value.target_directory,
        create_subdirectory: this.value.create_subdirectory,
      };
    },
  },
};
</script>

<style scoped>

</style>
