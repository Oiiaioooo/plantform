<template>
  <div>
    <el-form ref="form" :model="form" :rules="rules">
      <h1>直流电源设置</h1>
      <h3>通道1设置(0-30V 0-3A)</h3>
      <el-row style="text-align: center">
        <el-col :span="9" >电压V</el-col>
        <el-col :span="9">电流A</el-col>
        <el-col :span="6">开关</el-col>
      </el-row>
      <el-row>
        <el-col :span="9">
          <el-form-item prop="voltage1">
          <el-input-number size="small" :min="0" :max="v_Max.voltage1" type="number" v-model="form.voltage1"
                           :placeholder="'最高'+v_Max.voltage1+'V'"></el-input-number>
        </el-form-item>
        </el-col>
        <el-col :span="9">
          <el-form-item prop="current1">
          <el-input-number size="small"  :min="0" :max="i_Max.current1" type="number" v-model="form.current1"
                           :placeholder="'最高'+i_Max.current1+'A'"></el-input-number>
        </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-switch  active-text="开启" inactive-text="关闭" v-model="form.CH1_stat"></el-switch>
        </el-col>
      </el-row>



      <h3>通道2设置(0-30V 0-3A)</h3>
      <el-row>
        <el-col :span="9">
          <el-form-item prop="voltage2">
            <el-input-number size="small" :min="0" :max="v_Max.voltage2" type="number" v-model="form.voltage2"
                             :placeholder="'最高'+v_Max.voltage2+'V'"></el-input-number>
          </el-form-item>
        </el-col>
        <el-col :span="9">
          <el-form-item prop="current2">
            <el-input-number size="small"  :min="0" :max="i_Max.current2" type="number" v-model="form.current2"
                             :placeholder="'最高'+i_Max.current2+'A'"></el-input-number>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-switch  active-text="开启" inactive-text="关闭" v-model="form.CH2_stat"></el-switch>
        </el-col>
      </el-row>


      <h3>通道3电压设置(0-5V 0-3A)</h3>
      <el-row>
        <el-col :span="9">
          <el-form-item prop="voltage3">
            <el-input-number size="small" :min="0" :max="v_Max.voltage3" type="number" v-model="form.voltage3"
                             :placeholder="'最高'+v_Max.voltage3+'V'"></el-input-number>
          </el-form-item>
        </el-col>
        <el-col :span="9">
          <el-form-item prop="current3">
            <el-input-number size="small"  :min="0" :max="i_Max.current3" type="number" v-model="form.current3"
                             :placeholder="'最高'+i_Max.current3+'A'"></el-input-number>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-switch  active-text="开启" inactive-text="关闭" v-model="form.CH3_stat"></el-switch>
        </el-col>
      </el-row>
    </el-form>
    <el-button type="primary" @click="getConfig">当前设置</el-button>
    <el-button type="primary" @click="onSubmit">保存设置</el-button>
    <el-button type="primary" @click="getData">获取数据</el-button>
    <el-table
        :data="form.powerSupplyData"
        style="width: 100%">
      <el-table-column
          prop="channel"
          label="通道">
      </el-table-column>
      <el-table-column
          prop="voltage"
          label="电压">
      </el-table-column>
      <el-table-column
          prop="current"
          label="电流">
      </el-table-column>
      <el-table-column
          prop="power"
          label="功率">
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: "DCPowerSupply",
  props: {
    nodeData: Object,
    lf: Object || String,
  },
  data() {
    return {
      v_Max: {
        voltage1: 30,
        voltage2: 30,
        voltage3: 5,
      },
      i_Max:{
        current1:3,
        current2:3,
        current3:3,
      },
      // 要保存到节点里的数据全部放在form中
      form: {
        CH1_stat: false,
        CH2_stat: false,
        CH3_stat: false,
        voltage1: 0,
        voltage2: 0,
        voltage3: 0,
        current1: 0,
        current2: 0,
        current3: 0,
        powerSupplyData:[],
      },

      rules: {
        voltage1: [
          {required: true, message: '请输入电压'},
          {
            validator: (rule, value, callback) => {
              if (value < 0 || value > 30) {
                callback(new Error('电压范围为0-30V'));
              } else {
                callback();
              }
            }
          },
        ],
        voltage2: [
          {required: true, message: '请输入电压'},
          {
            validator: (rule, value, callback) => {
              if (value < 0 || value > 30) {
                callback(new Error('电压范围为0-30V'));
              } else {
                callback();
              }
            }
          },
        ],
        voltage3: [
          {required: true, message: '请输入电压'},
          {
            validator: (rule, value, callback) => {
              if (value < 0 || value > 5) {
                callback(new Error('电压范围为0-5V'));
              } else {
                callback();
              }
            }
          },
        ],
        current1: [
          {required: true, message: '请输入电流'},
          {
            validator: (rule, value, callback) => {
              if (value < 0 || value > this.i_Max.current1) {
                callback(new Error('电流超出范围'));
              } else {
                callback();
              }
            }
          },
        ],
        current2: [
          {required: true, message: '请输入电流'},
          {
            validator: (rule, value, callback) => {
              if (value < 0 || value > this.i_Max.current2) {
                callback(new Error('电流超出范围'));
              } else {
                callback();
              }
            }
          },
        ],
        current3: [
          {required: true, message: '请输入电流'},
          {
            validator: (rule, value, callback) => {
              if (value < 0 || value > this.i_Max.current3) {
                callback(new Error('电流超出范围'));
              } else {
                callback();
              }
            }
          },
        ],
      },

    }

  },
  methods: {
    // 获得设置
    getConfig(){
      this.$get('/api/dp832/config/').then(msg=>{
        console.log(msg)
        this.form.CH1_stat = msg.output_states[0]
        this.form.CH2_stat = msg.output_states[1]
        this.form.CH3_stat = msg.output_states[2]
        this.form.voltage1 = msg.voltages[0]
        this.form.voltage2 = msg.voltages[1]
        this.form.voltage3 = msg.voltages[2]
        this.form.current1 = msg.currents[0]
        this.form.current2 = msg.currents[1]
        this.form.current3 = msg.currents[2]
        const nodeData = this.$props.nodeData
        nodeData.properties = Object.assign({},nodeData.properties,this.form)
        this.$props.lf.setProperties(nodeData.id, nodeData.properties);
      })
    },
    // 采集数据
    getData(){
      this.$get('/api/dp832/data/').then(msg=>{
        this.form.powerSupplyData=msg
      //  将数据保存在节点的属性中
        const nodeData = this.$props.nodeData
        nodeData.properties = Object.assign({},nodeData.properties,this.form)
        this.$props.lf.setProperties(nodeData.id, nodeData.properties);
      })
    },
    onSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          // console.log('保存直流电源设置!');
          const nodeData = this.$props.nodeData
          //将数据保存在节点的属性中
          nodeData.properties = Object.assign({},nodeData.properties,this.form)
          this.$props.lf.setProperties(nodeData.id, nodeData.properties);
          // this.$emit('onClose')
          this.$message({
                message: '保存成功',
                type: 'success'
              }
          );
          //向后端发送post请求，控制电源
          const data = {
            channels:[1,2,3],
            voltages:[this.form.voltage1,this.form.voltage2,this.form.voltage3],
            currents:[this.form.current1,this.form.current2,this.form.current3],
            output_states:[this.form.CH1_stat,this.form.CH2_stat,this.form.CH3_stat]
          }
          this.$post('/api/dp832/',data)

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
      // 将节点属性与form属性合并，若重名，则覆盖form属性
      this.$data.form = Object.assign({}, this.$data.form, properties)
    }
  },
}
</script>

<style scoped>

</style>
