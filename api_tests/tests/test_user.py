import pytest
from api_tests.utils.api_client import APIClient
from api_tests.utils.data_factory import UserFactory

class TestUserEndpoints:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.user_data = UserFactory.create_user()

    def _create_user(self):
        return self.client.post("/user", json=self.user_data)

    def test_create_user(self):
        response = self._create_user()
        assert response.status_code == 200

    def test_create_users_with_list(self):
        users = [UserFactory.create_user() for _ in range(3)]
        response = self.client.post("/user/createWithList", json=users)
        assert response.status_code == 200

    def test_create_users_with_array(self):
        users = [UserFactory.create_user() for _ in range(2)]
        response = self.client.post("/user/createWithArray", json=users)
        assert response.status_code == 200

    def test_get_user_by_username(self):
        self._create_user()
        response = self.client.get(f"/user/{self.user_data['username']}")
        assert response.status_code == 200
        assert response.json()["username"] == self.user_data["username"]

    def test_get_user_not_found(self):
        response = self.client.get("/user/usuario_que_nao_existe_xpto123")
        assert response.status_code == 404

    def test_get_user_returns_correct_fields(self):
        self._create_user()
        response = self.client.get(f"/user/{self.user_data['username']}")
        body = response.json()
        for field in ("id", "username", "email"):
            assert field in body

    def test_user_login(self):
        self._create_user()
        response = self.client.get("/user/login", params={
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        })
        assert response.status_code == 200
        assert "logged in" in response.json().get("message", "").lower()

    def test_user_logout(self):
        response = self.client.get("/user/logout")
        assert response.status_code == 200

    def test_update_user(self):
        self._create_user()
        updated = {**self.user_data, "firstName": "NovoNome", "email": "novo@email.com"}
        response = self.client.put(f"/user/{self.user_data['username']}", json=updated)
        assert response.status_code == 200

    def test_delete_user(self):
        self._create_user()
        delete_resp = self.client.delete(f"/user/{self.user_data['username']}")
        assert delete_resp.status_code == 200
        get_resp = self.client.get(f"/user/{self.user_data['username']}")
        assert get_resp.status_code == 404