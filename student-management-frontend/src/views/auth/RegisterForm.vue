<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h1>创建新账号</h1>
        <p>请填写以下信息完成注册</p>
      </div>
      
      <form class="register-form" @submit.prevent="handleSubmit">
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
          <label class="form-label">邮箱</label>
          <div class="input-wrapper">
            <i class="icon">📧</i>
            <input
              v-model="email"
              type="email"
              class="form-control"
              placeholder="请输入邮箱"
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

        <div class="form-group">
          <label class="form-label">确认密码</label>
          <div class="input-wrapper">
            <i class="icon">🔒</i>
            <input
              v-model="confirmPassword"
              type="password"
              class="form-control"
              placeholder="请再次输入密码"
              required
            >
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn btn-primary btn-block" :disabled="isLoading">
            {{ isLoading ? '注册中...' : '注册' }}
          </button>
          <router-link to="/login" class="btn btn-secondary btn-block">
            返回登录
          </router-link>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>

      <div class="terms">
        注册即表示同意
        <a href="#" class="terms-link">服务条款</a>
        和
        <a href="#" class="terms-link">隐私政策</a>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import request from '@/utils/request'

export default {
  name: 'RegisterForm',
  setup() {
    const router = useRouter()
    
    const username = ref('')
    const email = ref('')
    const password = ref('')
    const confirmPassword = ref('')
    const isLoading = ref(false)
    const error = ref('')

    const isValid = computed(() => {
      if (password.value !== confirmPassword.value) {
        return false
      }
      if (password.value.length < 6) {
        return false
      }
      return true
    })

    const handleSubmit = async () => {
      if (!isValid.value) {
        error.value = '请确保两次输入的密码一致，且密码长度不少于6位'
        return
      }

      try {
        isLoading.value = true
        error.value = ''
        
        await request.post('/api/register/', {
          username: username.value,
          email: email.value,
          password: password.value
        })

        // 注册成功后跳转到登录页
        router.push('/login')
      } catch (err) {
        error.value = err.response?.data?.message || '注册失败，请稍后重试'
      } finally {
        isLoading.value = false
      }
    }

    return {
      username,
      email,
      password,
      confirmPassword,
      isLoading,
      error,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1890ff 0%, #36cfc9 100%);
  padding: 20px;
}

.register-card {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: var(--border-radius);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  padding: 2rem;
}

.register-header {
  text-align: center;
  margin-bottom: 2rem;
}

.register-header h1 {
  color: var(--heading-color);
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
}

.register-header p {
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

.form-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
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

.terms {
  text-align: center;
  margin-top: 1.5rem;
  color: var(--text-color);
  font-size: 0.875rem;
}

.terms-link {
  color: var(--primary-color);
  text-decoration: none;
}

.terms-link:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .register-card {
    padding: 1.5rem;
  }

  .register-header h1 {
    font-size: 1.5rem;
  }
}
</style> 