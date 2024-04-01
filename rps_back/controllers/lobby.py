import uuid
from fastapi import HTTPException

from models.database import Session, UserOrm
from models.schemas import Lobby, LobbyPlayer


class LobbyView:
    @classmethod
    async def check_queue(cls, queue, lobbies):
        if len(queue) >= 2:
            lobby_players = [LobbyPlayer(user_id=user.user_id) for user in queue[:2]]
            lobby_id = str(uuid.uuid4())
            lobby = Lobby(lobby_id=lobby_id, players=lobby_players)
            lobbies.append(lobby)
            del queue[:2]

    @classmethod
    def determine_winner(cls, choice1: str, choice2: str) -> str:
        if choice1 == choice2:
            return "tie"
        elif (choice1 == "rock" and choice2 == "scissors") or \
                (choice1 == "scissors" and choice2 == "paper") or \
                (choice1 == "paper" and choice2 == "rock"):
            return "player1"
        else:
            return "player2"

    @classmethod
    async def update_player_stats(cls, user_id: int, result: str, opponent_id: int) -> None:
        async with Session() as session:
            player = await session.get(UserOrm, user_id)
            if not player:
                raise HTTPException(status_code=404, detail="Player not found")

            if result == "player1":
                player.rating += 5
                player.wins += 1
                opponent = await session.get(UserOrm, opponent_id)
                opponent.losses += 1
            elif result == "player2":
                player.rating += 5
                player.wins += 1
                opponent = await session.get(UserOrm, opponent_id)
                opponent.losses += 1
            else:
                player.ties += 1
                opponent = await session.get(UserOrm, opponent_id)
                opponent.ties += 1

            player.games_played += 1
            opponent.games_played += 1

            await session.commit()

    @classmethod
    async def update_player_stats_on_surrender(cls, player_id: int, opponent_id: int) -> None:
        async with Session() as session:
            player = await session.get(UserOrm, player_id)
            opponent = await session.get(UserOrm, opponent_id)
            if not player or not opponent:
                raise HTTPException(status_code=404, detail="Player or opponent not found")

            player.wins += 1
            player.rating += 5
            player.games_played += 1
            opponent.losses += 1
            opponent.games_played += 1

            await session.commit()
