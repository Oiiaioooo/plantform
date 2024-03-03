<template>
  <div>
    <h1>实验现场</h1>
    <el-button ref="viedo_play" @click="togglePlay">播放</el-button>
    <div id="video-container"></div>
  </div>

</template>

<script>
import EZUIKit from "ezuikit-js";

export default {
  name: "ExpVideoLiving",
  data() {
    return {
      player: null,
      play: false,

    }
  },
  beforeDestroy() {
    if (this.play) this.player.stop();
  },
  mounted() {
    console.group("mounted 组件挂载完毕状态===============》");
    // 由于这里我们暂时没有使用video，所以取消
    this.player = new EZUIKit.EZUIKitPlayer({

      autoplay: false,
      id: "video-container",
      accessToken: "at.9zrxl7545cgpmwac1iat2wzhac1cnhb5-51d8s21avv-19hetun-q4tfumsov",
      url: "ezopen://open.ys7.com/G82053146/1.live",
      template: "security", // simple - 极简版;standard-标准版;security - 安防版(预览回放);voice-语音版；
      audio: 0, // 是否默认开启声音 0 - 关闭 1 - 开启
      width: 750,
      height: 450
    });
  },
  methods: {
    togglePlay() {
      if (!this.player) return;
      switch (this.play) {
        case true:
          this.player.stop();
          this.play = false;
          this.$refs.viedo_play.$el.innerText = '播放';
          break;
        case false:
          this.player.play();
          this.play = true;
          this.$refs.viedo_play.$el.innerText = '暂停';
          break;
        default:
          break;
      }
    }
  }
}
</script>

<style scoped>

</style>
