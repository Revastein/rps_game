<template>
  <div class="login-wrapper">
    <h1 class="login-h1">Sign In</h1>
    <form class="signin-form" @submit.prevent="login" autocomplete="off">
      <input type="text" v-model="username" placeholder="Username" name="username_input"/>
      <input type="password" v-model="password" placeholder="Password" name="password_input"/>
      <button type="submit" name="submit_button">&#xf0da;</button>
      <p>Don't have an account yet?
        <router-link to="/register">Click here</router-link>
      </p>
    </form>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<script>
import LoginFormScript from "@/scripts/LoginFormScript";

export default LoginFormScript;
</script>

<style scoped>
@import "@/assets/css/login.css";
</style>
