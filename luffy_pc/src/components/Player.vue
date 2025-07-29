<template>
  <div class="player">
    <div id="player"></div>
  </div>
</template>

<script>
export default {
  name: "Player",
  data() {
    return {
      vodPlayerJs: 'https://player.polyv.net/resp/vod-player/latest/player.js',
      player: null
    }
  },
  methods: {
    check_login() {
      // 检查当前访问者是否登录了！
      let token = localStorage.user_token || sessionStorage.user_token;
      if (!token) {
        this.$alert("对不起，您尚未登录，请登录以后再进行学习。").then(() => {
          this.$router.push("/user/login");
        });
        return false; // 阻止代码往下执行
      }
      return token;
    },

    // 因为index.html中的polyvPlayer.js加载顺序问题，所以这里要手动加载，当然我改了源码，可以不用手动加载了
    loadPlayerScript(callback) {
      if (!window.polyvPlayer) {
        const myScript = document.createElement('script');
        myScript.setAttribute('src', this.vodPlayerJs);
        myScript.onload = callback;
        document.body.appendChild(myScript);
      } else {
        callback();
      }
    },

    loadPlayer() {
      let jwt_token = this.check_login();
      let user_name = localStorage.user_name || sessionStorage.user_name;
      // 1.到数据库中查询用户购买的课程是否有当前章节
      // 2.到数据库中查询当前用户购买的课程是否有效期内
      let vid = this.$route.query.vid;
      let self = this;

      const polyvPlayer = window.polyvPlayer;
      this.player = polyvPlayer({
        wrap: '#player',
        width: document.documentElement.clientWidth - 260, // 页面宽度
        height: document.documentElement.clientHeight, // 页面高度
        forceH5: true,
        vid: vid,
        code: user_name, // 一般是用户昵称
        // 视频加密播放的配置
        playsafe: function (vid, next) { // 向后端发送请求获取加密的token
          self.$axios.get(`${self.$settings.HOST}/course/player/`, {
            params: {
              vid: vid,
            },
            headers: {
              "Authorization": `Bearer ${jwt_token}`
            },
          }).then(function (response) {
            // 获取播放视频的token令牌
            next(response.data);
          })
        }
      });
    }
  },
  // created 初始化，放置的是ajax等操作/获取数据的代码，不涉及操作页面
  // mounted 初始化，放置的是关于操作页面的初始化js代码
  mounted() {
    this.loadPlayerScript(this.loadPlayer);
  },
  computed: {},
  destroyed() {
    if (this.player) {
      this.player.destroy();
    }
  }
}
</script>

<style scoped>

</style>
