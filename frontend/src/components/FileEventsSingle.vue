<template>
  <div class="ui grid" v-if="currentFile !== ''">
    <div class="row">
      <div class="column">
        <div class="ui large header">{{ $t('File events') }}</div>
      </div>
    </div>
    <div class="row">
      <div class="column">
        <sui-breadcrumb>
          <sui-breadcrumb-section>
            <router-link :to="{ name: 'Files' }">{{ $t('Files') }}</router-link>
          </sui-breadcrumb-section>
          <sui-breadcrumb-divider icon="right chevron" />
          <sui-breadcrumb-section>
            <router-link :to="{ name: 'Edit File', params: { id: this.$route.params.id } }">{{ this.$route.params.id }}</router-link>
          </sui-breadcrumb-section>
          <sui-breadcrumb-divider icon="right chevron" />
          <sui-breadcrumb-section active>{{ this.$route.name }}</sui-breadcrumb-section>
        </sui-breadcrumb>
      </div>
    </div>
    <div class="row">
      <div class="column">
        <div class="ui large header"><h4>{{ currentFile }}</h4></div>
        <sui-table celled striped>
          <sui-table-header>
            <sui-table-row>
              <sui-table-header-cell>{{ $t('Service') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Subject') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Details') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Timestamp') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Originator User') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Originator Service') }}</sui-table-header-cell>
              <sui-table-header-cell class="center aligned">{{ $t('Status') }}</sui-table-header-cell>
            </sui-table-row>
          </sui-table-header>

          <sui-table-body>
            <sui-table-row v-for="fileEvent in fileEvents" :key="fileEvent.id">
              <sui-table-cell >{{ fileEvent.service && fileEvent.service.name }}</sui-table-cell>
              <sui-table-cell>{{ fileEvent.subject }}</sui-table-cell>
              <sui-table-cell>{{ fileEvent.details }}</sui-table-cell>
              <sui-table-cell>{{ fileEvent.timestamp }}</sui-table-cell>
              <sui-table-cell >{{ fileEvent.originator_user && fileEvent.originator_user.username }}</sui-table-cell>
              <sui-table-cell >{{ fileEvent.originator_service && fileEvent.originator_service.name }}</sui-table-cell>
              <sui-table-cell class="center aligned">
                <i class="check icon" v-if="fileEvent.status === 'Success'"></i>
                <i class="clock icon" v-else-if="fileEvent.status === 'In progress'"></i>
                <i class="exclamation triangle icon" v-else></i>
              </sui-table-cell>
            </sui-table-row>
          </sui-table-body>
        </sui-table>
      </div>
    </div>
  </div>
  <div v-else class="ui large header">{{ message }}</div>
</template>

<script>

export default {
  created() {
    this.fetchFileEvents();
  },
  watch: {
    '$route': 'fetchFileEvents'
  },
  data() {
    return {
      fileEvents: [],
      currentFile: '',
      message: ''
    };
  },
  methods: {
    getDate(dateStr) {
      return this.$d(new Date(dateStr), 'long');
    },
    fetchFileEvents() {
      let client = this.$store.getters.coreapiClient;
      let action = ['status', 'file', 'events'];
      let schema = this.$store.getters.coreapiSchema;
      let params = {
        id: this.$route.params.id,
      };

      client.action(schema, action, params).then((result) => {
        let status = '';
        // The `events` endpoint returns an array with child objects
        if ((!!result) && (result.constructor === Array)) {
          status = result[0].status;
        } else {
          // When no events are found, we are returning a non-array object
          status = result.status;
        }
        switch (status.toLowerCase()) {
          case 'success':
          case 'error':
            this.fileEvents = result;
            this.currentFile = result[0].file.filename;
            break;
          case 'not found':
            this.message = result.message;
            this.currentFile = '';
            break;
          default:
        }
      });
    }
  }
};
</script>

<style scoped>

</style>
