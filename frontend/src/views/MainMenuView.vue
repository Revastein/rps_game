<template>
  <div class="main-menu-page">
    <MainMenuForm />
  </div>
</template>

<script setup>
import MainMenuForm from '@/components/forms/MainMenuForm.vue';

const link = document.createElement("link");
link.rel = "stylesheet";
link.href = "/assets/css/menu.css";
document.head.appendChild(link);

import { onUnmounted } from "vue";
onUnmounted(() => {
  document.head.removeChild(link);
});
</script>
