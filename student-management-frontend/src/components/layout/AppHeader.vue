<template>
  <header class="header">
    <div class="logo">
      学生管理系统
    </div>
    <div class="user-info">
      <span class="username">{{ username }}</span>
      <button class="logout-btn" @click="handleLogout">退出</button>
    </div>
  </header>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'AppHeader',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const username = computed(() => store.state.user?.username || 'Admin')

    const handleLogout = () => {
      store.dispatch('logout')
      router.push('/login')
    }

    return {
      username,
      handleLogout
    }
  }
}
</script>

<style scoped>
.header {
  height: 64px;
  background: #001529;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: white;
}

.logo {
  font-size: 20px;
  font-weight: bold;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.username {
  font-size: 14px;
}

.logout-btn {
  padding: 4px 12px;
  border: 1px solid white;
  background: transparent;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.logout-btn:hover {
  background: rgba(255,255,255,0.1);
}
</style> 