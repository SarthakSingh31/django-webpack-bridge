import Vue from 'vue';

import Index from './components/index.vue';

Vue.component('index-comp', Index);

new Vue({
  el: '#vue_root',
});