<template>
  <div class="main-menu-wrapper">
    <h1 class="game-title">Rock Paper Scissors</h1>

    <!-- Уведомление о поиске оппонента -->
    <transition name="fade">
      <div v-if="searchingForOpponent" class="search-notification">
        <p>Searching for an opponent...</p>
        <p>Time in queue: {{ queueTimer }}s</p>
      </div>
    </transition>

    <!-- Кнопка старта игры / выхода из очереди -->
    <button
        class="start-button"
        :class="{ 'in-queue': searchingForOpponent }"
        @click="toggleQueue">
      {{ searchingForOpponent ? 'Leave Queue' : 'Start Game' }}
    </button>

    <!-- Анимированная утка -->
    <div class="duck-container">
      <img src="/assets/images/duck.gif" alt="Dancing Duck" class="duck-gif" />
    </div>

    <!-- Таблица лидеров -->
    <div class="leaderboard">
      <h2>Leaderboard</h2>
      <table>
        <thead>
        <tr>
          <th>#</th>
          <th>Player</th>
          <th>Rating</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(player, index) in leaderboard" :key="player.user_id">
          <td>{{ index + 1 }}</td>
          <td>{{ player.username }}</td>
          <td>{{ player.rating }}</td>
        </tr>
        <tr v-if="currentPlayerPosition > 5" class="current-player-row">
          <td>{{ currentPlayerPosition }}</td>
          <td>{{ currentPlayer.username }} (You)</td>
          <td>{{ currentPlayer.rating }}</td>
        </tr>
        </tbody>
      </table>
    </div>

    <!-- Данные игрока -->
    <div class="player-info">
      <h2>Your Stats</h2>
      <ul>
        <li>Rating: {{ currentPlayer.rating }}</li>
        <li>Games Played: {{ currentPlayer.games_played }}</li>
        <li>Wins: {{ currentPlayer.wins }}</li>
        <li>Losses: {{ currentPlayer.losses }}</li>
        <li>Draws: {{ currentPlayer.ties }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import MainMenuFormScript from "@/scripts/MainMenuFormScript.js";
export default MainMenuFormScript;
</script>
