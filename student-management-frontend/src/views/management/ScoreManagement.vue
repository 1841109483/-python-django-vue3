<template>
  <div class="management-page">
    <div class="page-header">
      <h2>成绩管理</h2>
      <button class="add-btn" @click="showAddDialog = true">
        <i class="icon">➕</i> 添加成绩
      </button>
    </div>

    <div class="search-bar">
      <input type="text" v-model="searchQuery" placeholder="搜索学生或课程...">
    </div>

    <table class="table">
      <thead>
        <tr>
          <th>学号</th>
          <th>学生姓名</th>
          <th>课程编号</th>
          <th>课程名称</th>
          <th>成绩</th>
          <th>学期</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="score in filteredScores" :key="score.id">
          <td>{{ score.student_id }}</td>
          <td>{{ score.student_name }}</td>
          <td>{{ score.course_id }}</td>
          <td>{{ score.course_name }}</td>
          <td>{{ score.score }}</td>
          <td>{{ score.semester }}</td>
          <td>
            <button class="edit-btn" @click="editScore(score)">编辑</button>
            <button class="delete-btn" @click="deleteScore(score.id)">删除</button>
          </td>
        </tr>
        <tr v-if="filteredScores.length === 0">
          <td colspan="7" class="empty-text">暂无数据</td>
        </tr>
      </tbody>
    </table>

    <!-- 添加/编辑对话框 -->
    <div v-if="showAddDialog" class="dialog-overlay">
      <div class="dialog">
        <h3>{{ isEditing ? '编辑成绩' : '添加成绩' }}</h3>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>学生</label>
            <select v-model="form.student" required>
              <option value="">请选择学生</option>
              <option v-for="student in students" :key="student.id" :value="student.id">
                {{ student.name }} ({{ student.student_id }})
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>课程</label>
            <select v-model="form.course" required>
              <option value="">请选择课程</option>
              <option v-for="course in courses" :key="course.id" :value="course.id">
                {{ course.name }} ({{ course.course_id }})
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>成绩</label>
            <input 
              type="number" 
              v-model="form.score" 
              required
              min="0"
              max="100"
              step="0.1"
            >
          </div>
          <div class="form-group">
            <label>学期</label>
            <select v-model="form.semester" required>
              <option value="">请选择学期</option>
              <option v-for="semester in semesters" :key="semester" :value="semester">
                {{ semester }}
              </option>
            </select>
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
  name: 'ScoreManagement',
  setup() {
    const scores = ref([])
    const students = ref([])
    const courses = ref([])
    const searchQuery = ref('')
    const showAddDialog = ref(false)
    const isEditing = ref(false)
    const currentId = ref(null)
    
    // 预设学期列表
    const semesters = [
      '2023-2024-1',
      '2023-2024-2',
      '2024-2025-1',
      '2024-2025-2'
    ]

    const form = reactive({
      student: '',
      course: '',
      score: '',
      semester: ''
    })

    const fetchScores = async () => {
      try {
        const response = await request.get('/api/scores/')
        scores.value = response.data
      } catch (error) {
        console.error('获取成绩列表失败:', error)
      }
    }

    const fetchStudents = async () => {
      try {
        const response = await request.get('/api/students/')
        students.value = response.data
      } catch (error) {
        console.error('获取学生列表失败:', error)
      }
    }

    const fetchCourses = async () => {
      try {
        const response = await request.get('/api/courses/')
        courses.value = response.data
      } catch (error) {
        console.error('获取课程列表失败:', error)
      }
    }

    const filteredScores = computed(() => {
      const query = searchQuery.value.toLowerCase()
      return scores.value.filter(score => 
        score.student_name.toLowerCase().includes(query) ||
        score.student_id.toLowerCase().includes(query) ||
        score.course_name.toLowerCase().includes(query) ||
        score.course_id.toLowerCase().includes(query)
      )
    })

    const handleSubmit = async () => {
      try {
        if (isEditing.value) {
          await request.put(`/api/scores/${currentId.value}/`, form)
        } else {
          await request.post('/api/scores/', form)
        }
        await fetchScores()
        closeDialog()
      } catch (error) {
        alert(error.response?.data?.message || '操作失败')
      }
    }

    const closeDialog = () => {
      showAddDialog.value = false
      isEditing.value = false
      Object.assign(form, {
        student: '',
        course: '',
        score: '',
        semester: ''
      })
    }

    const editScore = (score) => {
      isEditing.value = true
      currentId.value = score.id
      Object.assign(form, {
        student: score.student,
        course: score.course,
        score: score.score,
        semester: score.semester
      })
      showAddDialog.value = true
    }

    const deleteScore = async (id) => {
      if (confirm('确定要删除这个成绩记录吗？')) {
        try {
          await request.delete(`/api/scores/${id}/`)
          await fetchScores()
        } catch (error) {
          alert(error.response?.data?.message || '删除失败')
        }
      }
    }

    onMounted(() => {
      fetchScores()
      fetchStudents()
      fetchCourses()
    })

    return {
      scores,
      students,
      courses,
      semesters,
      searchQuery,
      showAddDialog,
      isEditing,
      form,
      filteredScores,
      handleSubmit,
      editScore,
      deleteScore,
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

select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  background: white;
}
</style> 