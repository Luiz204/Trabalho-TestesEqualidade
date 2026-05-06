import pytest
from api_tests.utils.api_client import APIClient
from api_tests.utils.data_factory import OrderFactory, PetFactory

class TestStoreEndpoints:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.pet = PetFactory.create_pet()
        self.client.post("/pet", json=self.pet)
        self.order_data = OrderFactory.create_order(pet_id=self.pet["id"])

    def test_get_inventory(self):
        response = self.client.get("/store/inventory")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_inventory_contains_known_statuses(self):
        response = self.client.get("/store/inventory")
        body = response.json()
        known = {"available", "pending", "sold"}
        assert known & set(body.keys())

    def test_place_order(self):
        response = self.client.post("/store/order", json=self.order_data)
        assert response.status_code == 200
        body = response.json()
        assert body["id"] == self.order_data["id"]
        assert body["petId"] == self.order_data["petId"]

    def test_place_order_returns_complete_body(self):
        response = self.client.post("/store/order", json=self.order_data)
        body = response.json()
        for field in ("id", "petId", "quantity", "status"):
            assert field in body

    def test_get_order_by_id(self):
        self.client.post("/store/order", json=self.order_data)
        response = self.client.get(f"/store/order/{self.order_data['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == self.order_data["id"]

    def test_get_order_not_found(self):
        response = self.client.get("/store/order/999999999")
        assert response.status_code == 404

    def test_delete_order(self):
        self.client.post("/store/order", json=self.order_data)
        delete_resp = self.client.delete(f"/store/order/{self.order_data['id']}")
        assert delete_resp.status_code == 200
        get_resp = self.client.get(f"/store/order/{self.order_data['id']}")
        assert get_resp.status_code == 404

    def test_delete_order_not_found(self):
        response = self.client.delete("/store/order/999999999")
        assert response.status_code == 404