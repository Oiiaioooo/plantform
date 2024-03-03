import Vue from 'vue'
import Router from 'vue-router'
// import {Message} from "element-ui";
// import HelloWorld from '@/components/HelloWorld'
import LF_circuit from '@/components/LF_Circuit'
import LF_circuit_management from '@/components/LF_Circuit_management'
import LF from '@/components/LF'
import TurboAdpter from '@/components/TurboAdpter'
import Test from '@/components/Test'
import test_view from "@/components/test_view"
import ShowJSON from "@/components/ShowJSON";
import test_websocket from '@/components/test_websocket'
import OscilloscopeCurve from '@/components/PropertySetting/OscilloscopeCurve'
import Login from '@/components/Login'
import Dashboard from '@/components/Dashboard'

Vue.use(Router)

const router = new Router({
    routes: [
        {
            path: '/',
            name: 'login',
            meta:{
                title:"登录"
            } ,
            component: Login
        },
        {
            path: '/exp',
            name: 'circuit',
            meta:{
               title:"远程实验平台"
            } ,
            component: LF_circuit
        },
        {
            path: '/exp_management',
            name: 'circuit_management',
            meta:{
                title:"远程设置管理"
            } ,
            component: LF_circuit_management
        },
        {
            path: '/dashboard',
            name: 'Dashboard',
            component: Dashboard,
            meta: {
                title: "仪表盘"
            }
        },
        {
            path: '/lf',
            name: 'LF',
            component: LF
        },
        {
            path: '/test',
            name: 'Test',
            component: Test
        },
        {
            path: '/test_view',
            name: 'test_view',
            component: test_view
        },
        {
            path:'/showjson',
            name:'showjson',
            component:ShowJSON
        },
        {
            path:'/test_websocket',
            name:'test_websocket',
            component:test_websocket
        },
        {
            path: '/TurboAdpter',
            name: 'TurboAdpter',
            component: TurboAdpter
        },
        {
            path: '/OscilloscopeCurve',
            name: 'OscilloscopeCurve',
            component: OscilloscopeCurve
        }


    ]
})

/**
 * 路由拦截
 * 权限验证
 */
router.beforeEach((to, from, next) => {
    const isLoggedIn = Boolean(sessionStorage.getItem('token')); // 或 localStorage
    const user = JSON.parse(sessionStorage.getItem('user')); // 或 localStorage
    const isAdmin = user && user.role === 'admin'; // 判断用户是否是管理员

    const protectedPaths = ['/exp', '/exp_management','/dashboard']; // 受保护的路由
    const adminPaths = ['/exp_management']; // 只有管理员可以访问的路由

    if (protectedPaths.includes(to.path) && !isLoggedIn) {
        next({ path: '/', query: { redirect: to.fullPath } });
    } else if (adminPaths.includes(to.path) && !isAdmin) {
        next({ path: '/dashboard' }); // 如果用户不是管理员，重定向到仪表盘
    } else {
        next();
    }
});

export default router
