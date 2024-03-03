import Vue from 'vue'
import App from './App.vue'
import router from './router'
import RoundSlider from "vue-round-slider";
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import {$get,$post} from "@/Util/request/http"
import * as echarts from 'echarts'

Vue.use(ElementUI)
Vue.component('round-slider', RoundSlider)
Vue.config.productionTip = false
// 设置vue的全局变量或方法
Vue.prototype.$get = $get
Vue.prototype.$post = $post
Vue.prototype.$echarts = echarts
router.beforeEach((to, from, next) => {
  /* 路由发生变化修改页面title */
  if (to.meta.title) {
    document.title = to.meta.title
  }
  next()
})
new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
