<template>
  <div>
    <div class="ui large header">{{ $t('Services') }}</div>
    <div class="row">
      <div class="column">
        <sui-table celled striped>
          <sui-table-header>
            <sui-table-row>
              <sui-table-header-cell v-if="currentUser.data.is_staff"></sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Name') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Address') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Port') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Created At') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Updated At') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Creator') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Updater') }}</sui-table-header-cell>
              <sui-table-header-cell>{{ $t('Status') }}</sui-table-header-cell>
            </sui-table-row>
          </sui-table-header>

          <sui-table-body>
            <sui-table-row v-for="service in services" :key="service.id">
              <sui-table-cell class="ui center aligned" v-if="currentUser.data.is_staff">
                <router-link :to="{name: 'Edit Service', params: {id: service.id}}">
                  <i class="edit icon"></i>
                </router-link>
              </sui-table-cell>
              <sui-table-cell >{{ service.name }}</sui-table-cell>
              <sui-table-cell>{{ service.address }}</sui-table-cell>
              <sui-table-cell>{{ service.port }}</sui-table-cell>
              <sui-table-cell>{{ service.created_at }}</sui-table-cell>
              <sui-table-cell>{{ service.updated_at }}</sui-table-cell>
              <sui-table-cell>{{ service.creator && service.creator.username }}</sui-table-cell>
              <sui-table-cell>{{ service.updater && service.updater.username }}</sui-table-cell>
              <sui-table-cell class="center aligned" v-bind:class="{positive: service.status === 'Up', negative: service.status === 'Down'}" >{{ service.status }}</sui-table-cell>
            </sui-table-row>
          </sui-table-body>
        </sui-table>
      </div>
    </div>
  </div>
</template>

<script>
import {mapGetters} from 'vuex';

export default {
  created() {
    this.fetchServices();
  },
  data() {
    return {
      services: []
    };
  },
  computed: {
    ...mapGetters([
      'currentUser',
    ])
  },
  methods: {
    fetchServices() {
      let client = this.$store.getters.coreapiClient;
      let action = ['status', 'service', 'list'];
      let schema = this.$store.getters.coreapiSchema;
      client.action(schema, action).then((result) => {
        this.services = result;
      });
    }
  }
};
</script>

<style scoped>

</style>
