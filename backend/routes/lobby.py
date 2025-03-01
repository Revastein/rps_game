from typing import List

from fastapi import APIRouter, HTTPException

from backend.manager.lobby_manager import lobby_manager
from backend.models.database import Session, UserOrm
from backend.models.schemas import GameResult, Lobby
from backend.service.lobby_service import LobbyView

router = APIRouter(prefix="/v1", tags=["Lobby"])


@router.get("/get_all_lobbies", response_model=List[Lobby], status_code=200)
async def get_all_lobbies():
    return lobby_manager.lobbies


@router.get("/get_lobby/{lobby_id}", response_model=Lobby, status_code=200)
async def get_lobby(lobby_id: str):
    lobby = lobby_manager.get_lobby(lobby_id)
    if lobby:
        return lobby
    raise HTTPException(status_code=404, detail="Lobby not found")


@router.post("/make_choice/{lobby_id}", response_model=GameResult, status_code=200)
async def make_choice(lobby_id: str, current_user_id: int, choice: str) -> dict:
    valid_choices = ["rock", "paper", "scissors"]
    if choice not in valid_choices:
        raise HTTPException(
            status_code=400,
            detail="Invalid choice. Must be 'rock', 'paper', or 'scissors'.",
        )

    lobby = lobby_manager.get_lobby(lobby_id)
    if not lobby:
        return {"winner": "waiting"}

    lobby_manager.set_player_choice(lobby, current_user_id, choice)

    if lobby_manager.is_lobby_ready(lobby):
        player1_choice = lobby.players[0].choice
        player2_choice = lobby.players[1].choice
        result = LobbyView.determine_winner(
            player1_choice,
            player2_choice,
            lobby.players[0].user_id,
            lobby.players[1].user_id,
        )
        if result == "tie":
            await LobbyView.update_player_stats(
                lobby.players[0].user_id, result, lobby.players[1].user_id
            )
            return {"winner": "tie"}
        else:
            winner_id = int(result)
            loser_id = (
                lobby.players[1].user_id
                if winner_id == lobby.players[0].user_id
                else lobby.players[0].user_id
            )
            await LobbyView.update_player_stats(winner_id, "win", loser_id)
            async with Session() as session:
                winner = await session.get(UserOrm, winner_id)
                if not winner:
                    raise HTTPException(status_code=404, detail="Winner not found")

            lobby.winner_id = winner_id
            lobby.winner_username = winner.username

            return {"winner_id": winner_id, "login": winner.username}
    return {"winner": "waiting"}


@router.post(
    "/surrender_game/{lobby_id}/{player_id}", response_model=GameResult, status_code=200
)
async def surrender_game(lobby_id: str, player_id: int):
    lobby = lobby_manager.get_lobby(lobby_id)
    if not lobby:
        raise HTTPException(status_code=404, detail="Lobby not found")
    if player_id not in [player.user_id for player in lobby.players]:
        raise HTTPException(status_code=404, detail="Player not found in lobby")
    opponent_ids = [p.user_id for p in lobby.players if p.user_id != player_id]
    if not opponent_ids:
        raise HTTPException(status_code=400, detail="No opponent found")
    opponent_id = opponent_ids[0]
    await LobbyView.update_player_stats_on_surrender(player_id, opponent_id)
    return {"winner": str(opponent_id)}


@router.get("/check_winner/{lobby_id}", response_model=GameResult, status_code=200)
async def check_winner(lobby_id: str) -> dict:
    lobby = lobby_manager.get_lobby(lobby_id)
    if not lobby:
        raise HTTPException(status_code=404, detail="Lobby not found")
    if lobby_manager.is_lobby_ready(lobby):
        player1_choice = lobby.players[0].choice
        player2_choice = lobby.players[1].choice
        result = LobbyView.determine_winner(
            player1_choice,
            player2_choice,
            lobby.players[0].user_id,
            lobby.players[1].user_id,
        )
        return {"winner": result}
    return {"winner": "waiting"}


@router.post("/confirm_rematch/{lobby_id}/{player_id}", response_model=None, status_code=200)
async def confirm_rematch(lobby_id: str, player_id: int, rematch_accepted: bool):
    lobby = lobby_manager.get_lobby(lobby_id)
    if not lobby:
        raise HTTPException(status_code=404, detail="Lobby not found")
    if player_id not in [player.user_id for player in lobby.players]:
        raise HTTPException(status_code=404, detail="Player not found in lobby")
    if rematch_accepted:
        if player_id not in lobby.rematch_accepted:
            lobby.rematch_accepted.append(player_id)
    else:
        if player_id in lobby.rematch_accepted:
            lobby.rematch_accepted.remove(player_id)
    if len(lobby.rematch_accepted) == len(lobby.players):
        await restart_lobby(lobby_id)
    return


@router.post("/restart_lobby/{lobby_id}", response_model=Lobby, status_code=200)
async def restart_lobby(lobby_id: str):
    lobby = lobby_manager.get_lobby(lobby_id)
    if not lobby:
        raise HTTPException(status_code=404, detail="Lobby not found")
    for player in lobby.players:
        player.choice = None
    lobby.rematch_accepted = []
    return lobby


@router.delete("/delete_lobby/{lobby_id}", response_model=dict, status_code=200)
async def delete_lobby(lobby_id: str):
    if lobby_manager.remove_lobby(lobby_id):
        return {"message": "Lobby successfully deleted"}
    return {"message": "Lobby not found"}
