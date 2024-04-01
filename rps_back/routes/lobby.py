from typing import List
from controllers.lobby import LobbyView
from models.database import Session, UserOrm
from fastapi import APIRouter, HTTPException
from models.schemas import Queue, GameResult, Lobby

router = APIRouter(tags=["Lobby"])

queue = []
lobbies = []


@router.post("/join_queue", response_model=Queue, status_code=201)
async def join_queue(game_queue: Queue):
    async with Session() as session:
        user = await session.get(UserOrm, game_queue.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    for user in queue:
        if user.user_id == game_queue.user_id:
            raise HTTPException(status_code=400, detail="User already in the queue")
    for lobby in lobbies:
        for player in lobby.players:
            if player.user_id == game_queue.user_id:
                raise HTTPException(status_code=400, detail="User already in a lobby")

    user_to_queue = Queue(user_id=game_queue.user_id)
    queue.append(user_to_queue)
    await LobbyView.check_queue(queue, lobbies)
    return user_to_queue


@router.get("/get_queue", response_model=List[Queue], status_code=200)
async def get_queue():
    return queue


@router.delete("/delete_user_from_queue", response_model=None, status_code=204)
async def delete_user_from_queue(game_queue: Queue):
    for user in queue:
        if user.user_id == game_queue.user_id:
            queue.remove(user)
            return {"message": "Successfully left the queue"}
    return {"message": "User not found in the queue"}


@router.get("/get_all_lobbies", response_model=List[Lobby], status_code=200)
async def get_all_lobbies():
    return lobbies


@router.get("/get_lobby_id_by_user/{user_id}", response_model=str, status_code=200)
async def get_lobby_id_by_user(user_id: int):
    for lobby in lobbies:
        for player in lobby.players:
            if player.user_id == user_id:
                return lobby.lobby_id
    raise HTTPException(status_code=404, detail="Lobby not found for this user")


@router.get("/get_lobby/{lobby_id}", response_model=Lobby, status_code=200)
async def get_lobby(lobby_id: str):
    for lobby in lobbies:
        if lobby.lobby_id == lobby_id:
            return lobby
    raise HTTPException(status_code=404, detail="Lobby not found")


@router.get("/get_lobby_by_user/{user_id}", response_model=Lobby, status_code=200)
async def get_lobby_by_user(user_id: int):
    for lobby in lobbies:
        for player in lobby.players:
            if player.user_id == user_id:
                return lobby
    raise HTTPException(status_code=404, detail="Lobby not found for this user")


@router.post("/make_choice/{lobby_id}", response_model=GameResult, status_code=200)
async def make_choice(lobby_id: str, current_user_id: int, choice: str) -> dict:
    valid_choices = ["rock", "paper", "scissors"]
    if choice not in valid_choices:
        raise HTTPException(status_code=400, detail="Invalid choice. Must be 'rock', 'paper', or 'scissors'.")

    for lobby in lobbies:
        if lobby.lobby_id == lobby_id:
            for player in lobby.players:
                if player.user_id == current_user_id:
                    player.choice = choice
            break
    else:
        return {"winner": "waiting"}

    if all(player.choice is not None for player in lobby.players):
        player1_choice = lobby.players[0].choice
        player2_choice = lobby.players[1].choice
        result = LobbyView.determine_winner(player1_choice, player2_choice)
        if result != "waiting":
            if result == "tie":
                await LobbyView.update_player_stats(lobby.players[0].user_id, result, lobby.players[1].user_id)
            else:
                winner_id = lobby.players[0].user_id if result == "player1" else lobby.players[1].user_id
                loser_id = lobby.players[1].user_id if result == "player1" else lobby.players[0].user_id
                await LobbyView.update_player_stats(winner_id, result, loser_id)
        return {"winner": result}
    return {"winner": "waiting"}


@router.post("/surrender_game/{lobby_id}/{player_id}", response_model=GameResult, status_code=200)
async def surrender_game(lobby_id: str, player_id: int):
    for lobby in lobbies:
        if lobby.lobby_id == lobby_id:
            for player in lobby.players:
                if player.user_id == player_id:
                    opponent_id = [p.user_id for p in lobby.players if p.user_id != player_id][0]
                    await LobbyView.update_player_stats_on_surrender(player_id, opponent_id)
                    return {"winner": str(opponent_id)}
    raise HTTPException(status_code=404, detail="Lobby or player not found")


@router.get("/check_winner/{lobby_id}", response_model=GameResult, status_code=200)
async def check_winner(lobby_id: str) -> dict:
    for lobby in lobbies:
        if lobby.lobby_id == lobby_id:
            if all(player.choice is not None for player in lobby.players):
                player1_choice = lobby.players[0].choice
                player2_choice = lobby.players[1].choice
                result = LobbyView.determine_winner(player1_choice, player2_choice)
                if result != "waiting":
                    return {"winner": result}
                else:
                    return {"winner": "waiting"}
    raise HTTPException(status_code=404, detail="Lobby not found")


@router.post("/confirm_rematch/{lobby_id}/{player_id}", response_model=None, status_code=200)
async def confirm_rematch(lobby_id: str, player_id: int, rematch_accepted: bool):
    for lobby in lobbies:
        if lobby.lobby_id == lobby_id:
            if player_id in [player.user_id for player in lobby.players]:
                if rematch_accepted:
                    if player_id not in lobby.rematch_accepted:
                        lobby.rematch_accepted.append(player_id)
                else:
                    if player_id in lobby.rematch_accepted:
                        lobby.rematch_accepted.remove(player_id)
                if len(lobby.rematch_accepted) == 2:
                    await restart_lobby(lobby_id)
                return
    raise HTTPException(status_code=404, detail="Lobby or player not found")


@router.post("/restart_lobby/{lobby_id}", response_model=Lobby, status_code=200)
async def restart_lobby(lobby_id: str):
    for lobby in lobbies:
        if lobby.lobby_id == lobby_id:
            for player in lobby.players:
                player.choice = None
            lobby.rematch_accepted = []
            return lobby
    raise HTTPException(status_code=404, detail="Lobby not found")


@router.delete("/delete_lobby/{lobby_id}", response_model=None, status_code=204)
async def delete_lobby(lobby_id: str):
    for lobby in lobbies:
        if lobby.lobby_id == lobby_id:
            lobbies.remove(lobby)
            return {"message": "Lobby successfully deleted"}
    return {"message": "Lobby not found"}
