<template>
  <div>
    <el-form ref="form" :model="form">
      <h1>示波器设置</h1>
    </el-form>
    <div>
      <el-button @click="$_getCurve">获取波形</el-button>
      <div ref="Echarts" style="width: 100%;height:400px;"></div>
    </div>
  </div>
</template>

<script>

export default {
  name: "Oscilloscope",

  props: {
    nodeData: Object,
    lf: Object || String,
  },
  data() {
    return {
      form: {
        curve:{
          ch1:[],
          ch2:[]
        }
      },
    }

  },
  methods: {
    myEChart() {
      this.myChart = this.$echarts.init(this.$refs.Echarts)
      var option = {
        toolbox: {
          show: true,
          feature: {
            dataZoom: {
              yAxisIndex: 'none'
            },
            // dataView: {
            //   readOnly: false
            // },
            // magicType: {
            //   type: ['line', 'bar']
            // },
            restore: {},
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'value',
        },
        yAxis: {
          type: 'value',
        },
        series: [
          {
            name: '通道1',
            type: 'line',
            data: [],
          },
          {
            name: '通道2',
            type: 'line',
            data: [],
          }
        ]
      };
      this.myChart.setOption(option)
      // window.addEventListener("resize",()=>{myChart.resize()})
    },
    setOptions(data1, data2) {
      var option = {
        legend: {
          data: ['通道1', '通道2']
        },
        animation: false,
        tooltip: {
          // trigger: 'axis',
          // axisPointer: {
          //   type: 'cross'
          // },
          alwaysShowContent: true,
          triggerOn: 'none',
          // position: function (pt) {
          //   return [pt[0], 130];
          // }
          backgroundColor: 'rgba(255, 255, 255, 0.8)',
          position: function (pos, params, el, elRect, size) {
            var obj = {top: 10};
            obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
            return obj;
          },
          extraCssText: 'width: 170px'
        },
        axisPointer: {

          link: {xAxisIndex: 'all'},
          handle: {size: 30},
          label: {
            backgroundColor: '#777'
          }
        },
        toolbox: {
          show: true,
          feature: {
            dataZoom: {
              yAxisIndex: false
            },
            brush: {
              type: ['lineX', 'clear']
            },
            // dataView: {
            //   readOnly: false
            // },
            // magicType: {
            //   type: ['line', 'bar']
            // },
            saveAsImage: {}
          }
        },
        brush: {
          xAxisIndex: 'all',
          brushLink: 'all',
          outOfBrush: {
            colorAlpha: 0.1
          }
        },

        dataZoom: [
          {
            filterMode: 'none',
            type: 'slider',
            show: true,
            xAxisIndex: [0],
            start: 0,
            end: 100
          },
          {
            filterMode: 'none',
            type: 'slider',
            show: true,
            yAxisIndex: [0],
            // left: '93%',
            start: 0,
            end: 100
          },
          {
            filterMode: 'none',
            type: 'inside',
            xAxisIndex: [0],
            start: 0,
            end: 100
          },
          {
            filterMode: 'none',
            type: 'inside',
            yAxisIndex: [0],
            start: 0,
            end: 100
          }
        ],
        xAxis: {
          type: 'value',
          axisPointer: {
            snap: false,
            lineStyle: {
              color: '#7581BD',
              width: 2
            },
            label: {
              show: true,
              // precision:'auto',
              // formatter: function (params) {
              //   return echarts.format.formatTime('yyyy-MM-dd', params.value);
              // },
              backgroundColor: '#7581BD'
            },
            handle: {
              show: true,
              color: '#7581BD'
            }
          },
        },
        yAxis: {
          type: 'value',

          axisPointer: {
            triggerTooltip: false,
            //关闭吸附，且关闭tooltip的话就没有吸附了，如果打开tooltip就还有吸附
            snap: false,
            lineStyle: {
              color: '#7581BD',
              width: 2
            },
            label: {
              show: true,
              // formatter: function (params) {
              //   return echarts.format.formatTime('yyyy-MM-dd', params.value);
              // },
              backgroundColor: '#7581BD'
            },
            handle: {
              show: true,
              color: '#7581BD'
            }
          },
        },
        series: [
          {
            name: '通道1',
            type: 'line',

            showSymbol: false,
            data: data1,
          },
          {
            name: '通道2',
            type: 'line',
            showSymbol: false,
            data: data2,
          }
        ]
      };
      this.myChart.setOption(option)
    },
    $_getCurve(){
      this.$get('/api/tbs1202b/data/').then(msg => {
        var w1 = Array.from(msg.ch1.time, (item, idx) => [item, msg.ch1.wave[idx]])
        var w2 = Array.from(msg.ch2.time, (item, idx) => [item, msg.ch2.wave[idx]])
        this.setOptions(w1, w2)
        this.form.curve.ch1=w1
        this.form.curve.ch2=w2
        const nodeData = this.$props.nodeData
        nodeData.properties = Object.assign({},nodeData.properties,this.form)
        this.$props.lf.setProperties(nodeData.id, nodeData.properties);


      })


      // this.$message({
      //       message: '获取数据成功',
      //       type: 'success'
      //     }
      // );
    },
  },
  mounted() {
    const {properties} = this.$props.nodeData
    if (properties) {
      this.$data.form = Object.assign({}, this.$data.form, properties)
    }
    this.myEChart()
    this.setOptions(this.form.curve.ch1,this.form.curve.ch2)
  },
}
</script>

<style scoped>

</style>
