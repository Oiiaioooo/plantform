<template>
<div>
  <h1>电容箱设置</h1>
  <el-row class="knob-group">
    <el-col :span="6"><p class="knob_describe_text">X0.1μF</p></el-col>
    <el-col :span="6"><p class="knob_describe_text">X0.01μF</p></el-col>
    <el-col :span="6"><p class="knob_describe_text">X0.001μF</p></el-col>
    <el-col :span="6"><p class="knob_describe_text">X0.0001μF</p></el-col>
  </el-row>
  <el-row>
    <el-col :span="6"><round-slider class="knob" radius="50" min="0" max="10" v-model="form.x0_1"></round-slider></el-col>
    <el-col :span="6"><round-slider class="knob" radius="50" min="0" max="10" v-model="form.x0_01"></round-slider></el-col>
    <el-col :span="6"><round-slider class="knob" radius="50" min="0" max="10" v-model="form.x0_001"></round-slider></el-col>
    <el-col :span="6"><round-slider class="knob" radius="50" min="0" max="10" v-model="form.x0_0001"></round-slider></el-col>
  </el-row>
  <div>
    <h1>总电容</h1>
    <p>{{(form.x0_1*0.1 + form.x0_01*0.01 + form.x0_001*0.001 + form.x0_0001*0.0001).toFixed(4)}}μF</p>
    <el-button type="primary" @click="onSubmit">保存</el-button>
  </div>
</div>
</template>

<script>
export default {
  name: "CapacitanceBox",
  props: {
    nodeData: Object,
    lf: Object || String,
  },
  data() {
    return {
      form: {
        x0_1: 0,
        x0_01: 0,
        x0_001: 0,
        x0_0001: 0,
      }
    }
  },
  methods: {
    onSubmit() {
      console.log('保存电容箱设置!');
      const nodeData = this.$props.nodeData
      nodeData.properties = this.$data.form
      this.$props.lf.setProperties(nodeData.id, this.$data.form);
      this.$emit('onClose')
    }
  },
  mounted() {
    const {properties} = this.$props.nodeData
    if (properties) {
      this.$data.form = Object.assign({}, this.$data.form, properties)
    }
  },
}
</script>

<style scoped>
.knob_describe_text{
  text-align: center;
  flex: 1;
}
</style>
