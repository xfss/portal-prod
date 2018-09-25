<template>
  <div>
    <div class="ui large header">{{ $t('Edit Publication') }}</div>
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
        <form v-on:submit.prevent="update" class="ui form">
          <div class="basic vertical ui segment">
            <div class="fields">
              <div class="five wide field">
                <label>{{ $t('Name') }}</label>
                <sui-input :placeholder="$t('Name')" v-model="name"/>
              </div>
              <div class="one wide field">
                <label>{{ $t('Code') }}</label>
                <sui-input :placeholder="$t('Code')" v-model="code"/>
              </div>
            </div>
            <div class="two fields">
              <div class="six wide field">
                <label>{{ $t('Filename Regex Pattern') }}</label>
                <sui-input :placeholder="$t('Filename Regex Pattern')" v-model="filename_pattern"/>
              </div>
            </div>
          </div>
          <div class="fields">
            <div class="three wide field">
              <label>{{ $t('Language') }}</label>
              <sui-dropdown search selection :options="languages" v-model="language" />
            </div>
            <div class="three wide field">
              <label>{{ $t('Timezone') }}</label>
              <sui-dropdown search selection :options="timezones" v-model="timezone" />
            </div>
          </div>
          <sui-button type="submit">{{ $t('Update') }}</sui-button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import {mapGetters} from 'vuex';
let schema = null;

export default {
  name: 'publication-edit',
  components: {},
  data() {
    return {
      name: '',
      code: '',
      language: '',
      timezone: '',
      filename_pattern: '',
      message: '',
    };
  },
  computed: {
    ...mapGetters([
      'languages',
      'timezones',
    ]),
  },
  created() {
    schema = this.$store.getters.coreapiSchema;
    this.fetchPublication();
  },
  watch: {
    '$route': 'fetchPublication'
  },
  methods: {
    fetchPublication() {
      let client = this.$store.getters.coreapiClient;
      let action = ['publication', 'read'];
      let params = {
        id: this.$route.params.id,
      };
      client.action(schema, action, params).then((result) => {
        this.name = result.name;
        this.code = result.code;
        this.language = result.language;
        this.timezone = result.timezone ? result.timezone.toString() : null;
        this.filename_pattern = result.filename_pattern;
      });
    },
    update(event) {
      let client = this.$store.getters.coreapiClient;

      let action = ['publication', 'partial_update'];
      let params = {
        id: this.$route.params.id,
        name: this.name,
        code: this.code,
        language: this.language,
        timezone: this.timezone,
        filename_pattern: this.filename_pattern,
      };

      client.action(schema, action, params).then((result) => {
        this.message = 'Success';
        this.secure_parameters = {};
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
