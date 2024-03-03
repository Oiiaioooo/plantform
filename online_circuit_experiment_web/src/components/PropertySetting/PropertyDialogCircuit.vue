<template>
  <div class="property-dialog">
    <User
      v-if="nodeData.type === 'user'"
      :nodeData="nodeData"
      :lf="lf"
      @onClose="handleClose"/>
    <ResistanceBox v-else-if="nodeData.type==='resistance_box'" :nodeData="nodeData" :lf="lf" @onClose="handleClose"/>
    <CapacitanceBox v-else-if="nodeData.type==='capacitance_box'" :nodeData="nodeData" :lf="lf" @onClose="handleClose"/>
    <DCPowerSupply v-else-if="nodeData.type==='dc_power_supply_real'" :nodeData="nodeData" :lf="lf" @onClose="handleClose"/>
    <Multimeter v-else-if="nodeData.type==='multimeter_real'" :node-data="nodeData" :lf="lf" @onClose="handleClose"/>
    <Oscilloscope v-else-if="nodeData.type==='oscilloscope_real'" :node-data="nodeData" :lf="lf" @onClose="handleClose"/>
    <SignalGenerator v-else-if="nodeData.type==='signal_generator'" :node-data="nodeData" :lf="lf" @onClose="handleClose"/>
    <DM8720 v-else-if="nodeData.type==='DM8720'" :node-data="nodeData" :lf="lf" @onClose="handleClose"/>
    <CommonProperty
      v-else
      :nodeData="nodeData"
      :lf="lf"
      @onClose="handleClose"/>
    <SetAnchorCNodeNumber v-if="user.role === 'admin'" :node-data="nodeData" :lf="lf"></SetAnchorCNodeNumber>
  </div>
</template>
<script>
import SetAnchorCNodeNumber from "@/components/LFComponents/SetAnchorCNodeNumber";
import CommonProperty from './CommonProperty'
import ResistanceBox from "@/components/PropertySetting/ResistanceBox";
import CapacitanceBox from "@/components/PropertySetting/CapacitanceBox";
import DCPowerSupply from "@/components/PropertySetting/DCPowerSupply";
import Multimeter from "@/components/PropertySetting/Multimeter";
import Oscilloscope from "@/components/PropertySetting/Oscilloscope";
import SignalGenerator from "@/components/PropertySetting/SignalGenerator";
import DM8720 from "@/components/PropertySetting/DM8720.vue";
export default {
  name: 'PropertyDialogCircuit',
  components: {
    SetAnchorCNodeNumber,
    DCPowerSupply,
    ResistanceBox,
    CommonProperty,
    CapacitanceBox,
    Multimeter,
    Oscilloscope,
    SignalGenerator,
    DM8720,
  },
  props: {
    nodeData: Object,
    lf: Object
  },
  mounted() {
    const storedUser = sessionStorage.getItem('user');
    if (storedUser) {
      this.user = JSON.parse(storedUser);
      console.log('PropertyDialog', this.user.role);
    }
  },

  data () {
    return {
      user: {
        role: '' // 默认值为空字符串
      }
    }
  },
  methods: {
    handleClose () {
      this.$emit('setPropertiesFinish')//trigger the function "setPropertiesFinish" of father component
    }
  }
}
</script>
<style>
.property-dialog{
  padding: 20px;
}
</style>
