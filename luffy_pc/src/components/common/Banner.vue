<template>
  <el-carousel height="720px" :interval="3000" arrow="always">
    <el-carousel-item v-for="(banner,index) in banner_list" :key="index">
      <a :href="banner.link | safeUrl">
        <img :src="banner.image_url | safeSrc" alt="">
      </a>
    </el-carousel-item>

  </el-carousel>
</template>

<script>
export default {
  // 定义组件名称为 "Banner"
  name: "Banner",

  // 定义组件的数据属性
  data() {
    return {
      // 存储轮播广告列表的数组
      banner_list: []
    }
  },

  // 在组件创建时执行的方法
  created() {
    // 调用获取轮播广告列表的方法
    this.get_banner_list();
  },

  // 定义组件的方法
  methods: {
    /**
     * 获取轮播广告列表
     * 本方法通过发送GET请求到服务器，获取轮播广告数据，并将其保存到组件的data属性中
     */
    get_banner_list() {
      // 使用axios库发送GET请求获取轮播广告列表
      this.$axios.get(`${this.$settings.HOST}/banner/`, {}).then(response => {
        // 成功获取数据后，将其保存到data中定义的banner_list数组中
        this.banner_list = response.data;
      }).catch(error => {
        // 请求失败时，打印错误信息到控制台
        console.log(error.response)
      });
    }
  }
}

</script>

<style scoped>
.el-carousel__item h3 {
  color: #475669;
  font-size: 18px;
  opacity: 0.75;
  line-height: 300px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n+1) {
  background-color: #d3dce6;
}
</style>
