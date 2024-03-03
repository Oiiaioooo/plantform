<template>
  <div>
    <h1>电阻箱设置</h1>
    <div class="knob-group">
      <p class="knob_describe_text">X1000Ω</p>
      <p class="knob_describe_text">X100Ω</p>
      <p class="knob_describe_text">X10Ω</p>
      <p class="knob_describe_text">X1Ω</p>
    </div>
    <div class="knob-group">
      <round-slider class="knob" radius="50" min="0" max="10" v-model="form.x1000"></round-slider>
      <round-slider class="knob" radius="50" min="0" max="10" v-model="form.x100"></round-slider>
      <round-slider class="knob" radius="50" min="0" max="10" v-model="form.x10"></round-slider>
      <round-slider class="knob" radius="50" min="0" max="10" v-model="form.x1"></round-slider>
    </div>
    <div>
      <h1>总电阻</h1>
      <p>{{form.x1000*1000 + form.x100*100 + form.x10*10 + form.x1}}Ω</p>
      <el-button type="primary" @click="onSubmit">保存</el-button>
    </div>

  </div>
</template>

<script>
export default {
  name: "ResistanceBox",
  props: {
    nodeData: Object,
    lf: Object || String,
  },
  data() {
    return {
      form: {
        x1000: 0,
        x100: 0,
        x10: 0,
        x1: 0,
      }
    }
  },
  methods: {
    onSubmit() {
      console.log('保存电阻箱设置!');
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
.knob-group{
  display: flex;
}
  .knob_describe_text{
    text-align: center;
    flex: 1;
  }
  .knob{
    flex:1;
  }
</style>
