<template>
  <div>
    <vue-json-pretty :path="'res'" :data="JSONdata"> </vue-json-pretty>
  </div>
</template>
<script>
import VueJsonPretty from 'vue-json-pretty';
import 'vue-json-pretty/lib/styles.css';

export default {
  name:'ShowJSON',
  data(){
    return {
      JSONdata: {
        id:'10e52e55-32cb-4117-b56b-2882ca1a27a4',
        type:'multimeter_real',
        properties:{
          value:'2.19870',
          type:'voltage',
          unit:'V',
        }
      },
    }
  },
  components: {
    VueJsonPretty,
  },
};
</script>
<style scoped>
</style>


