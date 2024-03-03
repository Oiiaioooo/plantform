<template>
  <div>
     <el-button-group>
      <el-button ref='select_btn' type="plain" size="small" @click="$_select" >框选</el-button>
      <el-button type="plain" size="small" @click="$_zoomIn">放大</el-button>
      <el-button type="plain" size="small" @click="$_zoomOut">缩小</el-button>
      <el-button type="plain" size="small" @click="$_zoomReset">大小适应</el-button>
      <el-button v-show="false" type="plain" size="small" @click="$_translateRest">定位还原</el-button>
      <el-button type="plain" size="small" @click="$_reset">还原(大小&定位)</el-button>
      <el-button type="plain" size="small" @click="$_undo" :disabled="undoDisable">上一步(ctrl+z)</el-button>
      <el-button type="plain" size="small" @click="$_redo" :disabled="redoDisable">下一步(ctrl+y)</el-button>
      <el-button v-show="false" type="plain" size="small" @click="$_download">下载图片</el-button>
      <el-button v-show="true" type="plain" size="small" @click="$_catData">查看数据</el-button>
       <el-button type="plain" size="small" @click="$_saveInitData">保存初始实验</el-button>
       <el-button type="plain" size="small" @click="$_saveData">保存实验</el-button>
       <el-button type="plain" size="small" @click="$_loadData">加载实验</el-button>
       <el-button type="plain" size="small" @click="$_executeConnect">执行连线</el-button>
      <el-button v-if="catTurboData" type="plain" size="small" @click="$_catTurboData">查看turbo数据</el-button>
      <el-button type="plain" size="small" @click="$_showMiniMap">查看缩略图</el-button>
    </el-button-group>
  </div>
</template>
<script>
export default {
  name: 'Control',
  props: {
    lf: Object || String,
    catTurboData: Boolean
  },
  data () {
    return {
      undoDisable: true,
      redoDisable: true,
      graphData: null,
      dataVisible: false,
      select:false
    }
  },
  mounted () {
    this.$props.lf.on('history:change', ({ data: { undoAble, redoAble } }) => {
      this.$data.undoDisable = !undoAble
      this.$data.redoDisable = !redoAble
    });
  },
  methods: {
    $_select () {
      this.select = !this.select;
      if (this.select) {
        this.$props.lf.openSelectionSelect();
        this.$refs.select_btn.$el.innerText = '取消框选';
      } else {
        this.$props.lf.closeSelectionSelect();
        this.$refs.select_btn.$el.innerText = '框选';
      }
    },
    $_zoomIn(){
      this.$props.lf.zoom(true);
    },
    $_zoomOut(){
      this.$props.lf.zoom(false);
    },
    $_zoomReset(){
      this.$props.lf.fitView()
    },
    $_translateRest(){
      this.$props.lf.resetTranslate();
    },
    $_reset(){
      this.$props.lf.resetZoom();
      this.$props.lf.resetTranslate();
    },
    $_undo(){
      this.$props.lf.undo();
    },
    $_redo(){
      this.$props.lf.redo();
    },
    $_download(){
      // console.log()
      this.$props.lf.getSnapshot()
    },
    $_saveInitData(){
      this.$emit('saveInitData')
    },
    $_executeConnect(){
      this.$emit('executeConnect')
    },
    $_catData(){
      this.$emit('catData');
    },
    $_saveData(){
      this.$emit('saveData')
    },
    $_loadData(){
      this.$emit('loadData')
    },
    $_catTurboData(){
      this.$emit('catTurboData');
    },
    $_showMiniMap() {
      const { lf } = this.$props;
      lf.extension.miniMap.show(lf.graphModel.width - 150, 40)
    }
  }
}
</script>
<style scoped>
</style>
