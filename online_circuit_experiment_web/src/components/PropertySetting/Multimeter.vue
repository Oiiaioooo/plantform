<template>
  <div>
    <el-form ref="form" :model="form">
      <h1>万用表设置</h1>
      <h3>模式选择</h3>
      <el-form-item>
        <el-select size="small" v-model="form.mode1_value">
          <el-option v-for="item in form.mode1_options" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <el-select size="small" v-model="form.mode2_value">
          <el-option v-for="item in form.mode2_options" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-form-item>
    </el-form>
    <el-button type="primary" @click="onSubmit">保存设置</el-button>
    <el-button type="primary" @click="getData">获取数据</el-button>
    <el-button type="primary" @click="delData">删除数据</el-button>
    <el-table
        @selection-change="handleSelectionChange"
        ref="table"
        :data="form.multimeterData"
        :default-sort = "{prop: 'time', order: 'descending'}"
        style="width: 100%">
      <el-table-column
          type="selection"
          >
      </el-table-column>
      <el-table-column
          sortable
          prop="time"
          label="测量时间">
      </el-table-column>
      <el-table-column
          prop="mode1"
          label="模式1">
      </el-table-column>
      <el-table-column
          prop="mode2"
          label="模式2">
      </el-table-column>
      <el-table-column
          sortable
          prop="value"
          label="数值">
      </el-table-column>
      <el-table-column
          prop="unit"
          label="单位">
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: "Multimeter",
  props: {
    nodeData: Object,
    lf: Object || String,
  },
  data() {
    return {

      form: {
        mode1_options:[{label:'voltage',value:'voltage'},{label: 'current',value:'current'}],
        mode1_value:"voltage",
        mode2_options:[{label:'dc',value:'dc'},{label: 'ac',value:'ac'}],
        mode2_value:"dc",
        multimeterData:[]
      },
      multipleSelection: []
    }

  },
  methods: {
    // 从后端拿到select里面的options
    getOptions(){
      this.$get()
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    delData(){
      for (var index in this.multipleSelection){
        this.form.multimeterData.splice(index-1,1)
      }
      this.$refs.table.clearSelection()
      const nodeData = this.$props.nodeData
      // 可优化的地方，不需要每次都用整个form去更新，部分更新就行了
      nodeData.properties = this.$data.form
      this.$props.lf.setProperties(nodeData.id, this.$data.form);
    },
    getData(){
      this.$post('/api/dm3058/data/',{mode1:this.form.mode1_value,mode2:this.form.mode2_value}).then(msg=>{
        this.form.multimeterData.push(msg)
        const nodeData = this.$props.nodeData
        // 可优化的地方，不需要每次都用整个form去更新，部分更新就行了
        nodeData.properties = this.$data.form
        this.$props.lf.setProperties(nodeData.id, this.$data.form);
      })
    },
    onSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          const nodeData = this.$props.nodeData
          nodeData.properties = this.$data.form
          this.$props.lf.setProperties(nodeData.id, this.$data.form);
          this.$message({
                message: '保存成功',
                type: 'success'
              }
          );
        } else {
          this.$message({
            message: '保存失败',
            type: 'error'
          });
        }

      });

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

</style>
