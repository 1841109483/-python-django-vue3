<template>
  <div class="management-page">
    <div class="page-header">
      <h2>成绩管理</h2>
      <button class="add-btn" @click="showAddDialog = true">
        <i class="icon">➕</i> 添加成绩
      </button>
    </div>

    <!-- 搜索和筛选 -->
    <div class="filter-bar">
      <input 
        type="text" 
        v-model="filters.studentId" 
        placeholder="按学号搜索..."
        @input="handleFilter"
      >
      <input 
        type="text" 
        v-model="filters.courseId" 
        placeholder="按课程编号搜索..."
        @input="handleFilter"
      >
      <select v-model="filters.semester" @change="handleFilter">
        <option value="">选择学期</option>
        <option v-for="sem in semesters" :key="sem" :value="sem">
          {{ sem }}
        </option>
      </select>
    </div>

    <!-- 成绩列表 -->
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>学号</th>
            <th>学生姓名</th>
            <th>课程编号</th>
            <th>课程名称</th>
            <th>学期</th>
            <th>分数</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="score in scores" :key="score.id">
            <td>{{ score.student_id }}</td>
            <td>{{ score.student_name }}</td>
            <td>{{ score.course_id }}</td>
            <td>{{ score.course_name }}</td>
            <td>{{ score.semester }}</td>
            <td :class="getScoreClass(score.score)">{{ score.score }}</td>
            <td>
              <button class="edit-btn" @click="handleEdit(score)">编辑</button>
              <button class="delete-btn" @click="handleDelete(score.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 添加/编辑对话框 -->
    <div class="dialog-overlay" v-if="showAddDialog" @click="showAddDialog = false">
      <div class="dialog" @click.stop>
        <h3>{{ editingScore ? '编辑成绩' : '添加成绩' }}</h3>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>学生</label>
            <select v-model="scoreForm.student" required>
              <option v-for="student in students" :key="student.id" :value="student.id">
                {{ student.name }} ({{ student.student_id }})
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>课程</label>
            <select v-model="scoreForm.course" required>
              <option v-for="course in courses" :key="course.id" :value="course.id">
                {{ course.name }} ({{ course.course_id }})
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>学期</label>
            <input type="text" v-model="scoreForm.semester" required
                   placeholder="例：2023-2024-1">
          </div>
          <div class="form-group">
            <label>分数</label>
            <input type="number" v-model="scoreForm.score" required
                   min="0" max="100" step="0.1">
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
  name: 'ScoreManagement',
  data() {
    return {
      scores: [],
      students: [],
      courses: [],
      filters: {
        studentId: '',
        courseId: '',
        semester: ''
      },
      showAddDialog: false,
      editingScore: null,
      scoreForm: {
        student: '',
        course: '',
        semester: '',
        score: ''
      },
      semesters: [
        '2023-2024-1',
        '2023-2024-2',
        '2024-2025-1',
        '2024-2025-2'
      ]
    }
  },
  created() {
    this.fetchScores()
    this.fetchStudents()
    this.fetchCourses()
  },
  methods: {
    async fetchScores() {
      try {
        const response = await axios.get('/api/scores/')
        this.scores = response.data
      } catch (error) {
        console.error('获取成绩列表失败:', error)
      }
    },
    async fetchStudents() {
      try {
        const response = await axios.get('/api/students/')
        this.students = response.data
      } catch (error) {
        console.error('获取学生列表失败:', error)
      }
    },
    async fetchCourses() {
      try {
        const response = await axios.get('/api/courses/')
        this.courses = response.data
      } catch (error) {
        console.error('获取课程列表失败:', error)
      }
    },
    handleEdit(score) {
      this.editingScore = score
      this.scoreForm = {
        student: score.student,
        course: score.course,
        semester: score.semester,
        score: score.score
      }
      this.showAddDialog = true
    },
    async handleDelete(id) {
      if (confirm('确定要删除这条成绩记录吗？')) {
        try {
          await axios.delete(`/api/scores/${id}/`)
          this.fetchScores()
        } catch (error) {
          console.error('删除成绩失败:', error)
        }
      }
    },
    async handleSubmit() {
      try {
        if (this.editingScore) {
          await axios.put(`/api/scores/${this.editingScore.id}/`, this.scoreForm)
        } else {
          await axios.post('/api/scores/', this.scoreForm)
        }
        this.showAddDialog = false
        this.fetchScores()
        this.resetForm()
      } catch (error) {
        console.error('保存成绩失败:', error)
        alert(error.response?.data?.message || '操作失败')
      }
    },
    resetForm() {
      this.scoreForm = {
        student: '',
        course: '',
        semester: '',
        score: ''
      }
      this.editingScore = null
    },
    async handleFilter() {
      try {
        let url = '/api/scores/?'
        if (this.filters.studentId) {
          url += `student_id=${this.filters.studentId}&`
        }
        if (this.filters.courseId) {
          url += `course_id=${this.filters.courseId}&`
        }
        if (this.filters.semester) {
          url += `semester=${this.filters.semester}`
        }
        const response = await axios.get(url)
        this.scores = response.data
      } catch (error) {
        console.error('筛选成绩失败:', error)
      }
    },
    getScoreClass(score) {
      if (score >= 90) return 'score-excellent'
      if (score >= 80) return 'score-good'
      if (score >= 60) return 'score-pass'
      return 'score-fail'
    }
  }
}
</script>

<style scoped>
.filter-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.filter-bar input,
.filter-bar select {
  padding: 0.5rem;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  width: 200px;
}

.score-excellent {
  color: #52c41a;
  font-weight: bold;
}

.score-good {
  color: #1890ff;
  font-weight: bold;
}

.score-pass {
  color: #faad14;
}

.score-fail {
  color: #ff4d4f;
  font-weight: bold;
}

/* 其他样式继承自 StudentManagement.vue */
</style> 