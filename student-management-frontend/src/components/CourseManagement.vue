<template>
  <div class="management-page">
    <div class="page-header">
      <h2>课程管理</h2>
      <button class="add-btn" @click="showAddDialog = true">
        <i class="icon">➕</i> 添加课程
      </button>
    </div>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="搜索课程名称或编号..."
        @input="handleSearch"
      >
    </div>

    <!-- 课程列表 -->
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>课程编号</th>
            <th>课程名称</th>
            <th>任课教师</th>
            <th>学分</th>
            <th>课时</th>
            <th>课程描述</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="course in courses" :key="course.id">
            <td>{{ course.course_id }}</td>
            <td>{{ course.name }}</td>
            <td>{{ course.teacher }}</td>
            <td>{{ course.credit }}</td>
            <td>{{ course.hours }}</td>
            <td class="description">{{ course.description }}</td>
            <td>
              <button class="edit-btn" @click="handleEdit(course)">编辑</button>
              <button class="delete-btn" @click="handleDelete(course.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 添加/编辑对话框 -->
    <div class="dialog-overlay" v-if="showAddDialog" @click="showAddDialog = false">
      <div class="dialog" @click.stop>
        <h3>{{ editingCourse ? '编辑课程' : '添加课程' }}</h3>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>课程编号</label>
            <input type="text" v-model="courseForm.course_id" required>
          </div>
          <div class="form-group">
            <label>课程名称</label>
            <input type="text" v-model="courseForm.name" required>
          </div>
          <div class="form-group">
            <label>任课教师</label>
            <input type="text" v-model="courseForm.teacher" required>
          </div>
          <div class="form-group">
            <label>学分</label>
            <input type="number" step="0.1" v-model="courseForm.credit" required>
          </div>
          <div class="form-group">
            <label>课时</label>
            <input type="number" v-model="courseForm.hours" required>
          </div>
          <div class="form-group">
            <label>课程描述</label>
            <textarea v-model="courseForm.description" rows="4"></textarea>
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
  name: 'CourseManagement',
  data() {
    return {
      courses: [],
      searchQuery: '',
      showAddDialog: false,
      editingCourse: null,
      courseForm: {
        course_id: '',
        name: '',
        teacher: '',
        credit: '',
        hours: '',
        description: ''
      }
    }
  },
  created() {
    this.fetchCourses()
  },
  methods: {
    async fetchCourses() {
      try {
        const response = await axios.get('/api/courses/')
        this.courses = response.data
      } catch (error) {
        console.error('获取课程列表失败:', error)
      }
    },
    handleEdit(course) {
      this.editingCourse = course
      this.courseForm = { ...course }
      this.showAddDialog = true
    },
    async handleDelete(id) {
      if (confirm('确定要删除这门课程吗？')) {
        try {
          await axios.delete(`/api/courses/${id}/`)
          this.fetchCourses()
        } catch (error) {
          console.error('删除课程失败:', error)
        }
      }
    },
    async handleSubmit() {
      try {
        if (this.editingCourse) {
          await axios.put(`/api/courses/${this.editingCourse.id}/`, this.courseForm)
        } else {
          await axios.post('/api/courses/', this.courseForm)
        }
        this.showAddDialog = false
        this.fetchCourses()
        this.resetForm()
      } catch (error) {
        console.error('保存课程信息失败:', error)
      }
    },
    resetForm() {
      this.courseForm = {
        course_id: '',
        name: '',
        teacher: '',
        credit: '',
        hours: '',
        description: ''
      }
      this.editingCourse = null
    },
    handleSearch() {
      if (!this.searchQuery) {
        this.fetchCourses()
        return
      }
      const query = this.searchQuery.toLowerCase()
      this.courses = this.courses.filter(course => 
        course.name.toLowerCase().includes(query) ||
        course.course_id.toLowerCase().includes(query)
      )
    }
  }
}
</script>

<style scoped>
/* 复用 StudentManagement.vue 的样式 */
.management-page {
  padding: 2rem;
}

/* 其他样式与 StudentManagement.vue 相同 */

/* 添加课程描述的特殊样式 */
.description {
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

textarea {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  resize: vertical;
}
</style> 