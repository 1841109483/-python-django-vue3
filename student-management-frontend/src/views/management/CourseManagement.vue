<template>
  <div class="management-page">
    <div class="page-header">
      <h2>课程管理</h2>
      <button class="add-btn" @click="showAddDialog = true">
        <i class="icon">➕</i> 添加课程
      </button>
    </div>

    <div class="search-bar">
      <input type="text" v-model="searchQuery" placeholder="搜索课程...">
    </div>

    <table class="table">
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
        <tr v-for="course in filteredCourses" :key="course.id">
          <td>{{ course.course_id }}</td>
          <td>{{ course.name }}</td>
          <td>{{ course.teacher }}</td>
          <td>{{ course.credit }}</td>
          <td>{{ course.hours }}</td>
          <td>{{ course.description }}</td>
          <td>
            <button class="edit-btn" @click="editCourse(course)">编辑</button>
            <button class="delete-btn" @click="deleteCourse(course.id)">删除</button>
          </td>
        </tr>
        <tr v-if="filteredCourses.length === 0">
          <td colspan="7" class="empty-text">暂无数据</td>
        </tr>
      </tbody>
    </table>

    <!-- 添加/编辑对话框 -->
    <div v-if="showAddDialog" class="dialog-overlay">
      <div class="dialog">
        <h3>{{ isEditing ? '编辑课程' : '添加课程' }}</h3>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>课程编号</label>
            <input 
              type="text" 
              v-model="form.course_id" 
              required
              :disabled="isEditing"
            >
          </div>
          <div class="form-group">
            <label>课程名称</label>
            <input 
              type="text" 
              v-model="form.name" 
              required
            >
          </div>
          <div class="form-group">
            <label>任课教师</label>
            <input 
              type="text" 
              v-model="form.teacher" 
              required
            >
          </div>
          <div class="form-group">
            <label>学分</label>
            <input 
              type="number" 
              v-model="form.credit" 
              required
              min="0.5"
              max="10"
              step="0.5"
            >
          </div>
          <div class="form-group">
            <label>课时</label>
            <input 
              type="number" 
              v-model="form.hours" 
              required
              min="1"
            >
          </div>
          <div class="form-group">
            <label>课程描述</label>
            <textarea 
              v-model="form.description" 
              rows="3"
            ></textarea>
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
  name: 'CourseManagement',
  setup() {
    const courses = ref([])
    const searchQuery = ref('')
    const showAddDialog = ref(false)
    const isEditing = ref(false)
    const currentId = ref(null)
    const form = reactive({
      course_id: '',
      name: '',
      teacher: '',
      credit: '',
      hours: '',
      description: ''
    })

    const fetchCourses = async () => {
      try {
        const response = await request.get('/api/courses/')
        courses.value = response.data
      } catch (error) {
        console.error('获取课程列表失败:', error)
      }
    }

    const filteredCourses = computed(() => {
      const query = searchQuery.value.toLowerCase()
      return courses.value.filter(course => 
        course.name.toLowerCase().includes(query) ||
        course.course_id.toLowerCase().includes(query) ||
        course.teacher.toLowerCase().includes(query)
      )
    })

    const handleSubmit = async () => {
      try {
        if (isEditing.value) {
          await request.put(`/api/courses/${currentId.value}/`, form)
        } else {
          await request.post('/api/courses/', form)
        }
        await fetchCourses()
        closeDialog()
      } catch (error) {
        alert(error.response?.data?.message || '操作失败')
      }
    }

    const closeDialog = () => {
      showAddDialog.value = false
      isEditing.value = false
      Object.assign(form, {
        course_id: '',
        name: '',
        teacher: '',
        credit: '',
        hours: '',
        description: ''
      })
    }

    const editCourse = (course) => {
      isEditing.value = true
      currentId.value = course.id
      Object.assign(form, course)
      showAddDialog.value = true
    }

    const deleteCourse = async (id) => {
      if (confirm('确定要删除这个课程吗？')) {
        try {
          await request.delete(`/api/courses/${id}/`)
          await fetchCourses()
        } catch (error) {
          alert(error.response?.data?.message || '删除失败')
        }
      }
    }

    onMounted(fetchCourses)

    return {
      courses,
      searchQuery,
      showAddDialog,
      isEditing,
      form,
      filteredCourses,
      handleSubmit,
      editCourse,
      deleteCourse,
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

textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  resize: vertical;
}

.dialog-buttons {
  margin-top: 2rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
</style> 