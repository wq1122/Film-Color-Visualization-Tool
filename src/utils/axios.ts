import axios from 'axios';
import { ElMessage, ElLoading } from 'element-plus'

let loading:any = null
const loadingConfig = { // ElLoading 的加载动画
    lock: true,
    text: 'Loading',
    background: 'rgba(0, 0, 0, 0.7)'
}

const loadingWhiteList = ['/getColorDominant'] // 请求白名单
const axiosInstance = axios.create({
    baseURL: '/api',
    timeout: 500000000,
});

// 添加请求拦截器
axiosInstance.interceptors.request.use(
    (config) => {
        // 在发送请求之前做些什么
        if (!loadingWhiteList.includes(config?.url ?? '')) {
            loading = ElLoading.service(loadingConfig)
        }
        return config;
    },
    (error: any) => {
        // 处理请求错误
        loading.close()
        return Promise.reject(error);
    },
);

// 添加响应拦截器
axiosInstance.interceptors.response.use(
    (response) => {
        // 对响应数据做点什么
        if(loading){
            loading.close()
        }
        return response;
    },
    (error: any) => {
        // 处理响应错误
        ElMessage({
            message: "请求失败，请稍后再试",
            type: 'warning'
        })
        return Promise.reject(error);
    },
);

export default axiosInstance;

