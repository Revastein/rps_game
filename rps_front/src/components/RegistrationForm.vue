<template>
  <div class="register-wrapper">
    <h1 class="register-h1">Registration</h1>
    <form class="register-form" @submit.prevent="register" autocomplete="off">
      <input type="text" v-model="username" placeholder="Username" name="username_input"/>
      <input type="password" v-model="password" placeholder="Password" name="password_input"/>
      <button type="submit" name="submit_button">&#xf0da;</button>
      <transition name="fade">
        <p v-if="registrationSuccess" class="success-message">Registration successful! Redirecting...</p>
      </transition>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <p>Already have an account?
        <router-link to="/login">Click here</router-link>
      </p>
    </form>
  </div>
</template>

<script>
import RegistrationFormScript from "@/scripts/RegistrationFormScript.js";

export default RegistrationFormScript;
</script>

<style scoped>
@import "@/assets/css/register.css";
</style>
