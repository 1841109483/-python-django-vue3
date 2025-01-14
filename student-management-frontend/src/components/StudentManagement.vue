<template>
  <div class="management-page">
    <div class="page-header">
      <h2>学生管理</h2>
      <button class="add-btn" @click="showAddDialog = true">
        <i class="icon">➕</i> 添加学生
      </button>
    </div>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="搜索学生姓名或学号..."
        @input="handleSearch"
      >
    </div>

    <!-- 学生列表 -->
    <div class="table-container">
      <table>
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
          <tr v-for="student in students" :key="student.id">
            <td>{{ student.student_id }}</td>
            <td>{{ student.name }}</td>
            <td>{{ student.gender }}</td>
            <td>{{ student.age }}</td>
            <td>{{ student.class_name }}</td>
            <td>{{ student.phone }}</td>
            <td>
              <button class="edit-btn" @click="handleEdit(student)">编辑</button>
              <button class="delete-btn" @click="handleDelete(student.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 添加/编辑对话框 -->
    <div class="dialog-overlay" v-if="showAddDialog" @click="showAddDialog = false">
      <div class="dialog" @click.stop>
        <h3>{{ editingStudent ? '编辑学生' : '添加学生' }}</h3>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>学号</label>
            <input type="text" v-model="studentForm.student_id" required>
          </div>
          <div class="form-group">
            <label>姓名</label>
            <input type="text" v-model="studentForm.name" required>
          </div>
          <div class="form-group">
            <label>性别</label>
            <select v-model="studentForm.gender" required>
              <option value="男">男</option>
              <option value="女">女</option>
            </select>
          </div>
          <div class="form-group">
            <label>年龄</label>
            <input type="number" v-model="studentForm.age" required>
          </div>
          <div class="form-group">
            <label>班级</label>
            <select v-model="studentForm.class_id" required>
              <option v-for="class_ in classes" :key="class_.id" :value="class_.id">
                {{ class_.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>联系电话</label>
            <input type="tel" v-model="studentForm.phone" required>
          </div>
          <div class="dialog-buttons">
            <button type="button" @click="showAddDialog = false">取消</button>
            <button type="submit">确定</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'StudentManagement',
  data() {
    return {
      students: [],
      classes: [],
      searchQuery: '',
      showAddDialog: false,
      editingStudent: null,
      studentForm: {
        student_id: '',
        name: '',
        gender: '男',
        age: '',
        class_id: '',
        phone: ''
      }
    }
  },
  created() {
    this.fetchStudents()
    this.fetchClasses()
  },
  methods: {
    async fetchStudents() {
      try {
        const response = await axios.get('/api/students/')
        this.students = response.data
      } catch (error) {
        console.error('获取学生列表失败:', error)
      }
    },
    async fetchClasses() {
      try {
        const response = await axios.get('/api/classes/')
        this.classes = response.data
      } catch (error) {
        console.error('获取班级列表失败:', error)
      }
    },
    handleEdit(student) {
      this.editingStudent = student
      this.studentForm = { ...student }
      this.showAddDialog = true
    },
    async handleDelete(id) {
      if (confirm('确定要删除这名学生吗？')) {
        try {
          await axios.delete(`/api/students/${id}/`)
          this.fetchStudents()
        } catch (error) {
          console.error('删除学生失败:', error)
        }
      }
    },
    async handleSubmit() {
      try {
        if (this.editingStudent) {
          await axios.put(`/api/students/${this.editingStudent.id}/`, this.studentForm)
        } else {
          await axios.post('/api/students/', this.studentForm)
        }
        this.showAddDialog = false
        this.fetchStudents()
        this.resetForm()
      } catch (error) {
        console.error('保存学生信息失败:', error)
      }
    },
    resetForm() {
      this.studentForm = {
        student_id: '',
        name: '',
        gender: '男',
        age: '',
        class_id: '',
        phone: ''
      }
      this.editingStudent = null
    },
    handleSearch() {
      // 实现搜索功能
      // TODO: 可以改为后端搜索
      if (!this.searchQuery) {
        this.fetchStudents()
        return
      }
      const query = this.searchQuery.toLowerCase()
      this.students = this.students.filter(student => 
        student.name.toLowerCase().includes(query) ||
        student.student_id.toLowerCase().includes(query)
      )
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

.add-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.add-btn:hover {
  background-color: #40a9ff;
}

.search-bar {
  margin-bottom: 1.5rem;
}

.search-bar input {
  width: 300px;
  padding: 0.5rem;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
}

.table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}

th {
  background-color: #fafafa;
  font-weight: 500;
}

.edit-btn, .delete-btn {
  padding: 0.3rem 0.8rem;
  margin: 0 0.2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.edit-btn {
  background-color: #1890ff;
  color: white;
}

.delete-btn {
  background-color: #ff4d4f;
  color: white;
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
}

.dialog h3 {
  margin-bottom: 1.5rem;
}

.dialog-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.dialog-buttons button {
  padding: 0.5rem 1.5rem;
}

.dialog-buttons button:first-child {
  background-color: #f0f0f0;
  color: #666;
}
</style> 