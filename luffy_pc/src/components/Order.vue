<template>
  <div class="cart">
    <Header/>
    <div class="cart-info">
      <h3 class="cart-top">购物车结算 <span>共{{ course_list.length }}门课程</span></h3>
      <div class="cart-title">
        <el-row>
          <el-col :span="2">&nbsp;</el-col>
          <el-col :span="10">课程</el-col>
          <el-col :span="8">有效期</el-col>
          <el-col :span="4">价格</el-col>
        </el-row>
      </div>
      <div class="cart-item" v-for="(course,index) in course_list" :key="course.id">
        <el-row>
          <el-col :span="2" class="checkbox">&nbsp;&nbsp;</el-col>
          <el-col :span="10" class="course-info">
            <img :src="course.course_img" alt="">
            <span class="course-name">
              {{ course.name }}
              <br>
              <span class="discount">
              {{ course.discount_name }}
              </span>
            </span>
          </el-col>
          <el-col :span="8"><span>{{ course.expired_text }}</span></el-col>
          <el-col :span="4" class="course-price">
            <span class="real_price">¥{{ course.real_price.toFixed(2) }}</span><br>
            <span class="original_price">原价￥{{ course.original_price.toFixed(2) }}</span>
          </el-col>
        </el-row>
      </div>

      <div class="calc">
        <el-row class="pay-row">
          <el-col :span="4" class="pay-col"><span class="pay-text">支付方式：</span></el-col>
          <el-col :span="8">
            <span class="alipay" v-if="pay_type==0"><img src="../../static/image/alipay2.png" alt=""></span>
            <span class="alipay" v-else @click="pay_type=0"><img src="../../static/image/alipay.png" alt=""></span>
            <span class="alipay wechat" v-if="pay_type==1"><img src="../../static/image/wechat2.png" alt=""></span>
            <span class="alipay wechat" v-else @click="pay_type=1"><img src="../../static/image/wechat.png"
                                                                        alt=""></span>
          </el-col>
          <el-col :span="8" class="count">实付款： <span>¥{{ total_price.toFixed(2) }}</span></el-col>
          <el-col :span="4" class="cart-pay"><span @click="PayHander">立即支付</span></el-col>
        </el-row>
      </div>
    </div>
    <Footer/>

  </div>
</template>

<script>
import Header from "./common/Header"
import Footer from "./common/Footer"

export default {
  name: "Order",
  data() {
    return {
      pay_type: 0,
      credit: 0,
      coupon: 0,
      course_list: [],
      total_price: 0,

    }
  },
  components: {
    Header,
    Footer,
  },
  created() {
    this.token = this.check_user_login();
    this.get_cart();
  },
  methods: {
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
    get_cart() {
      this.$axios.get(`${this.$settings.HOST}/cart/order/`, {
        headers: {
          "Authorization": `Bearer ${this.token}`
        },
      }).then(response => {
        this.course_list = response.data.course_list;
        this.total_price = response.data.total_price;
        console.log(this.course_list)
      }).catch(error => {
        this.$message.error(error.response.data.message + "有问题，请重新登录");
      })
    },
    PayHander() {
      // 生成订单
      this.$axios.post(`${this.$settings.HOST}/order/`, {
          pay_type: this.pay_type,  // 支付类型
          credit: this.credit,  // 积分
          coupon: this.coupon,  // 优惠劵
        }, {
          headers: {
            "Authorization": `Bearer ${this.token}`
          }
        }).then(response => {
          // 订单生成成功
          this.$message.success("订单生成成功！即将跳转至支付页面！请不要离开！")

      }).catch(error => {
        this.$message.error(error.response.data.message+"订单生成失败");
      })
    },
  }
}
</script>

<style scoped>
.cart {
  margin-top: 80px;
}

.cart-info {
  overflow: hidden;
  width: 1200px;
  margin: auto;
}

.cart-top {
  font-size: 18px;
  color: #666;
  margin: 25px 0;
  font-weight: normal;
}

.cart-top span {
  font-size: 12px;
  color: #d0d0d0;
  display: inline-block;
}

.cart-title {
  background: #F7F7F7;
  height: 70px;
}

.calc {
  margin-top: 25px;
  margin-bottom: 40px;
}

.calc .count {
  text-align: right;
  margin-right: 10px;
  vertical-align: middle;
}

.calc .count span {
  font-size: 36px;
  color: #333;
}

.calc .cart-pay {
  margin-top: 5px;
  width: 110px;
  height: 38px;
  outline: none;
  border: none;
  color: #fff;
  line-height: 38px;
  background: #ffc210;
  border-radius: 4px;
  font-size: 16px;
  text-align: center;
  cursor: pointer;
}

.cart-item {
  height: 120px;
  line-height: 120px;
  margin-bottom: 30px;
}

.course-info img {
  width: 175px;
  height: 115px;
  margin-right: 35px;
  vertical-align: middle;
}

.alipay {
  display: inline-block;
  height: 48px;
}

.alipay img {
  height: 100%;
  width: auto;
}

.pay-text {
  display: block;
  text-align: right;
  height: 100%;
  line-height: 100%;
  vertical-align: middle;
  margin-top: 20px;
}

.course-name {
  display: inline-block;
  line-height: 140%;
  font-size: 16px;
}

.course-name .discount {
  color: #ffc210;
  font-size: 13px;
}

.original_price {
  color: #999;
  font-size: 13px;
}

.course-price {
  line-height: 32px;
  padding-top: 18px;
}
</style>
