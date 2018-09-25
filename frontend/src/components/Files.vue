<template>
  <div id="lp-files">
    <div class="ui large header">{{ $t('Files') }}</div>
    <div class="row">
      <div class="column">
        <div class="ui grid">
          <div class="row file-events-container">
            <div class="column">
              <div class="row file-event-row" v-for="file in files" :key="file.id" v-bind:class="{ show: displayFileEvents(file.id) }">
                <div class="ui three column grid padded">
                  <div class="row">
                    <div class="column twelve wide">
                      <h4 v-if="file.publication">{{ file.publication.name }} | {{ file.category }} for <span v-if="file.edition">{{ file.edition.date }}</span></h4>
                    </div>
                    <div class="column one wide">
                      <i class="check icon fitted green big" v-if="file.status === 'Success'"></i>
                      <i class="clock icon fitted big" v-else-if="file.status === 'In progress'"></i>
                      <i class="exclamation fitted triangle icon red big" v-else></i>
                    </div>
                    <div class="column three wide file-event-show-column" v-bind:class="[{ show: displayFileEvents(file.id) }]">
                      <button class="ui secondary button" v-on:click="fetchEvents(file.id, $event)" v-bind:class="[ buttonLoading(file.id) ? 'loading disabled' : '', displayFileEvents(file.id) ? 'primary' : 'basic']">
                        <span v-if="displayFileEvents(file.id)">
                          <i class="icon minus square"></i> {{ $t('Close Events') }}
                        </span>
                        <span v-else>
                          <i class="icon list"></i> {{ $t('View Events') }}
                        </span>
                      </button>
                    </div>
                  </div>
                  <sui-grid-row class="file-events" v-bind:class="[{ show: displayFileEvents(file.id) }, 'file-event-'+file.id]">
                    <div class="column sixteen wide">
                      <div class="row">
                        <div class="column wide sixteen">
                          <div class="ui grid padded">
                            <sui-grid-row class="file-event-row-header blue" v-bind:id="'file-event-row-header-' + file.id ">
                              <sui-grid-column :width="4">{{ $t('What') }}</sui-grid-column>
                              <sui-grid-column :width="4">{{ $t('Where') }}</sui-grid-column>
                              <sui-grid-column :width="4">{{ $t('Status') }}</sui-grid-column>
                              <sui-grid-column :width="4">{{ $t('Time') }}</sui-grid-column>
                            </sui-grid-row>
                            <div class="row file-event-row-body">
                              <div class="grid ui padded">
                                <div class="row" v-for="event in getFileEvents(file.id)" :key="event.id">
                                  <sui-grid-column :width="4">{{ event.subject }}</sui-grid-column>
                                  <sui-grid-column :width="4">
                                    <span v-if="event.service">{{ event.service.friendly_name }}</span>
                                    <span v-else-if="event.subject === 'File Upload'">{{ $t('Portal') }}</span>
                                  </sui-grid-column>
                                  <sui-grid-column :width="4">
                                    <i class="check icon green" v-if="event.status === 'Success'"></i>
                                    <i class="clock icon" v-else-if="event.status === 'In progress'"></i>
                                    <i class="exclamation triangle icon red" v-else></i>
                                  </sui-grid-column>
                                  <sui-grid-column :width="4">{{ event.timestamp }}</sui-grid-column>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </sui-grid-row>
                </div>
              </div>
            </div>
          </div>
        </div>
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
      files: [],
      fileEvents: {},
      events: {}
    };
  },
  methods: {
    getFileEvents: function (id) {
      return this.events[id].data;
    },
    displayFileEvents: function (id) {
      return this.events[id].show;
    },
    buttonLoading: function (id) {
      if (Object.keys(this.events[id]).length !== 0) {
        return this.events[id].loading;
      }
      return false;
    },
    showFileEvents(id) {
      this.$nextTick(function () {
        this.events[id].loading = false;
        let el = document.querySelector('.file-event-' + id);
        let children = el.children[0].childNodes;
        let height = 0;
        for (var i = 0; i < children.length; i++) {
          if (children[i].className === 'row') {
            height += children[i].clientHeight;
          }
        }
        this.events[id].show = !this.events[id].show;
        if (this.events[id].show) {
          el.style.height = (height > 325 ? 325 : (height + 10)) + 'px';
        } else {
          el.style.height = '0px';
        }
      });
    },
    fetchFiles() {
      let client = this.$store.getters.coreapiClient;
      let action = ['status', 'file', 'list'];
      let schema = this.$store.getters.coreapiSchema;

      client.action(schema, action).then((result) => {
        // Return value is in 'result'
        this.files = result;
        for (var i = 0; i < result.length; i++) {
          let data = {
            show: false,
            loading: false,
            data: []
          };
          this.$set(this.events, result[i].id, data);
        }
      });
    },
    fetchEvents: function (id, event) {
      if (!this.events[id].loading) {
        this.events[id].loading = true;
        if (Object.keys(this.events[id].data).length === 0) {
          let client = this.$store.getters.coreapiClient;
          let action = ['status', 'file', 'events'];
          let schema = this.$store.getters.coreapiSchema;
          // Channels:
          //  0: File Upload
          //  1: File processing
          //  3: Edition published
          let params = {
            id: id,
            channel__in: [0, 1, 3]
          };

          client.action(schema, action, params).then((result) => {
            this.$set(this.events[id], 'data', result);
            this.showFileEvents(id);
          });
        } else {
          this.showFileEvents(id);
        }
      }
    }
  }
};
</script>

<style scoped>
.file-event-row h4,
.file-event-row h5 {
  margin: 0;
}
.ui.grid {
  width: 100%;
}
</style>
