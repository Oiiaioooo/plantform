<template>
  <div>
    <el-form ref="form" :model="anchorCnode">
      <div v-for="(anchor, index) in nodeData.Anchors" :key="index">
        <el-form-item :label="anchor.type">
          <el-select v-model="anchorCnode[anchor.type]" placeholder="请选择电路节点编号">
            <el-option
                v-for="i in 23"
                :key="i"
                :label="`C${i}`"
                :value="`C${i}`">
            </el-option>
          </el-select>
        </el-form-item>
      </div>
      <el-button type="primary" @click="onSubmit">保存</el-button>
    </el-form>
  </div>
</template>


<script>
export default {
  name: "SetAnchorCNodeNumber",
  props: {
    nodeData: Object,
    lf: Object || String,
    user: Object
  },
  data() {
    return {
      anchorCnode: {}
    }
  },
  methods: {
    onSubmit() {
      const nodeData = this.$props.nodeData
      nodeData.properties.anchorCnode = this.anchorCnode
      this.$props.lf.setProperties(nodeData.id, nodeData.properties);
    }
  },
  mounted() {
    const {properties} = this.$props.nodeData
    if (properties && properties.anchorCnode) {
      this.anchorCnode = properties.anchorCnode
    }
  },
}



</script>



<style>

</style>
