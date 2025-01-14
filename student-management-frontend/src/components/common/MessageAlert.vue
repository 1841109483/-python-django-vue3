<template>
  <transition name="fade">
    <div v-if="show" :class="['message-alert', type]">
      {{ message }}
    </div>
  </transition>
</template>

<script>
export default {
  name: 'MessageAlert',
  props: {
    show: Boolean,
    message: String,
    type: {
      type: String,
      default: 'info',
      validator: value => ['info', 'success', 'warning', 'error'].includes(value)
    }
  }
}
</script>

<style scoped>
.message-alert {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 20px;
  border-radius: 4px;
  color: white;
  font-size: 14px;
  z-index: 1000;
  box-shadow: var(--shadow);
}

.info {
  background: var(--primary-color);
}

.success {
  background: var(--success-color);
}

.warning {
  background: var(--warning-color);
}

.error {
  background: var(--error-color);
}
</style> 