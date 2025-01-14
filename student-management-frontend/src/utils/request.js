import axios from 'axios'
import store from '@/store'
import router from '@/router'

const request = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000',
  timeout: 5000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = store.state.token
    if (token) {
      config.headers.Authorization = token
    }
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response
  },
  error => {
    console.error('Response error:', error)
    
    if (error.response?.status === 401) {
      // 只有在非登录页面时才清除认证并跳转
      const currentPath = router.currentRoute.value.path
      if (currentPath !== '/login' && currentPath !== '/register') {
        store.dispatch('logout')
        router.push('/login')
      }
    }
    return Promise.reject(error)
  }
)

export default request 