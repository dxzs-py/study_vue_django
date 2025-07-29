<template>
  <div class="user-order">
    <Header/>
    <div class="main">
      <div class="banner"></div>
      <div class="profile">
        <div class="profile-info">
          <div class="avatar"><img class="newImg" width="100%" alt="" src="../../static/image/logo@2x.png"></div>
          <span class="user-name">Mixtea</span>
          <span class="user-job">宁夏回族自治区银川市 | 学生</span>
        </div>
        <ul class="my-item">
          <li>我的账户</li>
          <li class="active">我的订单</li>
          <li>个人资料</li>
          <li>账号安全</li>
        </ul>
      </div>
      <div class="user-data">
        <ul class="nav">
          <li class="order-info">订单</li>
          <li class="course-expire">有效期</li>
          <li class="course-price">课程价格</li>
          <li class="real-price">实付金额</li>
          <li class="order-status">交易状态</li>
          <li class="order-do">交易操作</li>
        </ul>
        <div class="my-order-item" v-for="(order, index) in order_list">
          <div class="user-data-header">
            <span class="order-time">{{ order.create_time|timeformat }}</span>
            <span class="order-num">订单号：
                        <span class="my-older-number">{{ order.order_number }}</span>
                    </span>
          </div>

          <ul class="nav user-data-list" v-for="(course, index) in order.course_list">
            <li class="order-info">
              <img :src="course.course_img" alt="">
              <div class="order-info-title">
                <p class="course-title">{{ course.name }}</p>
                <p class="price-service" v-if="course.discount_name">{{ course.discount_name }}</p>
              </div>
            </li>
            <li class="course-expire">{{ course.expire_text }}</li>
            <li class="course-price">{{ course.price.toFixed(2) }}</li>
            <li class="real-price">{{ course.real_price.toFixed(2) }}</li>
            <li class="order-status" v-if="order.order_status===0">等待付款</li>
            <li class="order-status" v-else-if="order.order_status===1">交易成功</li>
            <li class="order-status" v-else-if="order.order_status===2">已取消</li>
            <li class="order-status" v-else-if="order.order_status===3">超时取消</li>
            <li class="order-do">
              <span class="btn btn2" v-if="order.order_status===0"><span
                @click="gotopay(order.order_number)">去付款</span></span>
              <span class="btn btn2" v-else-if="order.order_status===1">
                <router-link v-if="course.section_type===2"
                :to="{path: '/course/player',query:{'vid':course.section_link}}">去学习
                </router-link>
                <router-link v-else-if="course.section_type===1"
                :to="{path: '/course/exam',query:{'vid':course.section_link}}">去学习
                </router-link>
                <router-link v-else-if="course.section_type===0"
                :to="{path: '/course/document',query:{'vid':course.section_link}}">去学习
                </router-link>
                <span class="btn btn2" v-else>哎嘿，还没有做，哈哈哈</span>

              </span>
            </li>
          </ul>

        </div>
      </div>
    </div>
    <Footer/>
  </div>
</template>

<script>
import Header from "./common/Header"
import Footer from "./common/Footer"

export default {
  name: "UserOrder",
  data() {
    return {
      order_list: []
    };
  },
  created() {
    this.get_user_order();
  },
  filters: {
    timeformat(value) {
      let datetime = new Date(value);
      let Y = datetime.getFullYear(); // 年
      let m = datetime.getMonth() + 1;
      let d = datetime.getDate();
      let H = datetime.getHours();
      let M = datetime.getMinutes();
      let S = datetime.getSeconds();
      m = m < 10 ? '0' + m : m;
      d = d < 10 ? '0' + d : d;
      H = H < 10 ? '0' + H : H;
      M = M < 10 ? '0' + M : M;
      S = S < 10 ? '0' + S : S;
      return `${Y}-${m}-${d} ${H}:${M}`;
    }
  },
  methods: {
    check_login() {
      // 检查当前访问者是否登录了！
      let token = localStorage.user_token || sessionStorage.user_token;
      if (!token) {
        this.$alert("对不起，您尚未登录，请登录以后再进行购物车").then(() => {
          this.$router.push("/user/login");
        });
        return false; // 阻止代码往下执行
      }
      return token;
    },
    get_user_order() {
      // 获取当前登录用户的所有订单
      let token = this.check_login();
      this.$axios.get(`${this.$settings.HOST}/user/order/`, {
        headers: {
          "Authorization": `Bearer ${token}`
        },
      }).then(response => {
        this.order_list = response.data;
      }).catch(error => {
        this.$message.error(error.response.data.message + "有问题，请重新登录");
      })
    },
    gotopay(order_number) {
      // 生成支付订单的链接地址
      this.$axios.get(`${this.$settings.HOST}/payments/alipay/`, {
        params: {
          order_number: order_number
        }
      }).then(response => {
        // 跳转至支付页面
        location.href = response.data.url;
      }).catch(error => {
        this.$message.error(error.response.data.message + "订单生成失败");
      })
    }
  },
  components: {
    Header,
    Footer,
  }
}
</script>

<style scoped>
.main .banner {
  width: 100%;
  height: 324px;
  background: url(../../static/image/my_bkging.0648ebe.png) no-repeat;
  background-size: cover;
  z-index: 1;
}

.profile {
  width: 1200px;
  margin: 0 auto;
}

.profile-info {
  text-align: center;
  margin-top: -80px;
}

.avatar {
  width: 120px;
  height: 120px;
  border-radius: 60px;
  overflow: hidden;
  margin: 0 auto;
}

.user-name {
  display: block;
  font-size: 24px;
  color: #4a4a4a;
  margin-top: 14px;
}

.user-job {
  display: block;
  font-size: 11px;
  color: #9b9b9b;
}

.my-item {
  list-style: none;
  line-height: 1.42857143;
  color: #333;
  width: 474px;
  height: 31px;
  display: -ms-flexbox;
  display: flex;
  cursor: pointer;
  margin: 41px auto 0;
  -ms-flex-pack: justify;
  justify-content: space-between;
}

.my-item .active {
  border-bottom: 1px solid #000;
}

.user-data {
  width: 1200px;
  height: auto;
  margin: 0 auto;
  padding-top: 30px;
  border-top: 1px solid #e8e8e8;
  margin-bottom: 63px;
}

.nav {
  width: 100%;
  height: 60px;
  background: #e9e9e9;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
}

.nav li {
  margin-left: 20px;
  margin-right: 28px;
  height: 60px;
  line-height: 60px;
  list-style: none;
  font-size: 13px;
  color: #333;
  border-bottom: 1px solid #e9e9e9;
  width: 160px;
}

.nav .order-info {
  width: 325px;
}

.nav .course-expire {
  width: 60px;
}

.nav .course-price {
  width: 130px;
}

.user-data-header {
  display: flex;
  height: 44px;
  color: #4a4a4a;
  font-size: 14px;
  background: #f3f3f3;
  -ms-flex-align: center;
  align-items: center;
}

.order-time {
  font-size: 12px;
  display: inline-block;
  margin-left: 20px;
}

.order-num {
  font-size: 12px;
  display: inline-block;
  margin-left: 29px;
}

.user-data-list {
  height: 100%;
  display: flex;
}

.user-data-list {
  display: flex;
  align-items: center; /* 垂直对齐 */
  padding: 18px 0; /* 增加垂直间距 */
  background: none;
}

.user-data-list li {
  display: flex;
  align-items: center; /* 垂直对齐 */
  justify-content: center; /* 水平对齐 */
  height: 60px;
  line-height: 60px;
  flex: 1; /* 等分宽度 */
  padding: 18px 0;
}

.user-data-list .order-info {
  display: flex;
  align-items: center;
  margin-right: 28px;
}

.user-data-list .order-info img {
  max-width: 100px;
  max-height: 75px;
  margin-right: 22px;
}

.course-title {
  width: 203px;
  font-size: 13px;
  color: #333;
  line-height: 20px;
  margin-top: -10px;
}

.order-info-title .price-service {
  line-height: 18px;
}

.price-service {
  font-size: 12px;
  color: #fa6240;
  padding: 0 5px;
  border: 1px solid #fa6240;
  border-radius: 4px;
  margin-top: 4px;
  position: absolute;
}

.order-info-title {
  margin-top: -10px;
}

.user-data-list .course-expire {
  font-size: 12px;
  color: #ff5502;
  width: 60px;
  text-align: center;
}

.btn {
  width: 100px;
  height: 32px;
  font-size: 14px;
  color: #fff;
  background: #ffc210;
  border-radius: 4px;
  border: none;
  outline: none;
  transition: all .25s ease;
  display: inline-block;
  line-height: 32px;
  text-align: center;
  cursor: pointer;
}
</style>
