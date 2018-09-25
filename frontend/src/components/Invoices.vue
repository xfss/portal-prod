<template>
  <div id="lp-invoices">
    <div class="ui large header">{{ $t('Invoices') }}</div>
    <div class="row">
      <div class="column">
        <div class="ui grid">
          <div class="row">
            <div class="four wide column">
              <button class="ui right labeled icon button" v-on:click="createInvoice()">
                <i class="right plus icon"></i> {{ $t('Create Invoice') }}
              </button>
            </div>
          </div>
          <sui-grid-row class="">
            <div class="column sixteen wide">
              <div class="row">
                <div class="column wide sixteen">
                  <div class="ui grid padded">
                    <sui-grid-row class="invoice-header">
                      <sui-grid-column :width="2">{{ $t('Invoice Number') }}</sui-grid-column>
                      <sui-grid-column :width="3">{{ $t('Publisher') }}</sui-grid-column>
                      <sui-grid-column :width="3">{{ $t('Publication') }}</sui-grid-column>
                      <sui-grid-column :width="2">{{ $t('Product') }}</sui-grid-column>
                      <sui-grid-column :width="3">{{ $t('Invoice Date') }}</sui-grid-column>
                      <sui-grid-column :width="3">{{ $t('Status') }}</sui-grid-column>
                    </sui-grid-row>
                    <div class="row invoice-row" v-for="item in invoices" :key="item.invoice.id" v-bind:class="[{ expanded: expandInvoice(item.invoice.id) }]" v-bind:id="'invoice-row-'+item.invoice.id">
                      <div class="grid ui padded">
                        <div class="row invoice-row-main valign-child-center" v-bind:class="[getUpdatedState(item.invoice.id) ? 'saved' : '']">
                          <sui-grid-column :width="2">{{ item.invoice.invoice_number }}</sui-grid-column>
                          <sui-grid-column :width="3">{{ item.invoice.publisher.name }}</sui-grid-column>
                          <sui-grid-column :width="3">{{ item.invoice.publications.map(p => p.code.toUpperCase()).join(', ') }}</sui-grid-column>
                          <sui-grid-column :width="2">{{ item.invoice.product }}</sui-grid-column>
                          <sui-grid-column :width="3">{{ item.invoice.invoice_date }}</sui-grid-column>
                          <sui-grid-column :width="2">
                            <i class="large clock icon" v-if="getStatus(item.invoice.id) === 'pending'"></i>
                            <i class="large check icon" v-else-if="getStatus(item.invoice.id) === 'paid'"></i>
                            <i class="large minus circle icon" v-else-if="getStatus(item.invoice.id) === 'cancelled'"></i>
                          </sui-grid-column>
                          <sui-grid-column :width="1">
                            <span class="expand-invoice-row" v-on:click="expand(item.invoice.id, $event)">
                              <i class="caret down icon"></i>
                            </span>
                          </sui-grid-column>
                        </div>
                        <div class="grid ui row padded stackable invoice-extra" v-bind:id="'invoice-extra-'+item.invoice.id">
                          <div class="row equal width invoice-row-extra">
                            <div class="column valign-child-center">
                              <table class="ui celled striped table">
                                <tbody>
                                  <tr>
                                    <td class="collapsing">
                                      <i class="calendar icon"></i> {{ $t('From') }}
                                    </td>
                                    <td>{{ item.invoice.invoice_start_date }}</td>
                                  </tr>
                                  <tr>
                                    <td>
                                      <i class="calendar icon"></i> {{ $t('To') }}
                                    </td>
                                    <td>{{ item.invoice.invoice_end_date }}</td>
                                  </tr>
                                  <tr>
                                    <td>
                                      <i class="calendar icon"></i> {{ $t('Due') }}
                                    </td>
                                    <td>{{ item.invoice.invoice_due_date }}</td>
                                  </tr>
                                </tbody>
                              </table>
                            </div>
                            <div class="column">
                              <table class="ui celled striped table">
                                <tbody>
                                  <tr>
                                    <td class="collapsing">
                                      <div class="ui labeled button" tabindex="0">
                                        <button class="ui right icon button" v-on:click="updateInvoiceStatus(item.invoice.id)" v-bind:class="[!statusChanged(item.invoice.id) ? 'red' : '']">
                                          {{ $t('Save') }}
                                        </button>
                                        <sui-dropdown
                                          placeholder="Status"
                                          selection
                                          fluid
                                          :options="item.options"
                                          v-model="item.statusValue"
                                          v-bind:id="'invoice-update-status-' + item.invoice.id"
                                        />
                                      </div>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                            </div>
                            <div class="column">
                              <table class="ui celled striped table">
                                <tbody>
                                  <tr>
                                    <td class="collapsing">
                                      <button class="ui right labeled icon button teal invoice" v-on:click.prevent="open(item.invoice.id)" v-bind:class="[invoiceLoading(item.invoice.id) ? 'loading' : '']">
                                        <i class="right eye icon"></i> {{ $t('View') }}
                                      </button>
                                    </td>
                                  </tr>
                                  <tr>
                                    <td class="collapsing">
                                      <a class="ui right labeled icon button teal invoice" v-bind:href="item.invoice.document" target="_blank">
                                        <i class="right download icon"></i> {{ $t('Download') }}
                                      </a>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                            </div>
                          </div>
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
    <sui-modal v-model="openInvoice" size="fullscreen" aligned="top" closeIcon>
      <sui-modal-header>{{ currentInvoice }}</sui-modal-header>
      <sui-modal-content>
        <iframe frameborder="0" width="100" height="100" id="invoice-view"></iframe>
      </sui-modal-content>
    </sui-modal>
  </div>
</template>

<script>

export default {
  created() {
    this.fetchInvoices();
  },
  data() {
    return {
      invoices: {},
      openInvoice: false,
      currentInvoice: ''
    };
  },
  methods: {
    notifySaved(id) {
      let self = this;
      this.invoices[id].statusChanged = true;
      setTimeout(function () {
        self.invoices[id].statusChanged = false;
      }, 2000);
    },
    getUpdatedState(id) {
      return this.invoices[id].statusChanged;
    },
    getStatus(id) {
      return this.invoices[id].statusValue;
    },
    statusChanged(id) {
      let currentStatus = this.invoices[id].invoice.status;
      let newStatus = this.invoices[id].statusValue;
      return newStatus === currentStatus;
    },
    updateInvoiceStatus(id) {
      let el = document.getElementById('invoice-update-status-' + id);
      let value = el.childNodes[0].innerText.toLowerCase();
      let client = this.$store.getters.coreapiClient;
      let action = ['crm', 'invoice', 'update'];
      let schema = this.$store.getters.coreapiSchema;
      let params = {
        id: id,
        status: value
      };
      client.action(schema, action, params).then((result) => {
        this.invoices[id].invoice = result;
        this.invoices[id].statusValue = result.status;
        this.statusChanged(id);
        this.notifySaved(id);
      });
    },
    invoiceLoading(id) {
      return this.invoices[id].loading;
    },
    open(id) {
      let el = document.getElementById('invoice-view');
      let client = this.$store.getters.coreapiClient;
      let action = ['crm', 'invoice', 'html'];
      let schema = this.$store.getters.coreapiSchema;
      let params = {
        id: id
      };
      this.invoices[id].loading = true;
      client.action(schema, action, params).then((result) => {
        el.src = 'about:blank';
        setTimeout(function () {
          el.contentWindow.document.write(result);
        }, 0);
        this.openInvoice = true;
        this.currentInvoice = this.invoices[id].invoice.invoice_number;
        this.invoices[id].loading = false;
      });
    },
    expand(id, e) {
      // TODO: Make this height dynamic by detecting child
      // element heights
      this.$nextTick(function () {
        // let el = document.getElementById('invoice-extra-' + id);
        this.invoices[id].show = !this.invoices[id].show;
      });
    },
    createInvoice() {
      this.$router.push({name: 'Create Invoice'});
    },
    expandInvoice(id) {
      return this.invoices[id].show;
    },
    fetchInvoices() {
      let client = this.$store.getters.coreapiClient;
      let action = ['crm', 'invoice', 'list'];
      let schema = this.$store.getters.coreapiSchema;
      client.action(schema, action).then((result) => {
        for (var i = 0; i < result.length; i++) {
          let data = {
            show: false,
            invoice: result[i],
            statusValue: result[i].status,
            statusChanged: false,
            loading: false,
            options: [{
              text: 'Pending',
              value: 'pending',
            }, {
              text: 'Paid',
              value: 'paid',
            }, {
              text: 'Cancelled',
              value: 'cancelled',
            }]
          };
          this.$set(this.invoices, result[i].id, data);
        }
      });
    }
  }
};
</script>

<style scoped>
.ui.labeled.button {
  width: 100%;
  font-size: 13px !important;
}
.ui.grid > .row.invoice-header {
  color: #242e59;
  font-weight: bold;
}
.ui.grid > .row.invoice-row {
  padding: 0;
  font-size: 13px;
}
.ui.grid > .row.invoice-row.expanded {
  margin-bottom: 15px;
  border: 1px solid #aaa;
}
.ui.grid > .row.invoice-row .invoice-row-main {
  padding-top: 7px;
  padding-bottom: 7px;
}
.ui.grid > .row.invoice-row:nth-child(even) .invoice-row-main {
  background-color: #eaeaea;
}
.ui.grid > .row.invoice-row:nth-child(odd) .invoice-row-main {
  background-color: #f9f9f9;
}
.ui.grid > .row.invoice-row.expanded .invoice-row-main {
  border-bottom: 1px solid #aaa;
  background-color: #40a3d6;
  color: #fff;
}

.ui.grid > .row.invoice-row .invoice-row-main.saved {
  -webkit-animation-name: flashBg;
  -webkit-animation-duration: 1500ms;
  -webkit-animation-iteration-count: 1;
  -webkit-animation-timing-function: linear;
  -moz-animation-name: flashBg;
  -moz-animation-duration: 1500ms;
  -moz-animation-iteration-count: 1;
  -moz-animation-timing-function: linear;
}

@-webkit-keyframes flashBg {
  0% {
    background-color: #40a3d6;
  }
  15% {
    background-color: #242e59;
  }
  100% {
    background-color: #40a3d6;
  }
}

.ui.grid.invoice-extra {
  opacity: 0;
  padding: 0;
  height: 0;
  visibility: hidden;
  overflow: hidden;
  transition: height 300ms, visibility 300ms, padding 300ms, opacity 300ms;
}
.ui.grid.invoice-extra.stackable {
  margin: 0 !important;
}
.ui.grid > .row.invoice-row.expanded .ui.grid.invoice-extra {
  height: 200px;
  opacity: 1;
  visibility: visible;
}
.valign-child-center > * {
  align-self: center;
}
.expand-invoice-row {
  cursor: pointer;
}
.invoice-row-extra .selection {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}
.invoice-date-field {
  margin-bottom: 15px;
}
.invoice-date-field span {
  align-self: center;
  display: inline-block;
}
.invoice-date-field span.invoice-date-field--date {
  border-radius: 0 4px 4px 0;
  padding: 4px 10px;
  position: relative;
  margin-left: 10px;
  border-left: 1px solid #aaa;
}
.invoice-date-field span.ui {
  min-width: 100px;
  border-radius: 4px 0 0 4px;
  padding-top: 8px;
}
@media only screen and (min-width: 1368px) {
  .invoice-row > .ui.grid {
    width: 100%;
  }
}
@media only screen and (max-width: 767px) {
  .ui.grid > .row.invoice-row.expanded .ui.grid.invoice-extra {
    height: auto;
  }
}
</style>
