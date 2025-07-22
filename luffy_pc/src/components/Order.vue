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

      <div class="discount">
        <div id="accordion">
          <div class="coupon-box">
            <div class="icon-box">
              <span class="select-coupon">使用优惠劵：</span>
              <a class="select-icon unselect" :class="use_coupon?'is_selected':''" @click="use_coupon=!use_coupon"><img
                class="sign is_show_select" src="../../static/image/12.png" alt=""></a>
              <span class="coupon-num">有{{ coupon_list.length }}张可用</span>
            </div>
            <p class="sum-price-wrap">商品总金额：<span class="sum-price">¥{{ total_price.toFixed(2) }}元</span></p>
          </div>
          <div id="collapseOne" v-if="use_coupon">
            <ul class="coupon-list" v-if="coupon_list.length>0">

              <li class="coupon-item" :class="selected_coupon(index,item.id)" v-for="(item,index) in coupon_list"
                  :key="item.id" @click="click_select_coupon(index,item.id)">
                <p class="coupon-name">{{ item.coupon.name }}</p>
                <p class="coupon-condition" v-if="item.coupon.condition>0"> 满{{ item.coupon.condition }}元可以使用</p>
                <p class="coupon-condition" v-else> 优惠券无门槛使用 </p>
                <p class="coupon-time start_time">开始时间：{{ item.start_time.replace('T', ' ') }}</p>
                <p class="coupon-time end_time">过期时间：{{ item.end_time }}</p>
              </li>
            </ul>
            <div class="no-coupon" v-if="coupon_list.length<1">
              <span class="no-coupon-tips">暂无可用优惠券</span>
            </div>
          </div>
        </div>
        <div class="credit-box">
          <label class="my_el_check_box">
            <el-checkbox class="my_el_checkbox" v-model="use_credit"></el-checkbox>
          </label>
          <p class="discount-num1" v-if="!use_credit">使用我的贝里</p>
          <p class="discount-num2" v-else>
            <span>
              总积分：{{ user_credit }}，抵扣
            <el-input-number @change="handleChange"
                             v-model="credit" :min="0"
                             :max="max_credit()"
                             label="请填写积分">
            </el-input-number>，
              本次花费以后，剩余{{ parseInt(user_credit - credit) }}积分
          </span>
          </p>
        </div>
        <p class="sun-coupon-num">优惠券抵扣：<span>0.00元</span></p>
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
          <el-col :span="8" class="count">实付款： <span>¥{{ (real_total - credit / credit_to_money).toFixed(2) }}</span>
          </el-col>
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
      use_credit: false,  // 是否使用了优惠券
      use_coupon: false,  // 优惠券ID，0表示没有使用优惠券
      credit: 0,          // 积分
      coupon: 0,          // 优惠券ID，0表示没有使用优惠券
      pay_type: 0,        // 支付方式
      total_price: 0,     // 订单总金额
      real_total: 0,      // 优惠劵和积分折算的价格
      course_list: [],     // 勾选商品
      coupon_list: [],      // 优惠券列表
      user_credit: localStorage.user_credit || sessionStorage.user_credit,  // 积分
      credit_to_money: localStorage.credit_to_money || sessionStorage.credit_to_money, // 积分兑换金额
    }
  },
  components: {
    Header,
    Footer,
  },
  watch: {
    coupon: {
      handler(newVal, oldVal) {
        this.calc_real_total(oldVal)
        if (this.real_total - this.credit / this.credit_to_money < 0) {
          this.credit = parseInt(this.real_total * this.credit_to_money)
        }
      }
    },
    use_coupon() {
      if (this.use_coupon === false) {
        this.coupon = 0
      }
    }
  },
  created() {
    this.token = this.check_user_login();
    this.get_cart();
    this.get_coupon()
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
        this.real_total = response.data.total_price;
        console.log(this.course_list)
      }).catch(error => {
        this.$message.error(error.response.data.message + "有问题，请重新登录");
      })
    },
    get_coupon() {
      // 获取当前用户拥有的优惠卷
      this.$axios.get(`${this.$settings.HOST}/coupon/`, {
        headers: {
          "Authorization": `Bearer ${this.token}`
        },
      }).then(response => {
        this.coupon_list = response.data;

      }).catch(error => {
        this.$message.error(error.response.data.message + "有问题，请重新登录");
      })
    },
    click_select_coupon(index, uer_coupon_id) {  // 点击切换优惠券时记录本次点击的优惠券
      let user_coupon = this.coupon_list[index]
      // 判断总价格是否满足优惠券条件
      if (this.total_price < user_coupon.coupon.condition) {
        return
      }
      // 判断优惠券是否处于使用时间范围内
      let start_time = parseInt(new Date(user_coupon.start_time) / 1000)
      let end_time = parseInt(new Date(user_coupon.end_time) / 1000)
      let now_time = parseInt(new Date() / 1000)
      if (now_time < start_time || now_time > end_time) {
        return
      }
      if (this.coupon === uer_coupon_id) {
        this.coupon = 0;
      } else {
        this.coupon = uer_coupon_id;
      }
    },
    selected_coupon(index, uer_coupon_id) {
      // 当选中优惠券时，切换高亮效果
      let user_coupon = this.coupon_list[index]

      // 判断总价格是否满足优惠券条件
      if (this.total_price < user_coupon.coupon.condition) {
        return "disable"
      }

      // 判断优惠券是否处于使用时间范围内
      let start_time = parseInt(new Date(user_coupon.start_time) / 1000)
      let end_time = parseInt(new Date(user_coupon.end_time) / 1000)
      let now_time = parseInt(new Date() / 1000)
      if (now_time < start_time || now_time > end_time) {
        return "disable"
      }

      if (this.coupon === uer_coupon_id) {
        return "active"
      }
      return ""
    },
    PayHander() {
      if (this.real_total===0){
        this.$message.error("请选择课程")
        return
      }
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
        // 发起支付[页面跳转,后端需要提供跳转地址]
        this.$axios.get(`${this.$settings.HOST}/payments/alipay/`,{
          params: {
            order_number: response.data.order_number
          }
        }).then(response => {
          // 跳转至支付页面
          location.href = response.data.url;
        }).catch(error => {
          this.$message.error(error.response.data.message + "订单生成失败");
        })
      }).catch(error => {
        this.$message.error(error.response.data.message + "订单生成失败");
      })
    },
    calc_real_total(oldVal) {
      if (this.coupon === 0) {
        this.coupon_list.forEach(item => {
          // 判断当前优惠劵是否被选中
          if (item.id === oldVal) {
            let f = parseFloat(item.coupon.sale.substr(1));
            if (item.coupon.sale[0] === "*") {
              this.real_total /= f;
            } else {
              this.real_total += f;
            }
          }
        })
      }
      this.coupon_list.forEach(item => {
        // 判断当前优惠劵是否被选中
        if (item.id === this.coupon) {
          let start_timestamp = parseInt(new Date(item.start_time) / 1000);
          let end_timestamp = parseInt(new Date(item.end_time) / 1000);
          let now_timestamp = parseInt(new Date() / 1000);
          // 选出当前可以使用的优惠券
          if ((this.total_price > item.coupon.condition) && (now_timestamp > start_timestamp) && (now_timestamp < end_timestamp)) {
            // 获取优惠公式
            let f = parseFloat(item.coupon.sale.substr(1));
            // 根据优惠公式计算最终折算后的总价格
            if (item.coupon.sale[0] === "*") {
              // 折扣优惠
              this.real_total = this.total_price * f;
            } else {
              // 减免优惠
              this.real_total = this.total_price - f;
            }
          }
        }
      })
    },
    max_credit() {
      // 计算本次订单中，用户可以设置的最大积分

      // 用户拥有的积分允许抵扣的最大金额
      let max_credit_to_money = this.user_credit / this.credit_to_money;
      console.log("用户积分抵扣", max_credit_to_money);
      // 计算当前真实的订单实付金额
      let ret = 0;
      if (max_credit_to_money > this.real_total) {
        ret = parseInt(this.real_total * this.credit_to_money);
      } else {
        ret = parseInt(this.user_credit);
      }
      console.log(ret);
      return ret;
    },
    handleChange(value) {
      if (typeof value !== "number" || !isFinite(value) || value < 0) {
        this.credit = 0;
      }
    }
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

/** 优惠劵 **/
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


.coupon-box {
  text-align: left;
  padding-bottom: 22px;
  padding-left: 30px;
  border-bottom: 1px solid #e8e8e8;
}

.coupon-box::after {
  content: "";
  display: block;
  clear: both;
}

.icon-box {
  float: left;
}

.icon-box .select-coupon {
  float: left;
  color: #666;
  font-size: 16px;
}

.icon-box::after {
  content: "";
  clear: both;
  display: block;
}

.select-icon {
  width: 20px;
  height: 20px;
  float: left;
}

.select-icon img {
  max-height: 100%;
  max-width: 100%;
  margin-top: 2px;
  transform: rotate(-90deg);
  transition: transform .5s;
}

.is_show_select {
  transform: rotate(0deg) !important;
}

.coupon-num {
  height: 22px;
  line-height: 22px;
  padding: 0 5px;
  text-align: center;
  font-size: 12px;
  float: left;
  color: #fff;
  letter-spacing: .27px;
  background: #fa6240;
  border-radius: 2px;
  margin-left: 20px;
}

.sum-price-wrap {
  float: right;
  font-size: 16px;
  color: #4a4a4a;
  margin-right: 45px;
}

.sum-price-wrap .sum-price {
  font-size: 18px;
  color: #fa6240;
}

.no-coupon {
  text-align: center;
  width: 100%;
  padding: 50px 0px;
  align-items: center;
  justify-content: center; /* 文本两端对其 */
  border-bottom: 1px solid rgb(232, 232, 232);
}

.no-coupon-tips {
  font-size: 16px;
  color: #9b9b9b;
}

.credit-box {
  height: 30px;
  margin-top: 40px;
  display: flex;
  align-items: center;
  justify-content: flex-end
}

.my_el_check_box {
  position: relative;
}

.my_el_checkbox {
  margin-right: 10px;
  width: 16px;
  height: 16px;
}

.discount {
  overflow: hidden;
}

.discount-num1 {
  color: #9b9b9b;
  font-size: 16px;
  margin-right: 45px;
}

.discount-num2 {
  margin-right: 45px;
  font-size: 16px;
  color: #4a4a4a;
}

.sun-coupon-num {
  margin-right: 45px;
  margin-bottom: 43px;
  margin-top: 40px;
  font-size: 16px;
  color: #4a4a4a;
  display: inline-block;
  float: right;
}

.sun-coupon-num span {
  font-size: 18px;
  color: #fa6240;
}

.coupon-list {
  margin: 20px 0;
}

.coupon-list::after {
  display: block;
  content: "";
  clear: both;
}

.coupon-item {
  float: left;
  margin: 15px 8px;
  width: 180px;
  height: 100px;
  padding: 5px;
  background-color: #fa3030;
  cursor: pointer;
}

.coupon-list .active {
  background-color: #fa9000;
}

.coupon-list .disable {
  cursor: not-allowed;
  background-color: #fa6060;
}

.coupon-condition {
  font-size: 12px;
  text-align: center;
  color: #fff;
}

.coupon-name {
  color: #fff;
  font-size: 24px;
  text-align: center;
}

.coupon-time {
  text-align: left;
  color: #fff;
  font-size: 12px;
}

.unselect {
  margin-left: 0px;
  transform: rotate(-90deg);
}

.is_selected {
  transform: rotate(-1turn) !important;
}
</style>
