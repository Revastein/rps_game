import uuid
from typing import List, Optional

from backend.models.schemas import Queue, Lobby, LobbyPlayer


class LobbyManager:
    def __init__(self):
        self.queue: List[Queue] = []
        self.lobbies: List[Lobby] = []

    def is_user_in_queue(self, user_id: int) -> bool:
        return any(user.user_id == user_id for user in self.queue)

    def is_user_in_lobby(self, user_id: int) -> bool:
        return any(
            user_id in [player.user_id for player in lobby.players]
            for lobby in self.lobbies
        )

    def add_to_queue(self, user_id: int) -> None:
        self.queue.append(Queue(user_id=user_id))

    def remove_user_from_queue(self, user_id: int) -> bool:
        for user in self.queue:
            if user.user_id == user_id:
                self.queue.remove(user)
                return True
        return False

    def get_lobby(self, lobby_id: str) -> Optional[Lobby]:
        for lobby in self.lobbies:
            if lobby.lobby_id == lobby_id:
                return lobby
        return None

    def set_player_choice(self, lobby: Lobby, user_id: int, choice: str) -> None:
        for player in lobby.players:
            if player.user_id == user_id:
                player.choice = choice
                break

    def is_lobby_ready(self, lobby: Lobby) -> bool:
        return all(player.choice is not None for player in lobby.players)

    def create_lobby_from_queue(self) -> Optional[Lobby]:
        if len(self.queue) >= 2:
            lobby_players = [
                LobbyPlayer(user_id=user.user_id) for user in self.queue[:2]
            ]
            lobby_id = str(uuid.uuid4())
            new_lobby = Lobby(lobby_id=lobby_id, players=lobby_players)
            self.lobbies.append(new_lobby)
            del self.queue[:2]
            return new_lobby
        return None

    def remove_lobby(self, lobby_id: str) -> bool:
        for lobby in self.lobbies:
            if lobby.lobby_id == lobby_id:
                self.lobbies.remove(lobby)
                return True
        return False


lobby_manager = LobbyManager()
