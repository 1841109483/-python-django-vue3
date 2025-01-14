<template>
  <div class="home">
    <div class="welcome">
      <h2>欢迎回来，！</h2>
      <p>今天是 {{ currentDate }}</p>
    </div>

    <div class="stats-cards">
      <div class="stat-card">
        <i class="icon">👨‍🎓</i>
        <div class="stat-info">
          <div class="stat-value">{{ stats.totalStudents }}</div>
          <div class="stat-label">总学生数</div>
        </div>
      </div>
      <div class="stat-card">
        <i class="icon">📚</i>
        <div class="stat-info">
          <div class="stat-value">{{ stats.totalCourses }}</div>
          <div class="stat-label">总课程数</div>
        </div>
      </div>
      <div class="stat-card">
        <i class="icon">👥</i>
        <div class="stat-info">
          <div class="stat-value">{{ stats.totalClasses }}</div>
          <div class="stat-label">总班级数</div>
        </div>
      </div>
      <div class="stat-card">
        <i class="icon">📊</i>
        <div class="stat-info">
          <div class="stat-value">{{ stats.averageScore }}</div>
          <div class="stat-label">平均成绩</div>
        </div>
      </div>
    </div>

    <div class="charts-container">
      <div class="chart-card">
        <h3>班级学生分布</h3>
        <v-chart class="chart" :option="classDistributionOption" autoresize />
      </div>
      <div class="chart-card">
        <h3>成绩分布</h3>
        <v-chart class="chart" :option="scoreDistributionOption" autoresize />
      </div>
      <div class="chart-card">
        <h3>课程平均分</h3>
        <v-chart class="chart" :option="courseAverageOption" autoresize />
      </div>
      <div class="chart-card">
        <h3>性别比例</h3>
        <v-chart class="chart" :option="genderRatioOption" autoresize />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart, BarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import request from '@/utils/request'

// 注册必需的组件
use([
  CanvasRenderer,
  PieChart,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

export default {
  name: 'Home',
  setup() {
    const stats = ref({
      totalStudents: 0,
      totalCourses: 0,
      totalClasses: 0,
      averageScore: 0
    })

    const classDistributionOption = ref({
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 'left',
        padding: [20, 0, 0, 0]
      },
      series: [{
        name: '班级分布',
        type: 'pie',
        radius: '60%',
        center: ['60%', '50%'],
        data: [],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        itemStyle: {
          borderRadius: 8,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}: {c}人'
        }
      }]
    })

    const scoreDistributionOption = ref({
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: ['0-60', '60-70', '70-80', '80-90', '90-100'],
        axisLabel: {
          interval: 0
        }
      },
      yAxis: {
        type: 'value',
        name: '学生人数'
      },
      series: [{
        name: '成绩分布',
        data: [],
        type: 'bar',
        itemStyle: {
          color: '#1890ff',
          borderRadius: [4, 4, 0, 0]
        }
      }]
    })

    const courseAverageOption = ref({
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: [],
        axisLabel: {
          interval: 0,
          rotate: 30
        }
      },
      yAxis: {
        type: 'value',
        min: 0,
        max: 100,
        name: '平均分'
      },
      series: [{
        name: '课程平均分',
        data: [],
        type: 'bar',
        itemStyle: {
          color: '#52c41a',
          borderRadius: [4, 4, 0, 0]
        }
      }]
    })

    const genderRatioOption = ref({
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c}人 ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 'left',
        padding: [20, 0, 0, 0]
      },
      series: [{
        name: '性别比例',
        type: 'pie',
        radius: '60%',
        center: ['60%', '50%'],
        data: [],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        itemStyle: {
          borderRadius: 8,
          borderColor: '#fff',
          borderWidth: 2,
          color: function(params) {
            const colors = ['#1890ff', '#f5222d']
            return colors[params.dataIndex]
          }
        },
        label: {
          show: true,
          formatter: '{b}: {c}人'
        }
      }]
    })

    const fetchData = async () => {
      try {
        const response = await request.get('/api/stats/')
        const data = response.data

        // 更新统计数据
        stats.value = data.overview

        // 更新班级分布图表
        classDistributionOption.value.series[0].data = data.classDistribution

        // 更新成绩分布图表
        scoreDistributionOption.value.series[0].data = data.scoreDistribution.map(item => ({
          name: item.name,
          value: item.value
        }))

        // 更新课程平均分图表
        const courseData = data.courseAverage.filter(item => item.average != null)
        courseAverageOption.value.xAxis.data = courseData.map(item => item.name)
        courseAverageOption.value.series[0].data = courseData.map(item => 
          parseFloat(item.average).toFixed(1)
        )

        // 更新性别比例图表
        genderRatioOption.value.series[0].data = data.genderRatio.map(item => ({
          name: item.gender === 'M' ? '男' : '女',
          value: item.value
        }))

      } catch (error) {
        console.error('获取统计数据失败:', error)
      }
    }

    onMounted(() => {
      fetchData()
    })

    return {
      stats,
      currentDate: new Date().toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
      }),
      classDistributionOption,
      scoreDistributionOption,
      courseAverageOption,
      genderRatioOption
    }
  }
}
</script>

<style scoped>
.home {
  padding: 2rem;
  background-color: #f0f2f5;
  min-height: calc(100vh - 64px);
}

.welcome {
  margin-bottom: 2rem;
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.welcome h2 {
  margin: 0;
  color: #1890ff;
}

.welcome p {
  margin: 0.5rem 0 0;
  color: #666;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.icon {
  font-size: 2.5rem;
  color: #1890ff;
}

.stat-info {
  flex-grow: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #1890ff;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: #666;
  font-size: 1rem;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 1.5rem;
}

.chart-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.chart-card h3 {
  margin: 0 0 1.5rem 0;
  color: #333;
  font-size: 1.2rem;
}

.chart {
  height: 350px;
  width: 100%;
}

@media (max-width: 768px) {
  .home {
    padding: 1rem;
  }

  .charts-container {
    grid-template-columns: 1fr;
  }

  .chart {
    height: 300px;
  }

  .stat-card {
    padding: 1rem;
  }

  .stat-value {
    font-size: 1.5rem;
  }
}
</style> 