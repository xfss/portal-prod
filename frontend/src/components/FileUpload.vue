<template>
  <div>
    <div class="ui large header">{{ $t('File upload') }}</div>
    <div class="row">
      <div class="column">
        <form class="ui form" v-bind:class="[operationStatus ? operationStatus : '']" v-on:submit.prevent="upload">
          <div class="field" v-if="availablePublications">
            <label>{{ $t('Publication') }}</label>
            <sui-dropdown selection :options="availablePublications" v-model="publication" />
          </div>
          <div class="field">
            <label>{{ $t('File') }}</label>
            <input type="file" @change="processFile($event)">
          </div>
          <sui-button type="submit">{{ $t('Upload') }}</sui-button>
          <div class="ui message" v-bind:class="[operationStatus ? operationStatus : '']" v-html="message">{{ message }}</div>
        </form>
        <sui-divider hidden />
        <div v-if="percentCompleted">
          <sui-progress
            :color="uploadColor"
            progress
            :indicating="uploadProcessing"
            :state="uploadState"
            :percent="percentCompleted"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {mapGetters} from 'vuex';

export default {
  name: 'file-upload',
  data() {
    return {
      availablePublications: null,
      // Warn if publication is being upload more than X days in advance
      publicationPreDateWarning: 3,
      publication: null,
      currentEpochTS: null,
      message: '',
      operationStatus: 'success',
      percentCompleted: 0,
      uploadColor: 'grey',
      uploadState: 'active',
      uploadProcessing: false,
    };
  },
  computed: {
    ...mapGetters([
      'publicationOptions',
    ]),
  },
  methods: {
    resetUpload(event) {
      this.operationStatus = 'error';
      this.publication = null;
      this.availablePublications = null;
      this.file = null;
      event.target.value = '';
    },
    validateFileDate(event) {
      let ext = this.file.name.split('.')[this.file.name.split('.').length - 1];
      if (ext.match(/pdf/gi)) {
        let currentLocalDate = new Date();
        this.currentEpochTS = Date.UTC(
          currentLocalDate.getUTCFullYear(),
          currentLocalDate.getUTCMonth(),
          currentLocalDate.getUTCDate(),
          0, 0, 0
        );
        let fileDate = this.file.name.match(/(\d{8})(?=_)/);
        if (!fileDate) {
          this.message = this.$t(
            'The selected file "' + this.file.name + '" does not have a ' +
            'recognizable date in the file name. ' +
            'Please correct the file name.'
          );
          this.resetUpload(event);
          return;
        }
        // Add dashes for creating Date object
        fileDate = fileDate[0].substr(0, 4) + '-' +
                   fileDate[0].substr(4, 2) + '-' +
                   fileDate[0].substr(6, 2);
        let filePubDate = new Date(fileDate);
        this.filePubEpochTS = Date.UTC(
          filePubDate.getUTCFullYear(),
          filePubDate.getUTCMonth(),
          filePubDate.getUTCDate(),
          0, 0, 0
        );

        if (this.filePubEpochTS < this.currentEpochTS) {
          this.message = this.$t(
            'Files for Editions with a date in the ' +
            'past cannot be uploaded. Selected file: "' + this.file.name + '"'
          );
          this.resetUpload(event);
          return;
        }
      }
      return true;
    },
    processFile(event) {
      this.message = '';
      this.operationStatus = 'success';
      this.file = event.target.files[0];
      this.percentCompleted = 0;
      let ext = this.file.name.split('.')[this.file.name.split('.').length - 1];
      let validFileDate = this.validateFileDate(event);
      if (!validFileDate) {
        return;
      }
      let patternMatchedPublications = [];
      let publications = this.$store.getters.currentUser.data.publications;
      if (publications) {
        for (let item of publications) {
          if (item.pattern) {
            let regex = new RegExp(item.pattern, 'gi');
            if (regex.test(this.file.name)) {
              patternMatchedPublications.push(item);
            }
          }
        }
        this.availablePublications = this.$store.getters.publicationOptions;
        if (patternMatchedPublications.length === 0) {
          this.message = this.$t('The selected file\'s name does not match ' +
                                 'any known publication.');
          this.operationStatus = 'warning';
          this.publication = null;
        }
        if (patternMatchedPublications.length === 1) {
          this.publication = patternMatchedPublications[0]['id'];
          if (ext.match(/pdf/gi)) {
            this.checkEditionSchedule(
              this.filePubEpochTS, this.currentEpochTS, patternMatchedPublications[0]
            );
          }
        }
      }
    },
    checkEditionSchedule(pubDateEpoch, currentDateEpoch, publication) {
      let pubDate = new Date(pubDateEpoch);
      let scheduledDays = publication.scheduled_days;
      // Schedule is sent from the publication settings.
      // JS uses "Sunday" as the first day of the week instead
      // of the usual "Monday".
      let jsWeekdayAdjust = {};
      for (let i = 0; i < 7; i++) {
        if (i === 0) {
          jsWeekdayAdjust[i] = 6;
        } else {
          jsWeekdayAdjust[i] = i - 1;
        }
      }
      if (scheduledDays.length > 0) {
        if (scheduledDays.indexOf(jsWeekdayAdjust[pubDate.getUTCDay()]) === -1) {
          this.message = this.$t('The Edition day for the selected file does not ' +
                                 'match the usual schedule for "' + publication.name + '".<br>');
          this.operationStatus = 'warning';
        }
      }
      let dayDiff = (pubDateEpoch - currentDateEpoch) / 1000 / 60 / 60 / 24;
      if (dayDiff > this.publicationPreDateWarning) {
        this.operationStatus = 'warning';
        this.message += this.$t('The Edition date for the selected file ' +
                                'is for ' + Math.ceil(dayDiff) + ' days from now.<br>');
      }
      if (this.operationStatus === 'warning') {
        this.message += this.$t('Please be sure this is the correct file to be uploaded. ');
      }
    },
    validateSubmit() {
      this.message = '';
      this.operationStatus = 'success';
      if (!this.file) {
        this.message = this.$t('Please select a file to upload');
        this.operationStatus = 'error';
      } else if (!this.publication) {
        this.message = this.$t('Please select a publication');
        this.operationStatus = 'error';
      }
      return this.operationStatus;
    },
    upload(event) {
      let valid = this.validateSubmit();
      if (valid !== 'success') {
        return;
      }
      this.percentCompleted = 0;
      this.uploadColor = 'grey';
      this.uploadState = 'active';
      let _self = this;
      let axiosClient = this.$store.getters.axiosClient;
      let data = new FormData();
      data.append('file', this.file);
      if (this.publication) {
        data.append('publication', this.publication);
      }

      let config = {
        onUploadProgress: function (progressEvent) {
          let completed = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          if (completed >= 25 && completed < 50) {
            _self.uploadColor = 'blue';
          } else if (completed >= 50 && completed < 75) {
            _self.uploadColor = 'teal';
          } else if (completed >= 75 && completed < 100) {
            _self.uploadColor = 'olive';
          } else if (completed >= 100) {
            _self.uploadColor = 'green';
            _self.uploadProcessing = true;
          }
          _self.percentCompleted = completed;
        }
      };

      axiosClient.post('status/file/', data, config).then((response) => {
        this.message = this.$t('Success!');
        this.operationStatus = 'success';
        this.$router.push({ name: 'Files' });
      }).catch((error) => {
        this.operationStatus = 'error';
        this.uploadState = 'error';
        if (error.response || error.request) {
          this.message = error.message;
        } else {
          console.log('Error', error.message);
        }
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
