<template>
  <div class="login-wrapper">
    <h1 class="login-h1">Login</h1>

    <form class="login-form" @submit.prevent="login" autocomplete="off">
      <input type="text" v-model="username" placeholder="Username" required />
      <input type="password" v-model="password" placeholder="Password" required />
      <button type="submit" :disabled="loading">Login</button>

      <transition name="fade">
        <p v-if="loginSuccess" class="success-message">Login successful! Redirecting...</p>
      </transition>

      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <p class="register-link" @click="goToRegister">Don't have an account yet?</p>
    </form>
  </div>
</template>

<script>
import LoginFormScript from "@/scripts/LoginFormScript.js";
export default LoginFormScript;
</script>
