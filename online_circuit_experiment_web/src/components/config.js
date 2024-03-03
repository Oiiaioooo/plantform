export const CircuitnodeList=[
  {
    type:'resistance_box',
    text:'电阻箱',
    class:'resistance_box',
  },
  {
    type:'capacitance_box',
    text: '电容箱',
    class:'capacitance_box',
  },
  {
    type:'inductance_box',
    text: '电感箱',
    class:'inductance_box'
  },
  {
    type:'dc_power_supply_real',
    text: '直流源',
    class:'dc_power_supply_real'
  },
  {
    type: 'multimeter_real',
    text: '数字万用表',
    class:'multimeter_real'
  },
  {
    type:'DM8720',
    text:'DM8720',
    class:'DM8720'
  },
  {
    type:'signal_generator',
    text:'信号发生器',
    class:'signal_generator'
  },
  {
    type:'oscilloscope_real',
    text:'示波器',
    class:'oscilloscope_real'
  },
  {
    type:'resistance_real',
    text:'电阻',
    class:'resistance_real'
  },
  {
    type:'capacitance_real',
    text:'电容',
    class:'capacitance_real'
  },
  {
    type:'inductance_real',
    text:'电感',
    class:'inductance_real'
  },
  {
    type:'MOSFET_real',
    text:'MOSFET',
    class:'MOSFET_real'
  },
  {
    type:'diode_real',
    text:'二极管',
    class:'diode_real'
  },
  {
    type:'GND',
    text:'接地',
    class:'GND'
  }
]

export const nodeList = [
  {
    text: '开始',
    type: 'start',
    class: 'node-start'
  },
  {
    text: '矩形',
    type: 'rect',
    class: 'node-rect'
  },
  {
    type: 'user',
    text: '用户',
    class: 'node-user'
  },
  {
    type: 'push',
    text: '推送',
    class: 'node-push'
  },
  {
    type: 'download',
    text: '位置',
    class: 'node-download'
  },
  {
    type: 'connect',
    text: 'Html',
    class: 'node-push'
  },
  {
    type: 'end',
    text: '结束',
    class: 'node-end'
  },

];

export const BpmnNode = [
  {
    type: 'bpmn:startEvent',
    text: '开始',
    class: 'bpmn-start'
  },
  {
    type: 'bpmn:endEvent',
    text: '结束',
    class: 'bpmn-end'
  },
  {
    type: 'bpmn:exclusiveGateway',
    text: '网关',
    class: 'bpmn-exclusiveGateway'
  },
  {
    type: 'bpmn:userTask',
    text: '用户',
    class: 'bpmn-user'
  },
]
