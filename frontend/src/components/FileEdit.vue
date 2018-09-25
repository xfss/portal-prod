<template>
  <div class="ui grid">
    <div class="row">
      <div class="column">
        <div class="ui large header">{{ $t('Edit uploaded file') }}</div>
      </div>
    </div>
    <div class="row">
      <div class="column">
        <sui-breadcrumb>
          <sui-breadcrumb-section>
            <router-link :to="{ name: 'Files' }">{{ $t('Files') }}</router-link>
          </sui-breadcrumb-section>
          <sui-breadcrumb-divider icon="right chevron" />
          <sui-breadcrumb-section active>{{ this.$route.params.id }}</sui-breadcrumb-section>
        </sui-breadcrumb>
      </div>
    </div>
    <div class="row">
      <div class="column">
        <sui-message class="positive message" v-show="message">
          <sui-message-header>{{ message }}</sui-message-header>
          <i class="close icon" v-on:click="clearMessage"></i>
        </sui-message>
      </div>
    </div>
    <div class="row">
      <div class="column">
        <form class="ui form" v-bind:class="[success ? 'success' : 'error']" v-on:submit.prevent="update">
          <sui-form-field>
            <label>{{ $t('File name') }}</label>
            <sui-input :placeholder="$t('File name')" v-model="filename"/>
          </sui-form-field>
          <sui-form-field>
            <label>{{ $t('File') }}</label>
            <input type="file" :placeholder="$t('File')" @change="processFile($event)">
          </sui-form-field>
          <sui-button type="submit">{{ $t('Update') }}</sui-button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'file-edit',
  data() {
    return {
      filename: null,
      file: null,
      currentFile: null,
      message: '',
      success: null,
      percentCompleted: null,
    };
  },
  created() {
    this.fetchFile();
  },
  watch: {
    '$route': 'fetchFile'
  },
  methods: {
    processFile(event) {
      console.log('file selected!');
      this.file = event.target.files[0];
    },
    fetchFile() {
      let action = ['status', 'file', 'read'];
      let params = {
        id: this.$route.params.id,
      };

      let client = this.$store.getters.coreapiClient;
      let schema = this.$store.getters.coreapiSchema;
      client.action(schema, action, params).then((result) => {
        this.filename = result.filename;
        this.currentFile = result.file;
      });
    },
    update(event) {
      let data = new FormData();
      if (this.filename) {
        data.append('filename', this.filename);
      }
      if (this.file) {
        data.append('file', this.file);
      }

      let config = {
        onUploadProgress: function (progressEvent) {
          this.percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        }
      };

      let axiosClient = this.$store.getters.axiosClient;
      axiosClient.patch(`status/file/${this.$route.params.id}/`, data, config).then((response) => {
        this.message = this.$t('Success!');
      });
    },
    clearMessage() {
      this.message = '';
    }
  }
};
</script>

<style scoped>

</style>
