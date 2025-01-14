<template>
  <div class="management-page">
    <div class="page-header">
      <h2>学生管理</h2>
      <button class="add-btn" @click="showAddDialog = true">
        <i class="icon">➕</i> 添加学生
      </button>
    </div>

    <div class="search-bar">
      <input type="text" v-model="searchQuery" placeholder="搜索学生...">
    </div>

    <table class="table">
      <thead>
        <tr>
          <th>学号</th>
          <th>姓名</th>
          <th>性别</th>
          <th>年龄</th>
          <th>班级</th>
          <th>联系电话</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="student in filteredStudents" :key="student.id">
          <td>{{ student.student_id }}</td>
          <td>{{ student.name }}</td>
          <td>{{ student.gender }}</td>
          <td>{{ student.age }}</td>
          <td>{{ student.class_name }}</td>
          <td>{{ student.phone }}</td>
          <td>
            <button class="edit-btn" @click="editStudent(student)">编辑</button>
            <button class="delete-btn" @click="deleteStudent(student.id)">删除</button>
          </td>
        </tr>
        <tr v-if="filteredStudents.length === 0">
          <td colspan="7" class="empty-text">暂无数据</td>
        </tr>
      </tbody>
    </table>

    <!-- 添加/编辑对话框 -->
    <div v-if="showAddDialog" class="dialog-overlay">
      <div class="dialog">
        <h3>{{ isEditing ? '编辑学生' : '添加学生' }}</h3>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>学号</label>
            <input 
              type="text" 
              v-model="form.student_id" 
              required
              :disabled="isEditing"
            >
          </div>
          <div class="form-group">
            <label>姓名</label>
            <input 
              type="text" 
              v-model="form.name" 
              required
            >
          </div>
          <div class="form-group">
            <label>性别</label>
            <select v-model="form.gender" required>
              <option value="男">男</option>
              <option value="女">女</option>
            </select>
          </div>
          <div class="form-group">
            <label>年龄</label>
            <input 
              type="number" 
              v-model="form.age" 
              required
              min="1"
              max="100"
            >
          </div>
          <div class="form-group">
            <label>班级</label>
            <select v-model="form.class_id" required>
              <option v-for="cls in classes" :key="cls.id" :value="cls.id">
                {{ cls.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>联系电话</label>
            <input 
              type="tel" 
              v-model="form.phone" 
              required
              pattern="[0-9]{11}"
              title="请输入11位手机号码"
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
  name: 'StudentManagement',
  setup() {
    const students = ref([])
    const classes = ref([])
    const searchQuery = ref('')
    const showAddDialog = ref(false)
    const isEditing = ref(false)
    const currentId = ref(null)
    const form = reactive({
      student_id: '',
      name: '',
      gender: '男',
      age: '',
      class_id: '',
      phone: ''
    })

    const fetchStudents = async () => {
      try {
        const response = await request.get('/api/students/')
        students.value = response.data
      } catch (error) {
        console.error('获取学生列表失败:', error)
      }
    }

    const fetchClasses = async () => {
      try {
        const response = await request.get('/api/classes/')
        classes.value = response.data
      } catch (error) {
        console.error('获取班级列表失败:', error)
      }
    }

    const filteredStudents = computed(() => {
      const query = searchQuery.value.toLowerCase()
      return students.value.filter(student => 
        student.name.toLowerCase().includes(query) ||
        student.student_id.toLowerCase().includes(query) ||
        student.class_name.toLowerCase().includes(query)
      )
    })

    const handleSubmit = async () => {
      try {
        if (isEditing.value) {
          await request.put(`/api/students/${currentId.value}/`, form)
        } else {
          await request.post('/api/students/', form)
        }
        await fetchStudents()
        closeDialog()
      } catch (error) {
        alert(error.response?.data?.message || '操作失败')
      }
    }

    const closeDialog = () => {
      showAddDialog.value = false
      isEditing.value = false
      Object.assign(form, {
        student_id: '',
        name: '',
        gender: '男',
        age: '',
        class_id: '',
        phone: ''
      })
    }

    const editStudent = (student) => {
      isEditing.value = true
      currentId.value = student.id
      Object.assign(form, {
        ...student,
        class_id: student.class_id.id
      })
      showAddDialog.value = true
    }

    const deleteStudent = async (id) => {
      if (confirm('确定要删除这个学生吗？')) {
        try {
          await request.delete(`/api/students/${id}/`)
          await fetchStudents()
        } catch (error) {
          alert(error.response?.data?.message || '删除失败')
        }
      }
    }

    onMounted(() => {
      fetchStudents()
      fetchClasses()
    })

    return {
      students,
      classes,
      searchQuery,
      showAddDialog,
      isEditing,
      form,
      filteredStudents,
      handleSubmit,
      editStudent,
      deleteStudent,
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