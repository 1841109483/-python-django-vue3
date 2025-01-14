<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1>学生管理系统</h1>
        <p>请登录您的账号</p>
      </div>
      
      <form class="login-form" @submit.prevent="handleSubmit">
        <div class="form-group">
          <label class="form-label">用户名</label>
          <div class="input-wrapper">
            <i class="icon">👤</i>
            <input
              v-model="username"
              type="text"
              class="form-control"
              placeholder="请输入用户名"
              required
            >
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">密码</label>
          <div class="input-wrapper">
            <i class="icon">🔒</i>
            <input
              v-model="password"
              type="password"
              class="form-control"
              placeholder="请输入密码"
              required
            >
          </div>
        </div>

        <div class="form-options">
          <label class="checkbox-wrapper">
            <input type="checkbox" v-model="rememberMe">
            <span>记住我</span>
          </label>
          <router-link to="/forgot-password" class="forgot-link">忘记密码？</router-link>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn btn-primary btn-block" :disabled="isLoading">
            {{ isLoading ? '登录中...' : '登录' }}
          </button>
          <router-link to="/register" class="btn btn-secondary btn-block">
            注册账号
          </router-link>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import request from '@/utils/request'

export default {
  name: 'LoginForm',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const username = ref('')
    const password = ref('')
    const rememberMe = ref(false)
    const isLoading = ref(false)
    const error = ref('')

    const handleSubmit = async () => {
      try {
        isLoading.value = true
        error.value = ''
        
        const response = await request.post('/api/login/', {
          username: username.value,
          password: password.value
        })

        console.log('Login response:', response.data)

        const { token, user } = response.data
        
        // 存储登录状态
        store.dispatch('login', { token, user })
        
        if (rememberMe.value) {
          localStorage.setItem('rememberMe', 'true')
        }

        router.push('/')
      } catch (err) {
        console.error('Login error:', err)
        error.value = err.response?.data?.error || '登录失败，请检查用户名和密码'
      } finally {
        isLoading.value = false
      }
    }

    return {
      username,
      password,
      rememberMe,
      isLoading,
      error,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1890ff 0%, #36cfc9 100%);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: var(--border-radius);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  padding: 2rem;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h1 {
  color: var(--heading-color);
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
}

.login-header p {
  color: var(--text-color);
  font-size: 0.875rem;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.icon {
  position: absolute;
  left: 12px;
  color: var(--text-color);
  font-size: 1.25rem;
}

.form-control {
  padding-left: 40px;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  color: var(--text-color);
  font-size: 0.875rem;
}

.forgot-link {
  color: var(--primary-color);
  text-decoration: none;
  font-size: 0.875rem;
}

.forgot-link:hover {
  text-decoration: underline;
}

.form-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn-block {
  width: 100%;
  padding: 0.75rem;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #fff2f0;
  border: 1px solid #ffccc7;
  border-radius: 4px;
  color: var(--error-color);
  font-size: 0.875rem;
  text-align: center;
}

@media (max-width: 480px) {
  .login-card {
    padding: 1.5rem;
  }

  .login-header h1 {
    font-size: 1.5rem;
  }
}
</style> 