<template>
  <div class="forgot-container">
    <div class="forgot-card">
      <div class="forgot-header">
        <h1>找回密码</h1>
        <p>请输入您的邮箱，我们将发送重置密码链接</p>
      </div>
      
      <form class="forgot-form" @submit.prevent="handleSubmit">
        <div class="form-group">
          <label class="form-label">邮箱地址</label>
          <div class="input-wrapper">
            <i class="icon">📧</i>
            <input
              v-model="email"
              type="email"
              class="form-control"
              placeholder="请输入注册时的邮箱"
              required
            >
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn btn-primary btn-block" :disabled="isLoading">
            {{ isLoading ? '发送中...' : '发送重置链接' }}
          </button>
          <router-link to="/login" class="btn btn-secondary btn-block">
            返回登录
          </router-link>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div v-if="success" class="success-message">
          {{ success }}
        </div>
      </form>

      <div class="help-text">
        没有收到邮件？请检查垃圾邮件文件夹，或
        <a href="#" @click.prevent="handleResend" class="resend-link">重新发送</a>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import request from '@/utils/request'

export default {
  name: 'ForgotPassword',
  setup() {
    const email = ref('')
    const isLoading = ref(false)
    const error = ref('')
    const success = ref('')

    const handleSubmit = async () => {
      try {
        isLoading.value = true
        error.value = ''
        success.value = ''
        
        await request.post('/api/password/reset/', {
          email: email.value
        })

        success.value = '重置密码链接已发送到您的邮箱，请查收'
      } catch (err) {
        error.value = err.response?.data?.message || '发送失败，请稍后重试'
      } finally {
        isLoading.value = false
      }
    }

    const handleResend = () => {
      if (email.value) {
        handleSubmit()
      } else {
        error.value = '请先输入邮箱地址'
      }
    }

    return {
      email,
      isLoading,
      error,
      success,
      handleSubmit,
      handleResend
    }
  }
}
</script>

<style scoped>
.forgot-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1890ff 0%, #36cfc9 100%);
  padding: 20px;
}

.forgot-card {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: var(--border-radius);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  padding: 2rem;
}

.forgot-header {
  text-align: center;
  margin-bottom: 2rem;
}

.forgot-header h1 {
  color: var(--heading-color);
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
}

.forgot-header p {
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

.success-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #f6ffed;
  border: 1px solid #b7eb8f;
  border-radius: 4px;
  color: var(--success-color);
  font-size: 0.875rem;
  text-align: center;
}

.help-text {
  text-align: center;
  margin-top: 1.5rem;
  color: var(--text-color);
  font-size: 0.875rem;
}

.resend-link {
  color: var(--primary-color);
  text-decoration: none;
  cursor: pointer;
}

.resend-link:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .forgot-card {
    padding: 1.5rem;
  }

  .forgot-header h1 {
    font-size: 1.5rem;
  }
}
</style> 