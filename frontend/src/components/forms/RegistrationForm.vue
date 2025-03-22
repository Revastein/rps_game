<template>
  <div class="register-wrapper">
    <h1 class="register-h1">Registration</h1>

    <form class="register-form" @submit.prevent="register" autocomplete="off">
      <input
        type="text"
        v-model="username"
        placeholder="Username"
        required
        maxlength="16"
      />
      <input
        type="password"
        v-model="password"
        placeholder="Password"
        required
      />
      <input
        type="password"
        v-model="confirmPassword"
        placeholder="Confirm Password"
        required
      />

      <button type="submit" :disabled="loading">Register</button>

      <transition name="fade">
        <p v-if="registrationSuccess" class="success-message">Registration successful! Redirecting...</p>
      </transition>

      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <p class="login-link" @click="goToLogin">Already have an account?</p>
    </form>
  </div>
</template>

<script>
import RegistrationFormScript from "@/scripts/RegistrationFormScript.js";
export default RegistrationFormScript;
</script>

