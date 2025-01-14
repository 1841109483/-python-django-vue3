<template>
  <div class="sidebar">
    <nav class="nav-menu">
      <router-link to="/" class="nav-item" exact>
        <i class="icon">📊</i>
        <span>首页</span>
      </router-link>
      <router-link to="/students" class="nav-item">
        <i class="icon">👨‍🎓</i>
        <span>学生管理</span>
      </router-link>
      <router-link to="/courses" class="nav-item">
        <i class="icon">📚</i>
        <span>课程管理</span>
      </router-link>
      <router-link to="/scores" class="nav-item">
        <i class="icon">📝</i>
        <span>成绩管理</span>
      </router-link>
      <router-link to="/classes" class="nav-item">
        <i class="icon">👥</i>
        <span>班级管理</span>
      </router-link>
      <router-link to="/users" class="nav-item" active-class="active">
        <i class="icon">👥</i>
        <span>用户管理</span>
      </router-link>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'AppSidebar'
}
</script>

<style scoped>
.sidebar {
  width: 200px;
  background: white;
  border-right: 1px solid #f0f0f0;
  height: calc(100vh - 64px);
}

.nav-menu {
  padding: 16px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 24px;
  color: #333;
  text-decoration: none;
  transition: all 0.3s;
  gap: 12px;
}

.nav-item:hover {
  background: #f5f5f5;
}

.nav-item.router-link-active {
  background: #e6f7ff;
  color: #1890ff;
  border-right: 3px solid #1890ff;
}

.icon {
  font-size: 18px;
}
</style> 