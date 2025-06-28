<template>
  <div class="cart">
    <Header></Header>
    <div class="cart_info">
      <div class="cart_title">
        <span class="text">我的购物车</span>
        <span class="total">共{{ $store.state.cart_length }}门课程</span>
      </div>
      <div class="cart_table">
        <div class="cart_head_row">
          <span class="doing_row"></span>
          <span class="course_row">课程</span>
          <span class="expire_row">有效期</span>
          <span class="price_row">单价</span>
          <span class="do_more">操作</span>
        </div>
        <!-- 购物车中商品列表 -->
        <div class="cart_course_list">
          <CartItem v-for="(course,index) in course_list" :key="index" :course="course" @change_select="calc_total"
                    @delete_course="del_cart(index)"></CartItem>
        </div>
        <div class="cart_footer_row">
          <span class="cart_select"><label> <el-checkbox
            @click="change_checked"
            v-model="checked"> <span>全选</span> </el-checkbox></label></span>
          <span class="cart_delete"><i class="el-icon-delete"></i> <span>删除</span></span>
          <router-link to="/order">
          <span class="goto_pay">
            去结算
          </span>
          </router-link>
          <span class="cart_total">总计：¥{{ total_price.toFixed(2) }}</span>
        </div>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from "./common/Header"
import Footer from "./common/Footer"
import CartItem from "./common/CartItem"

export default {
  name: "Cart",
  computed: {
    checked: {
      // 必须所以的都选择，才返回true
      get() {
        for (let i = 0; i < this.course_list.length; i++) {
          if (!this.course_list[i].selected) {
            return false
          }
        }
        return true
      },
      set(value) {
        //   let self = this;
        //   const request = this.course_list.map(function (item, key) {
        //     return self.$axios.patch(`${self.$settings.HOST}/cart/`, {
        //       course_id: item.id,
        //       selected: value,
        //     }, {
        //       headers: {
        //         Authorization: `Bearer ${self.token}`,
        //       }
        //     }).catch(error => {
        //       // 收集错误但不在此处提示
        //         console.error(error);
        //         return Promise.reject(error);
        //     })
        //   });
        //   Promise.all(request).then(function () {
        //     // 更新选中状态
        //     self.$message.success("批量更新成功")
        //     self.get_cart()
        //   }).catch(function (error) {
        //     self.$message.error(error.response.data.message + "部分或全部更新失败，请重试");
        //   })
        // }// 这个是一种思路，但是Cartltem,会监听selected的改变，并发信息到后端，所以这样写会浪费资源。
        for (let i = 0; i < this.course_list.length; i++) {
          this.course_list[i].selected = value
        }
      }


    },
  },
  data() {
    return {
      token: "",
      is_all_selected: false,
      total_price: 0.00,
      course_list: [],
    }
  },
  created() {
    this.token = this.check_user_login();
    this.get_cart()
  },
  methods: {
    calc_total() {
      // 勾选商品的总价格
      // 计算购物车勾选商品的总价格
      /**
       // 在javascript中，数组有一个默认的方法，forEach可以用于对数组进行遍历
       arr1 = ["a","b","c","d"]
       arr1.forEach(function(value,key){
       console.log(`下标：${key}，值=${value}`);
       });
       **/
      let total = 0
      this.course_list.forEach((item, key) => {
        if (item.selected) {
          total += parseFloat(item.price)
        }
      })
      this.total_price = total
    },
    get_cart() {
      // 获取购物车中商品信息
      this.$axios.get(`${this.$settings.HOST}/cart/`, {
        headers: {
          "Authorization": `Bearer ${this.token}`
        },
      }).then(response => {
        this.course_list = response.data;
        this.$store.commit('add_cart', this.course_list.length)
        // 统计勾选商品课程的具体价格
        this.calc_total()
      }).catch(error => {
        this.$message.error(error.response.data.message + "有问题，请重新登录");
      })
    },
    check_user_login() {
      let token = localStorage.user_token || sessionStorage.user_token;
      if (!token) {
        let self = this;
        this.$confirm("对不起，请先登录", "戴兴志", {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          self.$router.push("/user/login");
        });
        return false; // 阻止js继续往下执行
      }
      return token;
    },
    del_cart(key) {
      // 从购物车中删除指定商品
      this.course_list.splice(key, 1)
      // 删除商品之后，重新计算商品总价格
      this.calc_total()
    },
    change_checked() {
      this.checked = !this.checked
    }
  },
  components: {
    Header,
    Footer,
    CartItem,
  }
}
</script>

<style scoped>
.cart_info {
  width: 1200px;
  margin: 0 auto 200px;
}

.cart_title {
  margin: 25px 0;
}

.cart_title .text {
  font-size: 18px;
  color: #666;
}

.cart_title .total {
  font-size: 12px;
  color: #d0d0d0;
}

.cart_table {
  width: 1170px;
}

.cart_table .cart_head_row {
  background: #F7F7F7;
  width: 100%;
  height: 80px;
  line-height: 80px;
  padding-right: 30px;
}

.cart_table .cart_head_row::after {
  content: "";
  display: block;
  clear: both;
}

.cart_table .cart_head_row .doing_row,
.cart_table .cart_head_row .course_row,
.cart_table .cart_head_row .expire_row,
.cart_table .cart_head_row .price_row,
.cart_table .cart_head_row .do_more {
  padding-left: 10px;
  height: 80px;
  float: left;
}

.cart_table .cart_head_row .doing_row {
  width: 78px;
}

.cart_table .cart_head_row .course_row {
  width: 530px;
}

.cart_table .cart_head_row .expire_row {
  width: 188px;
}

.cart_table .cart_head_row .price_row {
  width: 162px;
}

.cart_table .cart_head_row .do_more {
  width: 162px;
}

.cart_footer_row {
  padding-left: 30px;
  background: #F7F7F7;
  width: 100%;
  height: 80px;
  line-height: 80px;
}

.cart_footer_row .cart_select span {
  margin-left: 7px;
  font-size: 18px;
  color: #666;
}

.cart_footer_row .cart_delete {
  margin-left: 58px;
}

.cart_delete .el-icon-delete {
  font-size: 18px;
}

.cart_delete span {
  margin-left: 15px;
  cursor: pointer;
  font-size: 18px;
  color: #666;
}

.cart_total {
  float: right;
  margin-right: 62px;
  font-size: 18px;
  color: #666;
}

.goto_pay {
  float: right;
  width: 159px;
  height: 80px;
  outline: none;
  border: none;
  background: #ffc210;
  font-size: 18px;
  color: #fff;
  text-align: center;
  cursor: pointer;
}
</style>
