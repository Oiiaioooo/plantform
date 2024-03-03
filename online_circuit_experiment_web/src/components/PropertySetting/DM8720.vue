<template>
  <div>
    <el-button type="primary" @click="getData">获取数据</el-button>
    <el-table :data="form.multimeterData" style="width: 100%">
      <el-table-column prop="Voltage" label="Voltage(V)"></el-table-column>
      <el-table-column prop="Current" label="Current(A)"></el-table-column>
      <el-table-column prop="Power" label="Power(W)"></el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: "DM8720",
  props: {
    nodeData: Object,
    lf: Object || String,
  },
  mounted() {
    this.getData()
  },
  data(){
    return{
      form:{
        multimeterData:[]
      }
    }
  },
  methods:{
    getData(){
      this.$get('/api/dm8720/data/').then(res=>{
        this.form.multimeterData = [res]
      })
    }
  }
}
</script>

<style>

</style>
