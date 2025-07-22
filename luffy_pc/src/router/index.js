import Vue from 'vue'
import Router from 'vue-router'
import Home from "../components/Home.vue"
import Login from "../components/Login.vue"
import Register from "../components/Register.vue"
import Course from "../components/Course.vue";
import Detail from "../components/Detail.vue";
import Cart from "../components/Cart.vue"
import Order from "../components/Order.vue"
import Success from "../components/Success.vue"
import UserOrder from "@/components/UserOrder"
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
    {
      path: '/courses',
      name: "Course",
      component: Course
    },
    {
      path: '/course/detail/:courses_id',
      name: "Detail",
      component: Detail
    },
    {
      path: '/cart',
      name: "Cart",
      component: Cart
    },
    {
      path: '/order',
      name: "Order",
      component: Order
    },
    {
      path: '/payments/result',
      name: "Success",
      component: Success,
    },
    {
      path: "/user/order",
      name: "UserOrder",
      component: UserOrder
    }
  ]
})
