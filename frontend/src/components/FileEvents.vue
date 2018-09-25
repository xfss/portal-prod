<template>
  <div>
    <div class="ui large header">{{ $t('All files events') }}</div>
    <div class="row">
      <div class="column">
        <sui-table celled striped>
          <sui-table-header>
            <sui-table-row>
              <sui-table-header-cell>{{ $t('File') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Service') }}</sui-table-header-cell>
              <sui-table-header-cell textAlign="center">{{ $t('Publication') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Subject') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Details') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Timestamp') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Originator User') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Originator Service') }}</sui-table-header-cell>
              <sui-table-header-cell class="center aligned">{{ $t('Status') }}</sui-table-header-cell>
            </sui-table-row>
          </sui-table-header>

          <sui-table-body>
            <sui-table-row v-for="fileEvent in fileEvents" :key="fileEvent.id" :data-file-event-id="fileEvent.id">
              <sui-table-cell v-if="fileEvent.file">
                <router-link :to="{name: 'File Events', params: {id: fileEvent.file.id}}">
                  {{ fileEvent.file && fileEvent.file.filename }}
                </router-link>
              </sui-table-cell>
              <sui-table-cell v-else>
              </sui-table-cell>
              <sui-table-cell>{{ fileEvent.service && fileEvent.service.name }}</sui-table-cell>
              <sui-table-cell textAlign="center" class="single line" v-if="fileEvent.file && fileEvent.file.publication">{{ fileEvent.file && fileEvent.file.publication.name }}</sui-table-cell>
              <sui-table-cell textAlign="center" class="single line" v-else></sui-table-cell>
              <sui-table-cell>{{ fileEvent.subject }}</sui-table-cell>
              <sui-table-cell>{{ fileEvent.details }}</sui-table-cell>
              <sui-table-cell>{{ fileEvent.timestamp }}</sui-table-cell>
              <sui-table-cell>{{ fileEvent.originator_user && fileEvent.originator_user.username }}</sui-table-cell>
              <sui-table-cell>{{ fileEvent.originator_service && fileEvent.originator_service.name }}</sui-table-cell>
              <sui-table-cell class="center aligned">
                <i class="check icon large" v-if="fileEvent.status === 'Success'"></i>
                <i class="clock icon large" v-else-if="fileEvent.status === 'In progress'"></i>
                <i class="exclamation triangle icon large" v-else></i>
              </sui-table-cell>
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
    this.fetchFileEvents();
  },
  data() {
    return {
      fileEvents: []
    };
  },
  methods: {
    fetchFileEvents() {
      let client = this.$store.getters.coreapiClient;
      let action = ['status', 'fileEvent', 'list'];
      let schema = this.$store.getters.coreapiSchema;

      client.action(schema, action).then((result) => {
        this.fileEvents = result;
      });
    }
  }
};
</script>

<style scoped>

</style>
