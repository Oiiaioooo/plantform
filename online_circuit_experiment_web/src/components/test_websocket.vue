<template>
<div>测试websocket
<el-input v-model="text1"></el-input>
  <el-input v-model="text2"></el-input>
  <el-input v-model="text3"></el-input>
  <el-input-number v-model="number1"></el-input-number>
  <el-button @click="send"></el-button>
</div>

</template>

<script>
import * as io from 'socket.io-client'

export default {
  name: "test_websocket",
  data(){
    return{
      number1:1,
      text1:"",
      text2:"",
      text3:""
    }
  },
  mounted() {
    var sockets = io.connect("http://127.0.0.1:8000")
    sockets.on('server',msg=>{console.log(msg)})
    sockets.on('power',msg=>{this.text1=msg})
    sockets.on('multimeter',msg=>{this.text2=msg})
    sockets.on('oscilloscope',msg=>{this.text3=msg})
    // this.$get('/test/').then(msg=>console.log(msg))
  },
  methods:{
    send(){
      this.$post('/test/',{t:this.number1}).then(msg=>console.log(msg))
    }
  }
}
</script>

<style scoped>

</style>
