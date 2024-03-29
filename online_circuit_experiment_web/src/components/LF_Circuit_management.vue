<template>
  <div class="logic-flow-view">
    <!-- Header section with remaining time and logout -->
    <div class="flex-container">
      <div class="centered-content">
        <h3 class="demo-title">远程实验平台</h3>
      </div>
      <RemainingTime />
      <Logout />
    </div>


    <!-- 辅助工具栏 -->
    <Control
        class="demo-control"
        v-if="lf"
        :lf="lf"
        @catData="$_catData"
        @saveData="$_saveData"
        @loadData="$_loadData"
        @executeConnect="$_executeConnect"
        @saveInitData="$_saveInitData"
    ></Control>
    <!-- 节点面板 -->
    <NodePanel v-if="lf" :lf="lf" :nodeList="CircuitnodeList" v-show="true"></NodePanel>
    <!-- 画布 -->
    <div id="LF-view" ref="container"></div>
    <!-- 用户节点自定义操作面板 -->
    <!--  似乎是借此增加节点  -->
    <AddPanel
        v-if="showAddPanel"
        class="add-panel"
        :style="addPanelStyle"
        :lf="lf"
        :nodeData="addClickNode"
        @addNodeFinish="hideAddPanel"
    >
    </AddPanel>
    <!-- 属性面板 -->
    <el-drawer
        title="设置节点属性"
        :visible.sync="dialogVisible"
        direction="rtl"
        size="600px"
        :before-close="closeDialog">
      <PropertyDialogCircuit
          v-if="dialogVisible"
          :nodeData="clickNode"
          :lf="lf"
          @setPropertiesFinish="closeDialog"
      ></PropertyDialogCircuit>
    </el-drawer>
    <!-- 数据查看面板 -->
    <el-dialog
        title="数据"
        :visible.sync="dataVisible"
        width="50%">
      <DataDialog :graphData="graphData"></DataDialog>
    </el-dialog>
    <!--    展示实验现场，暂不展示 -->
    <ExpVideoLiving v-show="false"></ExpVideoLiving>
    <!--    <h4>更多示例：-->
    <!--      <el-button type="text" @click="goto">BpmnElement & TurboAdpter</el-button>-->
    <!--    </h4>-->
  </div>
</template>
<script>

//一般来说,仪器每次点开面板,都是加载当前的设置,而不是加载初始设置.即通过向后端发送请求,获取当前的设置,这样比较直观.但是至于连线,由于无法获得当前的连线,因此只能加载初始设置或者保存的设置.
// 但是,这样会有一个问题,这样似乎是不能分时复用的,因为加载的是现有的设置.分时复用以后再考虑吧
// 而且如果是读取当前仪器的设置会有一些麻烦,因为连线无法读取.如果用户是第一次登录的话,那么他就没有保存过的实验,因此自然就加载原始实验,但是为了防止上一个人没有初始化实验设置,因此再他加载实验之后,要进形初始化的实验设置.
// 初始化实验设置的时候要注意初始化顺序,首先要关闭电源,然后再初始化其他仪器.最后再初始化连线.因此我这里考虑只是加载这个用户之前的设定,但是这样的话,我也需要对用户的一些仪器进行设置.比如加载设定的时候,要按照顺序,先连线,然后设置那些电源和表.

import LogicFlow from '@logicflow/core'
// const LogicFlow = window.LogicFlow
import {Menu, Snapshot, MiniMap, SelectionSelect} from '@logicflow/extension'
import '@logicflow/core/dist/style/index.css'
import '@logicflow/extension/lib/style/index.css'
import NodePanel from './LFComponents/NodePanel'
import AddPanel from './LFComponents/AddPanel'
import Control from './LFComponents/Control'
import DataDialog from './LFComponents/DataDialog'
import {CircuitnodeList} from './config'

import {registerCustomNode} from "@/components/registerNode";
import PropertyDialogCircuit from "@/components/PropertySetting/PropertyDialogCircuit";
import ExpVideoLiving from "@/components/LFComponents/ExpVideoLiving";
import RemainingTime from './util_components/RemainingTime.vue';
import Logout from "@/components/util_components/Logout.vue";
// import {getEdgeValueOfConnectMatrix} from "@/components/NodeRules/noderules";

// const demoData = require('./data_circuit.json')

export default {
  name: 'LF_circuit_management',
  components: {PropertyDialogCircuit, NodePanel, AddPanel, Control, DataDialog, ExpVideoLiving,RemainingTime,Logout},
  data() {
    return {
      lf: null,
      showAddPanel: false,
      addPanelStyle: {
        top: 0,
        left: 0
      },
      nodeData: null,
      addClickNode: null,
      clickNode: null,
      dialogVisible: false,
      graphData: null,
      dataVisible: false,
      config: {
        background: {
          // 背景色
          // backgroundColor: '#f7f9ff',
        },
        grid: {
          size: 10,
          // grid不可视
          visible: false
        },

        edgeTextDraggable: true,
        hoverOutline: false,
      },
      moveData: {},
      rawData: {},
      cnodeAnchor:{},
      CircuitnodeList,
    }
  },
  mounted() {
    // 每次mounted都从服务器加载原始的实验数据
    this.$get('/api/circuit/raw/').then(res => {
      this.rawData = res.circuit_data
      this.cnodeAnchor = res.cnode_anchor
      // 存储到 sessionStorage
      sessionStorage.setItem('cnodeAnchor', JSON.stringify(this.cnodeAnchor));
      this.$_initLf() // 初始化画布
    }).catch(error =>{
      console.log(error)
    })

  //

  },
  methods: {
    // 允许删除不在rawData里的，如果在则不删除并发出错误信息
    deleteNotInRaw(lf,node) {
      if (JSON.stringify(this.rawData).includes(JSON.stringify(node)) === false) {
        lf.deleteElement(node.id)
      } else {
        // 但是因为是在管理状态，所以允许删除
        lf.deleteElement(node.id)
      }
    },

    //每次mounted或者加载实验的时候，要将一些节点和连线设置为不可连接。
    $_initLf() {
      // 画布配置
      const lf = new LogicFlow({
        // grid:true,
        ...this.config,
        plugins: [
          Menu,
          MiniMap,
          Snapshot,
          SelectionSelect
        ],
        keyboard: {
          enabled: true,
          shortcuts:[
            {
              keys:["backspace"],
              callback:()=>{
                const elements=lf.getSelectElements()
                lf.clearSelectElements()

                elements.edges.forEach((node)=> {
                  this.deleteNotInRaw(lf,node)
                })
                elements.nodes.forEach((node)=> {
                  this.deleteNotInRaw(lf,node)
                })
              }
            }
          ]
        },
        container: this.$refs.container,
      })
      this.lf = lf
      //设置自定义快捷键
      //设置右键菜单
      lf.extension.menu.setMenuConfig({
        nodeMenu: [
          {
            text: '删除',
            callback:(node)=>{
              // 如果node在
              this.deleteNotInRaw(lf,node)
              // lf.deleteNode(node.id);
            },
          },
        ], // 覆盖默认的节点右键菜单
        edgeMenu: [
          {
            text: '删除',
            callback:(node)=>{
              this.deleteNotInRaw(lf,node)
              // lf.deleteEdge(node.id)
            }
          }
        ], // 删除默认的边右键菜单
        graphMenu: [],  // 覆盖默认的边右键菜单，与false表现一样
      });


      //snapshot禁用全局css否则不能保存图片,但是仍然有问题，看不到节点
      lf.extension.snapshot.useGlobalRules = false
      //     lf.extension.snapshot.customCssRules = `
      //   .lf-node-text-auto-wrap-content{
      //     line-height: 1.2;
      //     background: transparent;
      //     text-align: center;
      //     word-break: break-all;
      //     width: 100%;
      //   }
      //   .lf-canvas-overlay {
      //     background: red;
      //   }
      // `


      //设置堆叠顺序
      lf.graphModel.overlapMode = 1
      lf.extension.selectionSelect.setSelectionSense(false, false);
      // 设置主题
      lf.setTheme({
        circle: {
          stroke: '#000000',
          strokeWidth: 1,
          outlineColor: '#88f',
        },
        rect: {
          outlineColor: '#88f',
          strokeWidth: 1
        },
        polygon: {
          strokeWidth: 1
        },
        polyline: {
          stroke: '#000000',
          hoverStroke: '#000000',
          selectedStroke: '#000000',
          outlineColor: '#88f',
          strokeWidth: 1
        },
        bezier: {
          stroke: '#000000',
          hoverStroke: '#000000',
          selectedStroke: '#000000',
          outlineColor: '#88f',
          strokeWidth: 5
        },
        nodeText: {
          color: '#000000'
        },
        edgeText: {
          color: '#000000',
          background: {
            fill: '#f7f9ff'
          }
        },
      })
      this.$_registerNode()
    },
    // 自定义
    $_registerNode() {
      registerCustomNode(this.lf)
      this.$_render()
    },
    $_render() {
      this.lf.setDefaultEdgeType('bezier')
      this.lf.render(this.rawData)
      this.$_LfEvent()
    },
    $_saveInitData() {
      console.log('saveInitData')
      const graphData = this.lf.getGraphData()
      this.$post('/api/circuit/saveinit/', {data: JSON.stringify(graphData)}).then(
          response => {
            if (response.code === 200) {
              // 重新加载页面，执行mounted等一系列操作
              this.$router.go(0)
            } else {
              console.log('服务器未能成功保存初始电路')
            }
          }
      ).catch(
          error =>{
            console.log(error)
          }
      )
    },
    $_executeConnect() {
      const graphData = this.lf.getGraphData()
      this.$post('/api/relayMatrix/', {data: JSON.stringify(graphData.edges)})
    },
    $_loadData() {
      this.$get('/api/circuit/load/').then(
          msg => {
            // console.log(msg)
            this.lf.render(msg)
          }
      ).catch(
          error =>{
            console.log(error)
          }
      )
    },
    $_saveData() {
      const data = this.lf.getGraphData()
      this.$post('/api/circuit/save/', {data: JSON.stringify(data)})
    },
    $_LfEvent() {
      this.lf.on('node:click', ({data}) => {
        console.log('node:click', data)
        this.$data.clickNode = data
        this.$data.dialogVisible = true
      })
      // 在这里可以设置边的属性，比如边的颜色之类的，点击边之后会打开类似节点属性的面板
      // this.lf.on('edge:click', ({data}) => {
      //   console.log('edge:click', data)
      //    this.$data.clickNode = data
      //     this.$data.dialogVisible = true
      // })

      //addpanel不知道是啥，现在还没搞懂
      this.lf.on('element:click', () => {
        this.hideAddPanel()
      })
      // 当边成功添加时，可以触发这一个事件，向后端发送请求
      // 由于目前不能只改变某一个继电器，因此只能先将所有数据发送到后端，后端去判断
      // this.lf.on('edge:add', ({data}) => {
      //   console.log('edge:add', data)
      //   const res = getEdgeValueOfConnectMatrix(data.sourceAnchorId, data.targetAnchorId)
      //   if (res.valid) {
      //     this.$post('/relayMatrix/', {value: res.value})
      //   } else {
      //     this.$message({message: "连线似乎有问题", type: 'error', duration: 3 * 1000})
      //   }
      // })
      this.lf.on('edge:add', ({data}) => {
        console.log('edge:add', data)
        // const graphData = this.lf.getGraphData()
        // 只传边，节省流量和带宽
        // this.$post('/relayMatrix/', {data: JSON.stringify(graphData.edges)})
      })
      this.lf.on('node:mousemove', ({data}) => {
        console.log('node:mousemove')
        this.moveData = data
      })
      this.lf.on('blank:click', () => {
        this.hideAddPanel()
      })
      this.lf.on('connection:not-allowed', (data) => {
        console.log(data)
        this.$message({
          type: 'error',
          message: data.msg
        })
      })
      this.lf.on('node:mousemove', () => {
        console.log('on mousemove')
      })
    },
    clickPlus(e, attributes) {
      e.stopPropagation()
      console.log('clickPlus', e, attributes)
      const {clientX, clientY} = e
      console.log(clientX, clientY)
      this.$data.addPanelStyle.top = (clientY - 40) + 'px'
      this.$data.addPanelStyle.left = clientX + 'px'
      this.$data.showAddPanel = true
      this.$data.addClickNode = attributes
    },
    mouseDownPlus(e, attributes) {
      e.stopPropagation()
      console.log('mouseDownPlus', e, attributes)
    },
    hideAddPanel() {
      this.$data.showAddPanel = false
      this.$data.addPanelStyle.top = 0
      this.$data.addPanelStyle.left = 0
      this.$data.addClickNode = null
    },
    closeDialog() {
      this.$data.dialogVisible = false
    },
    $_catData() {
      this.$data.graphData = this.$data.lf.getGraphData();

      this.$data.dataVisible = true;
    },
    goto() {
      this.$router.push('/TurboAdpter')
    }
  }
}
</script>
<style>
.logic-flow-view {
  height: 100vh;
  position: relative;
}

.flex-container {
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  width: 100%;
}

.centered-content {
  flex-grow: 1;
  display: flex;
  justify-content: center;
}

.demo-title {
  margin: 20px;
  /* text-align: center; 依然适用于 <h3> 元素内的文本 */
}

.demo-control {
  position: absolute;
  top: 50px;
  right: 50px;
  z-index: 2;
}

#LF-view {
  width: calc(100% - 100px);
  height: 80%;
  outline: none;
  margin-left: 50px;
}

.time-plus {
  cursor: pointer;
}

.add-panel {
  position: absolute;
  z-index: 11;
  background-color: white;
  padding: 10px 5px;
}

.el-drawer__body {
  height: 80%;
  overflow: auto;
  margin-top: -30px;
  z-index: 3;
}
</style>

