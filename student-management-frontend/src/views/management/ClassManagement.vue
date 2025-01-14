<template>
  <div class="management-page">
    <div class="page-header">
      <h2>班级管理</h2>
      <button class="add-btn" @click="showAddDialog = true">
        <i class="icon">➕</i> 添加班级
      </button>
    </div>

    <div class="search-bar">
      <input type="text" v-model="searchQuery" placeholder="搜索班级...">
    </div>

    <table class="table">
      <thead>
        <tr>
          <th>班级编号</th>
          <th>班级名称</th>
          <th>班主任</th>
          <th>学生人数</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="cls in filteredClasses" :key="cls.id">
          <td>{{ cls.class_id }}</td>
          <td>{{ cls.name }}</td>
          <td>{{ cls.teacher }}</td>
          <td>{{ cls.student_count }}</td>
          <td>
            <button class="edit-btn" @click="editClass(cls)">编辑</button>
            <button class="delete-btn" @click="deleteClass(cls.id)">删除</button>
          </td>
        </tr>
        <tr v-if="filteredClasses.length === 0">
          <td colspan="5" class="empty-text">暂无数据</td>
        </tr>
      </tbody>
    </table>

    <!-- 添加/编辑对话框 -->
    <div v-if="showAddDialog" class="dialog-overlay">
      <div class="dialog">
        <h3>{{ isEditing ? '编辑班级' : '添加班级' }}</h3>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>班级编号</label>
            <input 
              type="text" 
              v-model="form.class_id" 
              required
              :disabled="isEditing"
            >
          </div>
          <div class="form-group">
            <label>班级名称</label>
            <input 
              type="text" 
              v-model="form.name" 
              required
            >
          </div>
          <div class="form-group">
            <label>班主任</label>
            <input 
              type="text" 
              v-model="form.teacher" 
              required
            >
          </div>
          <div class="dialog-buttons">
            <button type="submit" class="btn-primary">保存</button>
            <button type="button" class="btn-secondary" @click="closeDialog">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import request from '@/utils/request'

export default {
  name: 'ClassManagement',
  setup() {
    const classes = ref([])
    const searchQuery = ref('')
    const showAddDialog = ref(false)
    const isEditing = ref(false)
    const currentId = ref(null)
    const form = reactive({
      class_id: '',
      name: '',
      teacher: ''
    })

    const fetchClasses = async () => {
      try {
        const response = await request.get('/api/classes/')
        classes.value = response.data
      } catch (error) {
        console.error('获取班级列表失败:', error)
      }
    }

    const filteredClasses = computed(() => {
      const query = searchQuery.value.toLowerCase()
      return classes.value.filter(cls => 
        cls.name.toLowerCase().includes(query) ||
        cls.class_id.toLowerCase().includes(query) ||
        cls.teacher.toLowerCase().includes(query)
      )
    })

    const handleSubmit = async () => {
      try {
        if (isEditing.value) {
          await request.put(`/api/classes/${currentId.value}/`, form)
        } else {
          await request.post('/api/classes/', form)
        }
        await fetchClasses()
        closeDialog()
      } catch (error) {
        alert(error.response?.data?.message || '操作失败')
      }
    }

    const closeDialog = () => {
      showAddDialog.value = false
      isEditing.value = false
      Object.assign(form, {
        class_id: '',
        name: '',
        teacher: ''
      })
    }

    const editClass = (cls) => {
      isEditing.value = true
      currentId.value = cls.id
      Object.assign(form, cls)
      showAddDialog.value = true
    }

    const deleteClass = async (id) => {
      if (confirm('确定要删除这个班级吗？')) {
        try {
          await request.delete(`/api/classes/${id}/`)
          await fetchClasses()
        } catch (error) {
          alert(error.response?.data?.message || '删除失败')
        }
      }
    }

    onMounted(fetchClasses)

    return {
      classes,
      searchQuery,
      showAddDialog,
      isEditing,
      form,
      filteredClasses,
      handleSubmit,
      editClass,
      deleteClass,
      closeDialog
    }
  }
}
</script>

<style scoped>
.management-page {
  padding: 2rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.search-bar {
  margin-bottom: 1rem;
}

.search-bar input {
  width: 300px;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.add-btn {
  padding: 0.5rem 1rem;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.edit-btn,
.delete-btn {
  padding: 0.3rem 0.8rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin: 0 0.2rem;
}

.edit-btn {
  background: #1890ff;
  color: white;
}

.delete-btn {
  background: #ff4d4f;
  color: white;
}

.empty-text {
  text-align: center;
  color: #999;
  padding: 2rem;
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

.dialog {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
}

.dialog h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
}

.dialog-buttons {
  margin-top: 2rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
</style> 