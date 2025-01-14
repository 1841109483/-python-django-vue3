<template>
  <div class="dashboard">
    <div class="welcome-banner">
      <h2>欢迎回来，{{ user?.username }}！</h2>
      <p>今天是 {{ currentDate }}</p>
    </div>
    
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon student">👥</div>
        <div class="stat-info">
          <h3>总学生数</h3>
          <p>{{ stats.studentCount }}</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon course">📚</div>
        <div class="stat-info">
          <h3>总课程数</h3>
          <p>{{ stats.courseCount }}</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon class">👨‍👩‍👦‍👦</div>
        <div class="stat-info">
          <h3>总班级数</h3>
          <p>{{ stats.classCount }}</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon grade">📝</div>
        <div class="stat-info">
          <h3>平均成绩</h3>
          <p>{{ stats.averageScore }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, onMounted } from 'vue'
import { useStore } from 'vuex'
import request from '@/utils/request'

export default {
  name: 'HomePage',
  setup() {
    const store = useStore()
    const stats = reactive({
      studentCount: 0,
      courseCount: 0,
      classCount: 0,
      averageScore: 0
    })

    const fetchStats = async () => {
      try {
        const [students, courses, classes, scores] = await Promise.all([
          request.get('/api/students/'),
          request.get('/api/courses/'),
          request.get('/api/classes/'),
          request.get('/api/scores/')
        ])
        
        stats.studentCount = students.data.length
        stats.courseCount = courses.data.length
        stats.classCount = classes.data.length
        
        if (scores.data.length > 0) {
          const totalScore = scores.data.reduce((sum, score) => sum + parseFloat(score.score), 0)
          stats.averageScore = (totalScore / scores.data.length).toFixed(1)
        }
      } catch (error) {
        console.error('获取统计数据失败:', error)
      }
    }

    onMounted(fetchStats)

    return {
      user: store.state.user,
      stats,
      currentDate: new Date().toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
      })
    }
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-banner {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.welcome-banner h2 {
  margin: 0;
  color: #1890ff;
}

.welcome-banner p {
  margin: 0.5rem 0 0;
  color: #666;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5em;
  margin-right: 1rem;
}

.stat-info h3 {
  margin: 0;
  color: #666;
  font-size: 0.9em;
  font-weight: normal;
}

.stat-info p {
  margin: 0.5rem 0 0;
  font-size: 1.5em;
  font-weight: bold;
  color: #1890ff;
}

.student { background: #e6f7ff; }
.course { background: #f6ffed; }
.class { background: #fff7e6; }
.grade { background: #fff1f0; }
</style> 