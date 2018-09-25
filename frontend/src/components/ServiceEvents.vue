<template>
  <div>
    <div class="ui large header">{{ $t('Services') }}</div>
    <div class="row">
      <div class="column">
        <sui-table celled striped>
          <sui-table-header>
            <sui-table-row>
              <sui-table-header-cell>{{ $t('Service') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Details') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Timestamp') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Originator User') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Status') }}</sui-table-header-cell>
            </sui-table-row>
          </sui-table-header>

          <sui-table-body>
            <sui-table-row v-for="serviceEvent in serviceEvents" :key="serviceEvent.id">
              <sui-table-cell >{{ serviceEvent.service && serviceEvent.service.name }}</sui-table-cell>
              <sui-table-cell>{{ serviceEvent.details }}</sui-table-cell>
              <sui-table-cell>{{ serviceEvent.timestamp }}</sui-table-cell>
              <sui-table-cell>{{ serviceEvent.originator_user && serviceEvent.originator_user.username }}</sui-table-cell>
              <sui-table-cell class="center aligned" v-bind:class="{positive: serviceEvent.status === 'Up', negative: serviceEvent.status === 'Down'}" >{{ serviceEvent.status }}</sui-table-cell>
            </sui-table-row>
          </sui-table-body>
        </sui-table>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  created() {
    this.fetchServiceEvents();
  },
  data() {
    return {
      serviceEvents: []
    };
  },
  methods: {
    fetchServiceEvents() {
      let client = this.$store.getters.coreapiClient;
      let action = ['status', 'serviceEvent', 'list'];
      let schema = this.$store.getters.coreapiSchema;

      client.action(schema, action).then((result) => {
        // Return value is in 'result'
        this.serviceEvents = result;
      });
    }
  }
};
</script>

<style scoped>

</style>
