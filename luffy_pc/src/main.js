// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import settings from "./settings"

Vue.config.productionTip = false;
Vue.prototype.$settings = settings; // 在Vue中全局挂载settings

import axios from "axios";

axios.defaults.withCredentials = false // 是否让ajax携带cookie，默认是false不允许
Vue.prototype.$axios = axios;  // 把对象挂载到Vue上

// element ui配置
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
// 调用插件
Vue.use(ElementUI);

// 导入css初始化文件
import "../static/css/reset.css";

// 导入极验的sdk
import "../static/js/gt.js"

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {App},
  template: '<App/>'
})
