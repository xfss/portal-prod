<template>
  <div id="lp-files">
    <div class="ui large header">{{ $t('Publications') }}</div>
    <div class="row">
      <div class="column">
        <sui-table celled striped compact="very">
          <sui-table-header>
            <sui-table-row>
              <sui-table-header-cell>{{ $t('Code') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Name') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Language') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Timezone') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Role') }}</sui-table-header-cell>
              <sui-table-header-cell textAlign="center">{{ $t('Actions') }}</sui-table-header-cell>
            </sui-table-row>
          </sui-table-header>

          <sui-table-body>
            <sui-table-row v-for="publication in publications" :key="publication.id">
              <sui-table-cell >{{ publication.code }}</sui-table-cell>
              <sui-table-cell >{{ publication.name }}</sui-table-cell>
              <sui-table-cell >{{ publication.language_name }}</sui-table-cell>
              <sui-table-cell >{{ publication.timezone_name }}</sui-table-cell>
              <sui-table-cell >{{ publication.role }}</sui-table-cell>
              <sui-table-cell class="ui center aligned">
                <div class="ui compact pointing mini menu" v-if="publication.role === 'Admin'">
                  <router-link class="item" :to="{name: 'Edit Publication', params: {id: publication.id}}" title="Edit">
                    <i class="icon edit"></i>
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
    this.fetchPublications();
  },
  data() {
    return {
      publications: []
    };
  },
  methods: {
    fetchPublications() {
      let client = this.$store.getters.coreapiClient;
      let action = ['publication', 'list'];
      let schema = this.$store.getters.coreapiSchema;

      client.action(schema, action).then((result) => {
        this.publications = result;
      });
    }
  }
};
</script>

<style scoped>

</style>
