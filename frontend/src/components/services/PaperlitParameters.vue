<template>
  <div>
    <div class="ui header"><h3>{{ $t('Parameters') }}</h3></div>
    <div class="fields">
      <div class="five wide field">
        <label>{{ $t('Project Id') }}</label>
        <sui-input :placeholder="$t('Project Id')" v-model="value.project_id"/>
      </div>
      <div class="five wide field">
        <label>{{ $t('Publication Id') }}</label>
        <sui-input :placeholder="$t('Publication Id')" v-model="value.publication_id"/>
      </div>
    </div>
    <sui-form-field>
      <sui-checkbox :placeholder="$t('Default Paid')" v-model="value.default_paid" :label="$t('Default Paid')"/>
    </sui-form-field>
  </div>
</template>

<script>
export default {
  name: 'paperlit-parameters',
  props: ['value'],
  data() {
    return {};
  },
  computed: {
    parameters: () => {
      return {
        project_id: this.value.project_id,
        publication_id: this.value.publication_id,
        default_paid: this.value.default_paid,
      };
    },
  },
};
</script>

<style scoped>

</style>
