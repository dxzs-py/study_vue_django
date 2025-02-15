<template>
    <div class="home">
      <Header></Header>  <!-- 头部 -->
      <Banner></Banner>  <!-- 轮播图 -->
      <Footer></Footer> <!-- 底部 -->
    </div>
</template>

<script>
  import Header from "./common/Header"
  import Banner from "./common/Banner"
  import Footer from "./common/Footer"
  export default {
      name: "Home",
      data(){
        return {}
      },
      methods:{

      },
      components:{
        Header,
        Footer,
        Banner,
      }
  }
</script>

<style scoped>

</style>


