<template>
  <div id="lp-app" class="pusher" v-if="currentUser.token">
    <div id="header">
      <div class="row">
        <div class="header-left">
          <div class="brand"></div>
        </div>
        <div class="header-right">
          <div class="menu-toggle" v-on:click="menuToggle" >
            <a href="javascript:void(0);" class="item"><i class="sidebar icon"></i><span>{{ $t('Menu') }}</span></a>
          </div>
        </div>
      </div>
      <div id="menu" class="ui inverted left vertical menu" v-on:click="menuToggle" v-bind:class="{ visible: menuActive }">
        <div class="header item">
          <div class="brand inverted"></div>
        </div>
        <!-- <router-link class="item" exact-active-class="active" :to="{ name: 'Main' }"><i class="home icon"></i>Home</router-link> -->
        <router-link v-if="currentUser.token === ''" class="item" exact-active-class="active" :to="{ name: 'Login' }"><i class="user icon"></i>{{ $t('Sign in') }}</router-link>
        <div v-else>
          <router-link class="item" exact-active-class="active" :to="{ name: 'File Upload' }"><i class="file icon"></i>{{ $t('File Upload') }}</router-link>
          <router-link class="item" exact-active-class="active" :to="{ name: 'Files' }"><i class="file icon"></i>{{ $t('Files') }}</router-link>
          <router-link v-if="currentUser.data.is_staff" class="item" exact-active-class="active" :to="{ name: 'Files Admin' }"><i class="file icon"></i>{{ $t('Files - Admin') }}</router-link>
          <router-link class="item" exact-active-class="active" :to="{ name: 'Publications' }"><i class="file icon"></i>{{ $t('Publications') }}</router-link>
          <div v-if="currentUser.data.is_staff">
            <router-link class="item" exact-active-class="active" :to="{ name: 'New Service' }" v-if="currentUser.data.is_staff"><i class="server icon"></i>{{ $t('New Service') }}</router-link>
            <router-link class="item" exact-active-class="active" :to="{ name: 'Services' }"><i class="server icon"></i>{{ $t('Services') }}</router-link>
            <router-link class="item" exact-active-class="active" :to="{ name: 'Service Events' }"><i class="server icon"></i>{{ $t('All Service Events') }}</router-link>
            <router-link class="item" exact-active-class="active" :to="{ name: 'All File Events' }"><i class="file icon"></i>{{ $t('All File Events') }}</router-link>
            <router-link class="item" exact-active-class="active" :to="{ name: 'Invoices' }"><i class="file pdf icon"></i>Invoices</router-link>
          </div>
        </div>
        <div class="fixed bottom">
          <div class="item" v-if="currentUser.token && !isMobile">
            <span>{{ $t('Logged in as:') }}</span>
            <span>{{ this.currentUser.data.username }}</span>
          </div >
          <router-link class="item logout" v-if="currentUser.token" exact-active-class="active" :to="{ name: 'Logout' }"><i class="sign out alternate icon"></i>{{ $t('Sign out') }}</router-link>
        </div>
      </div>
    </div>
    <div id="content" class="pushable">
      <div class="basic segment ui">
        <div class="container fluid ui">
          <div class="row">
            <div class="column">
              <router-view></router-view>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else id="login-view">
    <router-view></router-view>
  </div>
</template>

<script>
import {mapGetters} from 'vuex';

export default {
  name: 'App',
  created() {
    let loader = document.getElementById('preload-overlay');
    loader.classList.add('loading-fade-out');
  },
  computed: {
    ...mapGetters([
      'currentUser',
    ])
  },
  data: function () {
    return {
      menuActive: false,
      isMobile: false
    };
  },
  methods: {
    menuToggle: function (event) {
      if (!this.isMobile && !this.menuActive) {
        return;
      }
      this.menuActive = !this.menuActive;
    },
    handleResize: function (event) {
      if (window.innerWidth < 992) {
        this.isMobile = true;
        return;
      }
      this.isMobile = false;
    }
  },
  mounted: function () {
    let loader = document.getElementById('preload-overlay');
    setTimeout(function () {
      loader.parentNode.removeChild(loader);
    }, 2000);
    this.handleResize();
    window.addEventListener('resize', this.handleResize);
  },
  beforeDestroy: function () {
    window.removeEventListener('resize', this.handleResize);
  }
};
</script>

<style lang="less">
  @import "vendors/semantic/dist/semantic.min.css";
  #login-view {
    height: 100%;
  }
</style>
