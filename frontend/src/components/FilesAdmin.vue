<template>
  <div id="lp-files">
    <div class="ui large header">{{ $t('Files') }}</div>
    <div class="row">
      <div class="column">
        <sui-table celled striped compact="very">
          <sui-table-header>
            <sui-table-row>
              <sui-table-header-cell>{{ $t('Filename') }}</sui-table-header-cell>
              <sui-table-header-cell textAlign="center">{{ $t('Publication') }}</sui-table-header-cell>
              <sui-table-header-cell textAlign="center">{{ $t('Edition Date') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Created At') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Updated At') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Creator') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Updater') }}</sui-table-header-cell>
              <sui-table-header-cell textAlign="center">{{ $t('Status') }}</sui-table-header-cell>
              <sui-table-header-cell textAlign="center">{{ $t('Actions') }}</sui-table-header-cell>
            </sui-table-row>
          </sui-table-header>

          <sui-table-body>
            <sui-table-row v-for="file in files" :key="file.id">
              <sui-table-cell >{{ file.filename }}</sui-table-cell>
              <sui-table-cell textAlign="center" v-if="file.publication">{{ file.publication.name }}</sui-table-cell>
              <sui-table-cell textAlign="center" v-else></sui-table-cell>
              <sui-table-cell textAlign="center">{{ file.edition_date }}</sui-table-cell>
              <sui-table-cell>{{ file.created_at }}</sui-table-cell>
              <sui-table-cell>{{ file.updated_at }}</sui-table-cell>
              <sui-table-cell>{{ file.creator && file.creator.username }}</sui-table-cell>
              <sui-table-cell>{{ file.updater && file.updater.username }}</sui-table-cell>
              <sui-table-cell textAlign="center">
                <i class="check icon" v-if="file.status === 'Success'"></i>
                <i class="clock icon" v-else-if="file.status === 'In progress'"></i>
                <i class="exclamation triangle icon" v-else></i>
              </sui-table-cell>
              <sui-table-cell class="ui center aligned">
                <div class="ui compact pointing mini menu">
                  <a class="item" target="_blank" :href="file.file" title="Download">
                    <i class="icon download"></i>
                  </a>
                  <router-link class="item" :to="{name: 'Edit File', params: {id: file.id}}" title="Edit">
                    <i class="icon edit"></i>
                  </router-link>
                  <router-link class="item" :to="{name: 'File Events', params: {id: file.id}}">
                    <i class="icon list"></i> {{ $t('Events') }}
                    <div class="floating ui label">{{ file.event_number }}</div>
                  </router-link>
                </div>
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
    this.fetchFiles();
  },
  data() {
    return {
      files: []
    };
  },
  methods: {
    fetchFiles() {
      let client = this.$store.getters.coreapiClient;
      let action = ['status', 'file', 'list'];
      let schema = this.$store.getters.coreapiSchema;

      client.action(schema, action).then((result) => {
        // Return value is in 'result'
        this.files = result;
      });
    }
  }
};
</script>

<style scoped>

</style>
