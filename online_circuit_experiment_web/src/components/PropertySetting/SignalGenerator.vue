<template>
  <div>
    <h1>信号源设置</h1>
    <el-form ref="form" :model="form">
      <el-row>
        <el-col :span="3">
          <p>输出</p>
        </el-col>
        <el-col :span="6">
          <el-switch
              active-text="开启" inactive-text="关闭"
              v-model="form.ch1.output"></el-switch>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item>
            <el-input size="small" type="text" value="请选择波形" disabled
                      placeholder="请选择波形">
              <template slot="prepend">波形</template>
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-select size="small" v-model="form.ch1.function_type">
            <el-option v-for="item in form.ch1.function_type_options" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item>
            <el-input size="small" type="number" v-model="form.ch1.voltage"
                      placeholder="输入幅值">
              <template slot="prepend">幅值</template>
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-select size="small" v-model="form.ch1.voltage_unit">
            <el-option v-for="item in form.ch1.voltage_unit_options" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-col>
      </el-row>
<!--      v-show是基于css的切换，v-if会卸载dom节点移除元素-->

      <el-row v-show="form.ch1.frequency_or_period">
        <el-col :span="12">
          <el-form-item>
            <el-input size="small" type="number" v-model="form.ch1.frequency"
                      placeholder="输入频率" disabled>
              <template slot="prepend">频率</template>
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-select size="small" v-model="form.ch1.frequency_unit">
            <el-option v-for="item in form.ch1.frequency_unit_options" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-col>

      </el-row>
      <el-row v-show="!(this.form.ch1.frequency_or_period)">
        <el-col :span="12">
          <el-form-item>
            <el-input size="small" type="number" v-model="form.ch1.period"
                      placeholder="输入周期">
              <template slot="prepend">周期</template>
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-select size="small" v-model="form.ch1.period_unit">
            <el-option v-for="item in form.ch1.period_unit_options" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item>
            <el-input size="small" type="number" v-model="form.ch1.offset"
                      placeholder="输入偏移">
              <template slot="prepend">偏移</template>
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-select size="small" v-model="form.ch1.offset_unit">
            <el-option v-for="item in form.ch1.offset_unit_options" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-col>
      </el-row>
      <el-row v-show="form.ch1.function_type==='square'">
        <el-col :span="16">
          <el-form-item>
            <el-input size="small" type="number" v-model="form.ch1.dcycle"
                      placeholder="输入占空比">
              <template slot="prepend">占空比</template>
              <template slot="append">%</template>
            </el-input>
          </el-form-item>
        </el-col>
      </el-row>

    </el-form>

    <el-button type="primary" @click="onSubmit">保存设置</el-button>
  </div>
</template>

<script>
export default {
  name: "SignalGenerator",
  props: {
    nodeData: Object,
    lf: Object || String,
  },
  watch: {
    'form.ch1.voltage': function(val) {
      if (val < 0) {
        this.form.ch1.voltage = 0;
      } else if (val > 3) {
        this.form.ch1.voltage = 3;
      }
    }
  },
  data() {
    return {

      form: {
        ch1:{
          output:false,
          function_type:"sinusoid",
          function_type_options:[{label:'sinusoid',value:'sinusoid'},{label:'square',value:'square'},{label:'ramp',value:'ramp'},{label:'pulse',value:'pulse'}],
          voltage:1,
          voltage_unit:"Vrms",
          voltage_unit_options:[{label:'Vrms',value:'Vrms'},{label:'mVrms',value:'mVrms'},{label:'Vpp',value:'Vpp'},{label:'mVpp',value:'mVpp'}],
          frequency_or_period:true,
          frequency:50,
          frequency_unit:"Hz",
          frequency_unit_options:[{label:'MAHz',value:'MAHz'},{label:'kHz',value:'kHz'},{label:'Hz',value:'Hz'},{label:'mHz',value:'mHz'},{label:'uHz',value:'uHz'}],
          period:1,
          period_unit:"ms",
          period_unit_options:[{label:'ks',value:'ks'},{label:'s',value:'s'},{label:'ms',value:'ms'},{label:'us',value:'us'},{label:'ns',value:'ns'}],
          offset:0,
          offset_unit:"mV",
          offset_unit_options:[{label:'V',value:'V'},{label:'mV',value:'mV'}],
          phase:0,
          dcycle:50
        },
        ch2:{
          function_type:"",
          function_options:[],
          voltage:"",
          voltage_unit:"",
          voltage_unit_options:[],
          frequency:"",
          frequency_unit:"",
          frequency_unit_options:[],
          period:"",
          period_unit:"",
          period_unit_options:[],
          offset:"",
          phase:"",
        },
      },

    }

  },
  methods: {
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
          this.$post('/api/tfg6930a/',this.form.ch1).then(msg=>{console.log(msg)})
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
