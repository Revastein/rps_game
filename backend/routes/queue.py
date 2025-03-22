import json
from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException

from backend.manager.user_manager import user_manager
from backend.manager.lobby_manager import lobby_manager
from backend.models.database import Session, UserOrm
from backend.models.schemas import Queue
from backend.routes.websocket import manager as ws_manager
from backend.secure.auth import get_current_user

router = APIRouter(tags=["Queue"], dependencies=[Depends(get_current_user)])


@router.post("/join_queue", response_model=Queue, status_code=201)
async def join_queue(game_queue: Annotated[Queue, Depends()]):
    async with Session() as session:
        user = await session.get(UserOrm, game_queue.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

    if lobby_manager.is_user_in_queue(game_queue.user_id):
        raise HTTPException(status_code=400, detail="User already in the queue")
    if lobby_manager.is_user_in_lobby(game_queue.user_id):
        raise HTTPException(status_code=400, detail="User already in a lobby")

    lobby_manager.add_to_queue(game_queue.user_id)
    await user_manager.update_status(game_queue.user_id, "in_queue")

    await ws_manager.broadcast(json.dumps({
        "event": "queue_update",
        "queue": [q.user_id for q in lobby_manager.queue]
    }))

    return game_queue


@router.get("/get_queue", response_model=List[Queue], status_code=200)
async def get_queue():
    return lobby_manager.queue


@router.delete("/delete_user_from_queue", response_model=dict, status_code=200)
async def delete_user_from_queue(game_queue: Annotated[Queue, Depends()]):
    if lobby_manager.remove_user_from_queue(game_queue.user_id):
        await ws_manager.broadcast(json.dumps({
            "event": "queue_update",
            "queue": [q.user_id for q in lobby_manager.queue]
        }))
        return {"message": "Successfully left the queue"}
    return {"message": "User not found in the queue"}
