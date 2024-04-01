import os
import string
import random
import asyncio
import pytest
from main import app
from fastapi.testclient import TestClient
from models.database import create_tables


@pytest.fixture(scope='session', autouse=True)
def teardown():
    asyncio.run(create_tables())
    yield
    os.remove('rps_arena.db')


client = TestClient(app)

username = ''.join(random.choices(string.ascii_letters, k=8))
password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

mock_queue = []
mock_lobbies = []


def add_user(count: int = 1):
    for i in range(1, count + 1):
        username = ''.join(random.choices(string.ascii_letters, k=8))
        user_data = {"username": username, "password": password}
        client.post("/register", json=user_data)


def add_user_to_queue(count: int = 1):
    for i in range(1, count + 1):
        client.post("/join_queue", json={"user_id": i})


def get_lobby_id(user_id: int = 1):
    response = client.get(f"/get_lobby_id_by_user/{user_id}")
    lobby_id = response.json()
    return lobby_id


def tie_result(lobby_id: int):
    client.post(f"/make_choice/{lobby_id}?current_user_id=1&choice=rock")
    client.post(f"/make_choice/{lobby_id}?current_user_id=2&choice=rock")
