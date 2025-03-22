<template>
  <div class="register-page">
    <RegistrationForm />
  </div>
</template>

<script setup>
import RegistrationForm from '@/components/forms/RegistrationForm.vue';

const link = document.createElement("link");
link.rel = "stylesheet";
link.href = "/assets/css/register.css";
document.head.appendChild(link);

import { onUnmounted } from "vue";
onUnmounted(() => {
  document.head.removeChild(link);
});
</script>
