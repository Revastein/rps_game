<template>
  <div class="game-body">

    <div class="user-in-queue-container">
      <p class="user-in-queue-text" v-show="userInQueue">Player in queue</p>
      <p v-if="userInQueue" class="queue-length">Players in the queue: {{ queueLength }}</p>
    </div>

    <h1 class="duck-h1"></h1>

    <div class="menu">
      <h1 class="game-h1">Rock Paper Scissors</h1>
      <div class="user-card">
        <h2>{{ userStat.username }}</h2>
        <p>Rating: {{ userStat.rating }}</p>
        <p>Rating position: {{ userPosition }}</p>
        <p>Games played: {{ userStat.games_played }}</p>
        <p>Wins: {{ userStat.wins }}</p>
        <p>Losses: {{ userStat.losses }}</p>
        <p>Ties: {{ userStat.ties }}</p>
      </div>
          <div class="button-container">
        <button v-if="!userInQueue" class="game-btn" @click="enterQueue" :disabled="searching">Start the battle</button>
        <div v-if="userInQueue" class="popup">
          <button class="game-btn" @click="cancelQueue">Leave the queue</button>
        </div>
        <button v-if="inLobby" class="game-btn" @click="returnToLobby">Return to Lobby</button>
      </div>
    </div>

    <div class="top-players">
      <div class="top-players-box">
        <h2>Top Players</h2>
        <div v-for="(player, index) in topPlayers" :key="player.user_id">
          <p>{{ index + 1 }}. {{ player.username }} - {{ player.rating }}</p>
        </div>
      </div>

      <div class="current-player-box">
        <h2>Current Player</h2>
        <p v-if="userPosition !== -1">
          {{ userPosition }}. {{ userStat.username }} - {{ userStat.rating }}
        </p>
        <p v-else>
          Current player not found in the top players.
        </p>
      </div>
    </div>

  </div>
</template>


<script>
import GameFormScript from "@/scripts/GameFormScript";

export default {
  setup: GameFormScript.setup,
};
</script>

<style scoped>
@import "../assets/css/game.css";
</style>
