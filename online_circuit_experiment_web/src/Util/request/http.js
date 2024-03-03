/**axios封装
 * 请求拦截、相应拦截、错误统一处理
 */
import axios from 'axios';
import {Message} from "element-ui";
// import QS from 'qs';

//qs.stringify()是将对象 序列化成URL的形式，以&进行拼接
//  let protocol = window.location.protocol; //协议
//  let host = window.location.host; //主机
//  axios.defaults.baseURL = protocol + "//" + host;
// 外网设置
//  axios.defaults.baseURL = 'http://166.111.194.32:8000/api/'
// axios.defaults.baseURL = 'http://183.173.105.207:8000/api/'
// 本地设置
axios.defaults.baseURL = 'http://127.0.0.1:8001/'
// const token = sessionStorage.getItem('token');
// axios.defaults.headers = {'Content-Type': 'application/json','Authorization': `Bearer ${token}`}
// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
axios.interceptors.request.use( //响应拦截
    async config => {
        // 每次发送请求之前判断vuex中是否存在token
        // 如果存在，则统一在http请求的header都加上token，这样后台根据token判断你的登录情况
        // 即使本地存在token，也有可能token是过期的，所以在响应拦截器中要对返回状态进行判断
        const token = sessionStorage.getItem('token');
        config.headers.Authorization = `Bearer ${token}`
        return config;
    },
    error => {
        return Promise.error(error);
    })
// 响应拦截器
// 这里要做一件事情，如果后端返回的status有错误，则要反映出来，使用el-message,如果后端的error中没有定义message，则使用默认的message，否则使用后端定义的message。
// 这便是拦截器的作用，之后所有的信息只要写在后端就行了，省的前端也写来写去重复代码。
axios.interceptors.response.use(
    // response:{data,status,statusText,header,config}，根据官网文档：
    // Any status code that lie within the range of 2xx cause this function to trigger
    // Do something with response data
    // 当然，也可以在response.data里面加入code，这可以与后端进行约定
    response => {
        // console.log("response",response)
        // 这里将不是200的都视为失败了
        // 如果status是200，但是服务器response.data.code又返回了code404，说明响应成功了，但是找不到数据，与后端定义了404是找不到数据，这是自定义的
        if (response.status === 200) {
            Message({
                message:response.data.message===undefined?"响应成功":response.data.message,
                type:'success',
                duration:1*1000
            })
            return Promise.resolve(response); //进行中
        } else {
            // 这里如果reject了，则不会跳到下面的error，而是被catch抓到
            return Promise.reject(response); //失败
        }
    },
    // 服务器状态码不是200的情况
    // 受到服务器返回的error后，要
    // AxiosError{
    //  message,name,code:"ERR_BAD_REQUEST",config,request,
    // response{data:(来自服务器返回的),config,status:状态码，statusText,headers,request,}
    // }
    error => {
        // console.log("error",error)
        if (error.response.status) {
            switch (error.response.status) {
                // 401: 未登录
                // 未登录则跳转登录页面，并携带当前页面的路径
                // 在登录成功后返回当前页面，这一步需要在登录页操作。

                // 在这里，可以对error.message根据status进行自定义更改，不使用默认值。
                case 401:
                    error.message = '未认证，请登录'
                    break
                // 403 token过期
                // 登录过期对用户进行提示
                // 清除本地token和清空vuex中token对象
                // 跳转登录页面
                case 403:
                    error.message = '拒绝访问'
                    sessionStorage.clear()
                    break
                // 404请求不存在
                case 404:
                    error.message = `请求地址出错: ${error.response.config.url}`
                    break;
                // 其他错误，直接抛出错误提示
                case 408:
                    error.message = '请求超时'
                    break
                case 500:
                    error.message = '服务器内部错误'
                    break
                case 501:
                    error.message = '服务未实现'
                    break
                case 502:
                    error.message = '网关错误'
                    break
                case 503:
                    error.message = '服务不可用'
                    break
                case 504:
                    error.message = '网关超时'
                    break
                case 505:
                    error.message = 'HTTP版本不受支持'
                    break
                default:
                    break
            }
            Message({
                message: error.response.data.message===undefined?error.message:error.response.data.message,
                type:'error',
                duration:5*1000
            })
            return Promise.reject(error);
        }
    }
);
/**
 * get方法，对应get请求
 * @param {String} url [请求的url地址]
 * @param {Object} params [请求时携带的参数]
 * @param customHeaders
 */
const $get = (url, params) => {
    return new Promise((resolve, reject) => {
        // 创建一个配置对象，包括传递的参数和自定义的请求头
        const config = {
            params: params,
        };
        // console.log("config",config)
        axios.get(url, config)
            .then(res => {
                resolve(res.data);
            })
            .catch(err => {
                reject(err);
            });
    });
}
/**
 * post方法，对应post请求
 * @param {String} url [请求的url地址]
 * @param {Object} params [请求时携带的参数]
 */
const $post = (url, params) => {
    return new Promise((resolve, reject) => {

        axios.post(url, params
            ) //是将对象 序列化成URL的形式，以&进行拼接
            .then(res => {
                resolve(res.data);
            })
            .catch(err => {
                reject(err)
            })
    });
}
//下面是vue3必须加的，vue2不需要，只需要暴露出去get，post方法就可以
export {
    $get,
    $post
}
// export default{
//     install:(app) => {
//         app.config.globalProperties['$get'] = $get;
//         app.config.globalProperties['$post'] = $post;
//         app.config.globalProperties['$axios'] = axios;
//     }
// }
