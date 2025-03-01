from fastapi import HTTPException

from backend.manager.lobby_manager import lobby_manager
from backend.models.database import Session, UserOrm


class LobbyView:
    @classmethod
    async def check_queue(cls):
        lobby_manager.create_lobby_from_queue()

    @classmethod
    def determine_winner(
        cls, player1_choice: str, player2_choice: str, player1_id: int, player2_id: int
    ) -> str:
        if player1_choice == player2_choice:
            return "tie"
        elif (
            (player1_choice == "rock" and player2_choice == "scissors")
            or (player1_choice == "scissors" and player2_choice == "paper")
            or (player1_choice == "paper" and player2_choice == "rock")
        ):
            return str(player1_id)
        else:
            return str(player2_id)

    @classmethod
    async def update_player_stats(
        cls, user_id: int, result: str, opponent_id: int
    ) -> None:
        async with Session() as session:
            player = await session.get(UserOrm, user_id)
            if not player:
                raise HTTPException(status_code=404, detail="Player not found")

            opponent = await session.get(UserOrm, opponent_id)
            if not opponent:
                raise HTTPException(status_code=404, detail="Opponent not found")

            if result == "tie":
                player.ties += 1
                opponent.ties += 1
            else:
                player.rating += 5
                player.wins += 1
                opponent.losses += 1

            player.games_played += 1
            opponent.games_played += 1

            await session.commit()

    @classmethod
    async def update_player_stats_on_surrender(
        cls, player_id: int, opponent_id: int
    ) -> None:
        async with Session() as session:
            player = await session.get(UserOrm, player_id)
            opponent = await session.get(UserOrm, opponent_id)
            if not player or not opponent:
                raise HTTPException(
                    status_code=404, detail="Player or opponent not found"
                )

            player.wins += 1
            player.rating += 5
            player.games_played += 1
            opponent.losses += 1
            opponent.games_played += 1

            await session.commit()
