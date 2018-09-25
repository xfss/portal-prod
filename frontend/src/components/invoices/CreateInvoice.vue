<template>
  <div id="lp-create-invoice">
    <div class="ui large header">{{ $t('Create Invoice') }}</div>
    <div class="row">
      <div class="column">
        <sui-breadcrumb>
          <sui-breadcrumb-section>
            <router-link :to="{ name: 'Invoices' }">{{ $t('Invoices') }}</router-link>
          </sui-breadcrumb-section>
          <sui-breadcrumb-divider icon="right chevron" />
          <sui-breadcrumb-section active>{{ this.$route.name }}</sui-breadcrumb-section>
        </sui-breadcrumb>
      </div>
    </div>
    <div class="row">
      <div class="column">
        <form v-on:submit.prevent="create" class="ui equal width form" v-bind:class="[success ? 'success' : 'error']">
          <div class="basic vertical ui segment">
            <div class="two fields">
              <div class="required field" v-bind:class="[formErrors.product ? 'error' : '']">
                <label>{{ $t('Product') }}</label>
                <sui-dropdown selection :placeholder="$t('Select a Product')" :options="product_options" v-model="product" />
              </div>
              <div class="required field" v-bind:class="[formErrors.contract ? 'error' : '']">
                <label>{{ $t('Contract') }}</label>
                <sui-dropdown selection :placeholder="$t('Select a Publisher')" :options="contract_options" v-model="contract" v-bind:class="{disabled: contract_options.length < 1}" />
              </div>
            </div>
            <div class="two fields">
              <div class="required field" v-bind:class="[formErrors.date_range ? 'error' : '']">
                <label>{{ $t('Invoice for') }}</label>
                <date-picker v-model="invoice_date_range" range :shortcuts="shortcuts" input-class='date-input' :lang="lang" range-separator='-'></date-picker>
              </div>
              <div class="required field" v-bind:class="[formErrors.invoice_date ? 'error' : '']">
                <label>{{ $t('Invoice date') }}</label>
                <date-picker v-model="invoice_date" :shortcuts="shortcuts" input-class='date-input' :lang="lang" ></date-picker>
                <!-- <sui-input placeholder="Due by..." icon="calendar" /> -->
              </div>
            </div>
            <div class="field" v-if="messages.length > 0">
              <div class="ui message" v-bind:class="[success ? 'success' : 'error']">
                <ul class="list">
                  <li v-for="message in messages" :key="message.id">{{ message }}</li>
                </ul>
              </div>
            </div>
          </div>
          <sui-button type="submit" v-bind:class="[loading ? 'loading' : '']">{{ $t('Create') }}</sui-button>
          <span v-if="loading">{{ $t('Creating invoice...') }}</span>
        </form>
      </div>
    </div>
  </div>
</template>

<script>

import DatePicker from 'vue2-datepicker';
import moment from 'moment';

export default {
  components: { DatePicker },
  data() {
    return {
      loading: false,
      success: false,
      formErrors: {
        'contract': false,
        'product': false,
        'date_range': false,
        'invoice_date': false
      },
      messages: [],
      contract: null,
      contract_options: [],
      product: null,
      product_options: [
        {text: 'Adfusion', value: 'adfusion'},
        {text: 'Newsfusion', value: 'newsfusion'},
      ],
      invoice_date_range: [],
      invoice_date: new Date(),
      lang: 'en',
      shortcuts: [
        {
          text: 'Today',
          start: new Date(),
          end: new Date()
        },
        {
          text: 'Last month',
          start: moment().subtract(1, 'months').startOf('month').toDate(),
          end: moment().subtract(1, 'months').endOf('month').toDate()
        }
      ]
    };
  },
  watch: {
    product: function (contractType) {
      let client = this.$store.getters.coreapiClient;
      let action = ['crm', 'contract', contractType, 'list'];
      let schema = this.$store.getters.coreapiSchema;

      if (contractType) {
        client.action(schema, action).then((result) => {
          if (result) {
            this.contract_options = result.map(contract => {
              return {'text': `${contract.publications.map(p => p.code).sort().join(', ')} | ${contract.publisher.name}`, 'value': contract.id};
            }).sort((a, b) => { return a.text > b.text; });

            // ESLint complains about this, but we should not fall through here if our request was a success, so add null to the return value
            return null;
          }
        });
      }
      this.contract = null;
    },
  },
  methods: {
    validateForm() {
      this.success = false;
      this.messages = [];
      for (const k in this.formErrors) {
        if (this.formErrors.hasOwnProperty(k)) {
          this.formErrors[k] = false;
        }
      }
      console.log(this.formErrors);
      if (this.contract && this.product && this.invoice_date_range.length === 2 && this.invoice_date) {
        this.success = true;
        return true;
      }
      if (!this.contract) {
        // this.message = this.$t('"Contract" is a required field.');
        this.formErrors.contract = true;
      }
      if (!this.product) {
        // this.message = this.$t('"Product" is a required field.');
        this.formErrors.product = true;
      }
      if (this.invoice_date_range.length < 2) {
        // this.message = this.$t('"Invoice for" is a required field.');
        this.formErrors.date_range = true;
      }
      if (!this.invoice_date) {
        // this.message = this.$t('"Invoice date" is a required field.');
        this.formErrors.invoice_date = true;
      }
      if (!this.contract_options.length > 0) {
        if (!this.product) {
          this.messages.push(this.$t('Please select a product before selecting a contract.'));
        } else {
          this.messages.push(this.$t('The currently selected product has no contracts available, please select another one.'));
        }
      }
      this.messages.push(this.$t('Please enter a value for the highlighted fields.'));
      this.success = false;
      return false;
    },
    create() {
      if (!this.validateForm()) {
        return false;
      }
      this.loading = true;

      // To get the right date here we are intentionally converting to a iso string with a timezone offset instead of utc and cutting off the end
      let startDate = moment(this.invoice_date_range[0]).toISOString(true).split('T')[0];
      let endDate = moment(this.invoice_date_range[1]).toISOString(true).split('T')[0];
      let invoiceDate = moment(this.invoice_date).toISOString(true).split('T')[0];
      let data = new FormData();

      data.set('start_date', startDate);
      data.set('end_date', endDate);
      data.set('invoice_date', invoiceDate);
      data.set('product', this.product);

      let axiosClient = this.$store.getters.axiosClient;

      axiosClient.post(`crm/contract/${this.contract}/invoice/`, data).then((response) => {
        this.$router.push({name: 'Invoices'});
      }).catch((error) => {
        this.success = false;
        if (error.response || error.request) {
          this.messages.push(error.message);
        } else {
          console.log('Error', error.message);
        }
      });
    }
  }
};
</script>

<style scoped>
.mx-datepicker,
.date-input {
  width: 100% !important;
}
</style>
