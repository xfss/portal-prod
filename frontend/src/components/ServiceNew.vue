<template>
  <div>
    <div class="ui large header">{{ $t('Create new service') }}</div>
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
        <form v-on:submit.prevent="create" class="ui equal width form">
          <div class="basic vertical ui segment">
            <div class="two fields">
              <div class="field">
                <label>{{ $t('Name') }}</label>
                <sui-input :placeholder="$t('Name')" v-model="name"/>
              </div>
              <div class="field">
                <label>{{ $t('Address') }}</label>
                <sui-input :placeholder="$t('Address')" v-model="address"/>
              </div>
            </div>
            <div class="two fields">
              <div class="field">
                <label>{{ $t('Port') }}</label>
                <input type="number" :placeholder="$t('Port')" v-model.number="port"/>
              </div>
              <div class="field">
                <label>{{ $t('Filename Regex Pattern') }}</label>
                <sui-input :placeholder="$t('Filename Regex Pattern')" v-model="filename_pattern"/>
              </div>
            </div>
            <div class="field">
              <label>{{ $t('Type') }}</label>
              <sui-dropdown selection :options="type_options" v-model="type" />
            </div>
          </div>
          <div class="vertical segment ui" v-if="this.type === 1">
            <SftpParameters v-model="parameters" />
          </div>
          <div class="basic vertical segment ui" v-if="this.type === 1">
            <SftpSecureParameters v-model="secure_parameters" />
          </div>
          <div class="vertical segment ui" v-if="this.type === 2" >
            <AboDBParameters v-model="parameters" />
          </div>
          <div class="basic vertical segment ui" v-if="this.type === 2" >
            <AboDBSecureParameters v-model="secure_parameters" />
          </div>
          <div class="vertical segment ui" v-if="this.type === 3">
            <PaperlitParameters v-model="parameters" />
          </div>
          <div class="basic vertical segment ui" v-if="this.type === 3">
            <PaperlitSecureParameters v-model="secure_parameters" />
          </div>
          <sui-button type="submit">{{ $t('Create') }}</sui-button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import SftpParameters from './services/SftpParameters';
import SftpSecureParameters from './services/SftpSecureParameters';
import AboDBParameters from './services/AboDBParameters';
import AboDBSecureParameters from './services/AboDBSecureParameters';
import PaperlitParameters from './services/PaperlitParameters';
import PaperlitSecureParameters from './services/PaperlitSecureParameters';

export default {
  name: 'service-new',
  components: {SftpParameters, SftpSecureParameters, AboDBParameters, AboDBSecureParameters, PaperlitParameters, PaperlitSecureParameters},
  data() {
    return {
      name: '',
      address: '',
      port: '',
      filename_pattern: '',
      type: null,
      type_options: [
        {text: 'SFTP', value: 1},
        {text: 'AboDB', value: 2},
        {text: 'Paperlit', value: 3}
      ],
      parameters: {},
      secure_parameters: {},
      message: '',
      percentCompleted: null,
    };
  },
  methods: {
    processFile(event) {
      console.log('file selected!');
      this.file = event.target.files[0];
    },
    create(event) {
      let client = this.$store.getters.coreapiClient;
      let action = ['status', 'service', 'create'];
      let schema = this.$store.getters.coreapiSchema;
      let params = {
        name: this.name,
        address: this.address,
        port: this.port,
        filename_pattern: this.filename_pattern,
        type: this.type,
        parameters: this.parameters,
        secure_parameters: this.secure_parameters,
      };

      client.action(schema, action, params).then((result) => {
        this.message = this.$t('Success');
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
