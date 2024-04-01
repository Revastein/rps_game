from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password: str


class User(UserBase):
    user_id: int
    rating: int = 0
    games_played: int = 0
    wins: int = 0
    losses: int = 0
    ties: int = 0


class UserId(BaseModel):
    user_id: int


class UserStatUpdate(UserId):
    rating: Optional[int] = None
    games_played: Optional[int] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    ties: Optional[int] = None


class UserAuthUpdate(UserId):
    username: Optional[str] = None
    password: str


class Queue(BaseModel):
    user_id: int


class GameResult(BaseModel):
    winner: str


class LobbyPlayer(BaseModel):
    user_id: int
    choice: str = None


class Lobby(BaseModel):
    lobby_id: str
    players: List[LobbyPlayer]
    rematch_accepted: List[int] = []
