<template>
  <div class="lobby">
    <h1 class="lobby-header">Let the party get started</h1>
    <div class="choice_button">
      <button @click="makeChoice('rock')">Rock</button>
      <button @click="makeChoice('paper')">Paper</button>
      <button @click="makeChoice('scissors')">Scissors</button>
    </div>
    <p v-if="winner !== null">Result: {{ result }}</p>
    <p class="timer" v-if="timerVisible">{{ timerText }}</p>
    <button class="quit-button" @click="leaveLobby">Quit to main lobby</button>
    <div v-if="winner !== null">
      <button class="restart-button" @click="requestRematch">Restart Lobby</button>
    </div>
  </div>
</template>

<script>
import LobbyFormScript from "@/scripts/GameLobbyFormScript";

export default {
  setup: LobbyFormScript.setup,
};
</script>

<style scoped>
@import "@/assets/css/game_lobby.css";
</style>
