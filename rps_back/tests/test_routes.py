from config import *
from unittest.mock import patch


class TestUsers:

    def test_create_user(self):
        user_data = {"username": username, "password": password}
        response = client.post("/register", json=user_data)
        assert response.status_code == 201
        assert "user_id" in response.json()

    def test_login_user(self):
        user_data = {"username": username, "password": password}
        response = client.post("/login", json=user_data)
        assert response.status_code == 200
        assert "user_id" in response.json()

    def test_get_user(self):
        user_id = 1
        response = client.get(f"/user/{user_id}")
        assert response.status_code == 200
        assert "username" in response.json()

    def test_get_users(self):
        response = client.get("/users/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_update_user_stat(self):
        response = client.patch(f"/update_stat/?user_id=1&rating=99999")
        assert response.status_code == 204

    def test_update_user_auth_data(self):
        response = client.patch("/update_auth/?user_id=1&password=cool_password", json={})
        assert response.status_code == 204


class TestQueue:

    @patch('routes.lobby.queue', mock_queue)
    def test_join_queue(self):
        response = client.post("/join_queue", json={"user_id": 1})
        assert response.status_code == 201
        assert len(mock_queue) == 1
        assert mock_queue[0].user_id == 1

    @patch('routes.lobby.queue', mock_queue)
    def test_get_queue(self):
        response = client.get("/get_queue")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @patch('routes.lobby.queue', mock_queue)
    def test_delete_user_from_queue(self):
        response = client.request("DELETE", "/delete_user_from_queue", json={"user_id": 1})
        assert response.status_code == 204


class TestLobby:

    @patch('routes.lobby.lobbies', mock_lobbies)
    def test_get_lobby_by_user(self):
        add_user(2)
        add_user_to_queue(2)
        user_id = 1
        response = client.get(f"/get_lobby_by_user/{user_id}")
        assert response.status_code == 200

    @patch('routes.lobby.lobbies', mock_lobbies)
    def test_get_lobby_id_by_user(self):
        user_id = 1
        response = client.get(f"/get_lobby_id_by_user/{user_id}")
        assert response.status_code == 200
        lobby_id = response.json()
        assert isinstance(lobby_id, str)
        assert lobby_id

    @patch('routes.lobby.lobbies', mock_lobbies)
    def test_get_all_lobbies(self):
        response = client.get("/get_all_lobbies")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @patch('routes.lobby.lobbies', mock_lobbies)
    def test_get_lobby(self):
        lobby_id = get_lobby_id()
        response = client.get(f"/get_lobby/{lobby_id}")
        assert response.status_code == 200

    @patch('routes.lobby.lobbies', mock_lobbies)
    def test_make_choice(self):
        lobby_id = get_lobby_id()
        user_id = 1
        user_choice = "rock"
        response = client.post(f"/make_choice/{lobby_id}?current_user_id={user_id}&choice={user_choice}")
        assert response.status_code == 200

    @patch('routes.lobby.lobbies', mock_lobbies)
    def test_check_winner(self):
        lobby_id = get_lobby_id()
        tie_result(lobby_id)
        response = client.get(f"/check_winner/{lobby_id}")
        assert response.status_code == 200

    @patch('routes.lobby.lobbies', mock_lobbies)
    def test_surrender_game(self):
        lobby_id = get_lobby_id()
        response = client.post(f"/surrender_game/{lobby_id}/1")
        assert response.status_code == 200

    @patch('routes.lobby.lobbies', mock_lobbies)
    def test_confirm_rematch(self):
        lobby_id = get_lobby_id()
        player_id = 1
        response = client.post(f"/confirm_rematch/{lobby_id}/{player_id}?rematch_accepted=True")
        assert response.status_code == 200

    @patch('routes.lobby.lobbies', mock_lobbies)
    def test_restart_lobby(self):
        lobby_id = get_lobby_id()
        response = client.post(f"/restart_lobby/{lobby_id}")
        assert response.status_code == 200

    @patch('routes.lobby.lobbies', mock_lobbies)
    def test_delete_lobby(self):
        lobby_id = get_lobby_id()
        response = client.delete(f"/delete_lobby/{lobby_id}")
        assert response.status_code == 204
