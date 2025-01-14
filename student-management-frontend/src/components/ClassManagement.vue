<template>
  <div class="management-page">
    <div class="page-header">
      <h2>班级管理</h2>
      <button class="add-btn" @click="showAddDialog = true">
        <i class="icon">➕</i> 添加班级
      </button>
    </div>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="搜索班级名称..."
        @input="handleSearch"
      >
      <select v-model="gradeFilter" @change="handleSearch">
        <option value="">所有年级</option>
        <option v-for="grade in grades" :key="grade" :value="grade">
          {{ grade }}年级
        </option>
      </select>
    </div>

    <!-- 班级列表 -->
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>班级名称</th>
            <th>年级</th>
            <th>学生人数</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="class_ in classes" :key="class_.id">
            <td>{{ class_.name }}</td>
            <td>{{ class_.grade }}</td>
            <td>{{ class_.student_count || 0 }}</td>
            <td>{{ formatDate(class_.created_at) }}</td>
            <td>
              <button class="view-btn" @click="handleViewStudents(class_)">查看学生</button>
              <button class="edit-btn" @click="handleEdit(class_)">编辑</button>
              <button class="delete-btn" @click="handleDelete(class_.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 添加/编辑对话框 -->
    <div class="dialog-overlay" v-if="showAddDialog" @click="showAddDialog = false">
      <div class="dialog" @click.stop>
        <h3>{{ editingClass ? '编辑班级' : '添加班级' }}</h3>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>班级名称</label>
            <input type="text" v-model="classForm.name" required>
          </div>
          <div class="form-group">
            <label>年级</label>
            <select v-model="classForm.grade" required>
              <option v-for="grade in grades" :key="grade" :value="grade">
                {{ grade }}年级
              </option>
            </select>
          </div>
          <div class="dialog-buttons">
            <button type="button" @click="showAddDialog = false">取消</button>
            <button type="submit">确定</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 查看学生对话框 -->
    <div class="dialog-overlay" v-if="showStudentsDialog" @click="showStudentsDialog = false">
      <div class="dialog" @click.stop>
        <h3>{{ selectedClass?.name }}的学生列表</h3>
        <div class="students-list">
          <table>
            <thead>
              <tr>
                <th>学号</th>
                <th>姓名</th>
                <th>性别</th>
                <th>年龄</th>
                <th>联系电话</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in classStudents" :key="student.id">
                <td>{{ student.student_id }}</td>
                <td>{{ student.name }}</td>
                <td>{{ student.gender }}</td>
                <td>{{ student.age }}</td>
                <td>{{ student.phone }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="dialog-buttons">
          <button @click="showStudentsDialog = false">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ClassManagement',
  data() {
    return {
      classes: [],
      searchQuery: '',
      gradeFilter: '',
      showAddDialog: false,
      showStudentsDialog: false,
      editingClass: null,
      selectedClass: null,
      classStudents: [],
      classForm: {
        name: '',
        grade: ''
      },
      grades: ['一', '二', '三', '四']
    }
  },
  created() {
    this.fetchClasses()
  },
  methods: {
    async fetchClasses() {
      try {
        const response = await axios.get('/api/classes/')
        this.classes = response.data
      } catch (error) {
        console.error('获取班级列表失败:', error)
      }
    },
    handleEdit(class_) {
      this.editingClass = class_
      this.classForm = { ...class_ }
      this.showAddDialog = true
    },
    async handleDelete(id) {
      if (confirm('确定要删除这个班级吗？')) {
        try {
          await axios.delete(`/api/classes/${id}/`)
          this.fetchClasses()
        } catch (error) {
          console.error('删除班级失败:', error)
          alert('删除失败：可能存在关联的学生数据')
        }
      }
    },
    async handleSubmit() {
      try {
        if (this.editingClass) {
          await axios.put(`/api/classes/${this.editingClass.id}/`, this.classForm)
        } else {
          await axios.post('/api/classes/', this.classForm)
        }
        this.showAddDialog = false
        this.fetchClasses()
        this.resetForm()
      } catch (error) {
        console.error('保存班级信息失败:', error)
        alert(error.response?.data?.message || '操作失败')
      }
    },
    async handleViewStudents(class_) {
      this.selectedClass = class_
      try {
        const response = await axios.get(`/api/students/?class_id=${class_.id}`)
        this.classStudents = response.data
        this.showStudentsDialog = true
      } catch (error) {
        console.error('获取班级学生列表失败:', error)
      }
    },
    resetForm() {
      this.classForm = {
        name: '',
        grade: ''
      }
      this.editingClass = null
    },
    handleSearch() {
      // 实现本地搜索和筛选
      this.fetchClasses()
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.search-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.search-bar input,
.search-bar select {
  padding: 0.5rem;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  width: 200px;
}

.view-btn {
  background-color: #13c2c2;
  color: white;
  padding: 0.3rem 0.8rem;
  margin: 0 0.2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.students-list {
  max-height: 400px;
  overflow-y: auto;
  margin: 1rem 0;
}

/* 其他样式继承自 StudentManagement.vue */
</style> 