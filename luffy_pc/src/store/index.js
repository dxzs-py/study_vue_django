import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // 数据仓库,类似vue组件里面的data
    cart_length: 0
  },
  // 数据操作方法,类似vue里面的methods
  mutations: {
      add_cart(state, data) {
          state.cart_length = data
      }
  }
})
