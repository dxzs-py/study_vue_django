// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import settings from "./settings"

Vue.config.productionTip = false;
Vue.prototype.$settings = settings; // 在Vue中全局挂载settings

import axios, {request} from "axios";

axios.defaults.withCredentials = false // 是否让ajax携带cookie，默认是false不允许
Vue.prototype.$axios = axios;  // 把对象挂载到Vue上

// element ui配置
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
// 调用插件
Vue.use(ElementUI);


// vue-video-player 视频播放器导入video.js
require('video.js/dist/video-js.css'); // video-js.css 是底层视频播放库 video.js 的核心样式
require('vue-video-player/src/custom-theme.css'); // custom-theme.css 是 vue-video-player 的默认主题样式
import VideoPlayer from 'vue-video-player'
Vue.use(VideoPlayer);

// 导入css初始化文件
import "../static/css/reset.css";

// 导入极验的sdk
import "../static/js/gt.js"

// 导入vuex
import store from "./store/index"



/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: {App},
  template: '<App/>'
});
