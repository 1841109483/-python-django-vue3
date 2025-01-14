<template>
  <div class="user-management">
    <div class="page-header">
      <h2>用户管理</h2>
      <button class="btn btn-primary" @click="showAddDialog">
        <i class="icon">➕</i> 添加用户
      </button>
    </div>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <div class="input-wrapper">
        <i class="icon">🔍</i>
        <input
          v-model="searchQuery"
          type="text"
          class="form-control"
          placeholder="搜索用户名或邮箱"
          @input="handleSearch"
        >
      </div>
    </div>

    <!-- 用户列表 -->
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>邮箱</th>
            <th>角色</th>
            <th>状态</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
            <td>
              <span :class="['status-badge', user.is_active ? 'active' : 'inactive']">
                {{ user.is_active ? '启用' : '禁用' }}
              </span>
            </td>
            <td>{{ formatDate(user.created_at) }}</td>
            <td>
              <div class="action-buttons">
                <button class="btn btn-small btn-primary" @click="showEditDialog(user)">
                  编辑
                </button>
                <button 
                  class="btn btn-small" 
                  :class="user.is_active ? 'btn-warning' : 'btn-success'"
                  @click="toggleUserStatus(user)"
                >
                  {{ user.is_active ? '禁用' : '启用' }}
                </button>
                <button class="btn btn-small btn-error" @click="confirmDelete(user)">
                  删除
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="totalPages > 1">
      <button 
        class="btn btn-outline" 
        :disabled="currentPage === 1"
        @click="changePage(currentPage - 1)"
      >
        上一页
      </button>
      <span class="page-info">
        第 {{ currentPage }} 页，共 {{ totalPages }} 页
      </span>
      <button 
        class="btn btn-outline"
        :disabled="currentPage === totalPages"
        @click="changePage(currentPage + 1)"
      >
        下一页
      </button>
    </div>

    <!-- 添加/编辑用户对话框 -->
    <div v-if="showDialog" class="dialog-overlay" @click="closeDialog">
      <div class="dialog-content" @click.stop>
        <h3>{{ isEditing ? '编辑用户' : '添加用户' }}</h3>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label class="form-label">用户名</label>
            <input
              v-model="formData.username"
              type="text"
              class="form-control"
              required
            >
          </div>
          <div class="form-group">
            <label class="form-label">邮箱</label>
            <input
              v-model="formData.email"
              type="email"
              class="form-control"
              required
            >
          </div>
          <div class="form-group">
            <label class="form-label">密码</label>
            <input
              v-model="formData.password"
              type="password"
              class="form-control"
              :required="!isEditing"
              :placeholder="isEditing ? '不修改请留空' : '请输入密码'"
            >
          </div>
          <div class="form-group">
            <label class="form-label">角色</label>
            <select v-model="formData.role" class="form-control">
              <option value="admin">管理员</option>
              <option value="teacher">教师</option>
              <option value="student">学生</option>
            </select>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn btn-primary">确定</button>
            <button type="button" class="btn btn-secondary" @click="closeDialog">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import request from '@/utils/request'

export default {
  name: 'UserManagement',
  setup() {
    const users = ref([])
    const currentPage = ref(1)
    const totalUsers = ref(0)
    const pageSize = 10
    const searchQuery = ref('')
    const showDialog = ref(false)
    const isEditing = ref(false)
    const formData = ref({
      username: '',
      email: '',
      password: '',
      role: 'student',
      is_active: true
    })
    const editingUserId = ref(null)

    const totalPages = computed(() => Math.ceil(totalUsers.value / pageSize))

    // 获取用户列表
    const fetchUsers = async (page = 1, search = '') => {
      try {
        const response = await request.get('/api/users/', {
          params: { 
            page,
            search,
            page_size: pageSize
          }
        })
        users.value = response.data.results
        totalUsers.value = response.data.count
      } catch (error) {
        console.error('获取用户列表失败:', error)
      }
    }

    // 搜索处理
    const handleSearch = () => {
      currentPage.value = 1
      fetchUsers(1, searchQuery.value)
    }

    // 切换页面
    const changePage = (page) => {
      currentPage.value = page
      fetchUsers(page, searchQuery.value)
    }

    // 显示添加对话框
    const showAddDialog = () => {
      isEditing.value = false
      formData.value = {
        username: '',
        email: '',
        password: '',
        role: 'student'
      }
      showDialog.value = true
    }

    // 显示编辑对话框
    const showEditDialog = (user) => {
      isEditing.value = true
      editingUserId.value = user.id
      formData.value = {
        username: user.username,
        email: user.email,
        password: '',
        role: user.role
      }
      showDialog.value = true
    }

    // 关闭对话框
    const closeDialog = () => {
      showDialog.value = false
      formData.value = {
        username: '',
        email: '',
        password: '',
        role: 'student'
      }
    }

    // 提交表单
    const handleSubmit = async () => {
      try {
        if (isEditing.value) {
          await request.put(`/api/users/${editingUserId.value}/`, formData.value)
        } else {
          await request.post('/api/users/', formData.value)
        }
        closeDialog()
        fetchUsers(currentPage.value, searchQuery.value)
      } catch (error) {
        console.error('保存用户失败:', error)
      }
    }

    // 切换用户状态
    const toggleUserStatus = async (user) => {
      try {
        await request.patch(`/api/users/${user.id}/`, {
          is_active: !user.is_active
        })
        fetchUsers(currentPage.value, searchQuery.value)
      } catch (error) {
        console.error('切换用户状态失败:', error)
      }
    }

    // 删除用户
    const confirmDelete = async (user) => {
      if (confirm(`确定要删除用户 "${user.username}" 吗？`)) {
        try {
          await request.delete(`/api/users/${user.id}/`)
          fetchUsers(currentPage.value, searchQuery.value)
        } catch (error) {
          console.error('删除用户失败:', error)
        }
      }
    }

    // 格式化日期
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    onMounted(() => {
      fetchUsers()
    })

    return {
      users,
      currentPage,
      totalUsers,
      totalPages,
      searchQuery,
      showDialog,
      isEditing,
      formData,
      handleSearch,
      changePage,
      showAddDialog,
      showEditDialog,
      closeDialog,
      handleSubmit,
      toggleUserStatus,
      confirmDelete,
      formatDate
    }
  }
}
</script>

<style scoped>
.user-management {
  padding: 2rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-header h2 {
  margin: 0;
  color: var(--heading-color);
}

.search-bar {
  margin-bottom: 1.5rem;
}

.search-bar .input-wrapper {
  max-width: 300px;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.875rem;
}

.status-badge.active {
  background: #f6ffed;
  color: var(--success-color);
  border: 1px solid #b7eb8f;
}

.status-badge.inactive {
  background: #fff2f0;
  color: var(--error-color);
  border: 1px solid #ffccc7;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn-small {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.page-info {
  color: var(--text-color);
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog-content {
  background: white;
  padding: 2rem;
  border-radius: var(--border-radius);
  width: 100%;
  max-width: 500px;
}

.dialog-content h3 {
  margin: 0 0 1.5rem 0;
  color: var(--heading-color);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-outline {
  border: 1px solid var(--border-color);
  background: transparent;
  color: var(--text-color);
  padding: 0.5rem 1rem;
  border-radius: var(--border-radius);
  cursor: pointer;
}

.btn-outline:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-outline:not(:disabled):hover {
  background: var(--hover-color);
}

@media (max-width: 768px) {
  .user-management {
    padding: 1rem;
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn-small {
    width: 100%;
  }
}
</style> 