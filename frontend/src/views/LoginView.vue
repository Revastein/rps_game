<template>
  <div class="login-page">
    <LoginForm />
  </div>
</template>

<script setup>
import LoginForm from '@/components/forms/LoginForm.vue';

const link = document.createElement("link");
link.rel = "stylesheet";
link.href = "/assets/css/login.css";
document.head.appendChild(link);

import { onUnmounted } from "vue";
onUnmounted(() => {
  document.head.removeChild(link);
});
</script>
