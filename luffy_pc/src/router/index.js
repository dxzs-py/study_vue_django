import Vue from 'vue'
import Router from 'vue-router'
import Home from "../components/Home.vue"
import Login from "../components/Login.vue"
import Register from "../components/Register.vue"
// 这里是路由的配置

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: "Home",
      component: Home,
    },
    {
      path: '/user/login',
      name: "Login",
      component: Login
    },
    {
      path: '/user/reg',
      name: "Register",
      component: Register
    },

  ]
})
