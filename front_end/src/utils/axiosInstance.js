import axios from 'axios';

// 创建 axios 实例
const instance = axios.create({
  baseURL: 'http://47.113.222.46:8081',
  timeout: 1000,
});

// 添加请求拦截器
instance.interceptors.request.use(
  config => {
    const token = sessionStorage.getItem('token');
    if (token) {
      config.headers.token = token; // 使用自定义头 'token'
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 添加响应拦截器
instance.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if (error.response && error.response.data.code === '-1') {
      sessionStorage.removeItem('token');
      window.location.href = '/login'; 
    }
    return Promise.reject(error);
  }
);

export default instance;
