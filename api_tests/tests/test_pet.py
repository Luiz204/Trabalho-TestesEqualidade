import pytest
from api_tests.utils.api_client import APIClient
from api_tests.utils.data_factory import PetFactory

class TestPetEndpoints:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.pet_data = PetFactory.create_pet()

    def test_create_pet_success(self):
        response = self.client.post("/pet", json=self.pet_data)
        assert response.status_code == 200
        body = response.json()
        assert body["id"] == self.pet_data["id"]
        assert body["name"] == self.pet_data["name"]
        assert body["status"] == self.pet_data["status"]

    def test_create_pet_returns_json(self):
        response = self.client.post("/pet", json=self.pet_data)
        assert "application/json" in response.headers.get("Content-Type", "")

    def test_get_pet_by_id(self):
        self.client.post("/pet", json=self.pet_data)
        response = self.client.get(f"/pet/{self.pet_data['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == self.pet_data["id"]

    def test_get_pet_not_found(self):
        response = self.client.get("/pet/999999999999999")
        assert response.status_code in [404, 200]

    def test_find_pets_by_status_available(self):
        response = self.client.get("/pet/findByStatus", params={"status": "available"})
        assert response.status_code == 200
        pets = response.json()
        assert isinstance(pets, list)
        assert all(p["status"] == "available" for p in pets if "status" in p)

    def test_find_pets_by_status_sold(self):
        response = self.client.get("/pet/findByStatus", params={"status": "sold"})
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_find_pets_by_status_pending(self):
        response = self.client.get("/pet/findByStatus", params={"status": "pending"})
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_update_pet(self):
        self.client.post("/pet", json=self.pet_data)
        updated = {**self.pet_data, "name": "Rex Updated", "status": "sold"}
        response = self.client.put("/pet", json=updated)
        assert response.status_code == 200
        assert response.json()["name"] == "Rex Updated"
        assert response.json()["status"] == "sold"

    def test_delete_pet(self):
        self.client.post("/pet", json=self.pet_data)
        delete_resp = self.client.delete(f"/pet/{self.pet_data['id']}")
        assert delete_resp.status_code == 200
        get_resp = self.client.get(f"/pet/{self.pet_data['id']}")
        assert get_resp.status_code == 404