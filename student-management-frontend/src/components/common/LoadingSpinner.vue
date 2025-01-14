<template>
  <div class="loading-spinner">
    <div class="spinner"></div>
    <div class="text">{{ text }}</div>
  </div>
</template>

<script>
export default {
  name: 'LoadingSpinner',
  props: {
    text: {
      type: String,
      default: '加载中...'
    }
  }
}
</script>

<style scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f0f0f0;
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.text {
  margin-top: 1rem;
  color: var(--text-color);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style> 