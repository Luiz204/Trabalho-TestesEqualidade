import random
import string
import time

def _unique_id() -> int:
    return int(time.time() * 1000) % 2_147_483_647

def _random_suffix(length: int = 6) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))

class PetFactory:
    @staticmethod
    def create_pet(status: str = "available") -> dict:
        return {
            "id": _unique_id(),
            "category": {"id": 1, "name": "Dogs"},
            "name": f"Rex_{_random_suffix()}",
            "photoUrls": ["https://example.com/photo.jpg"],
            "tags": [{"id": 1, "name": "friendly"}],
            "status": status,
        }

class OrderFactory:
    @staticmethod
    def create_order(pet_id=None) -> dict:
        return {
            "id": _unique_id(),
            "petId": pet_id or _unique_id(),
            "quantity": random.randint(1, 5),
            "shipDate": "2025-06-01T10:00:00.000Z",
            "status": "placed",
            "complete": False,
        }

class UserFactory:
    @staticmethod
    def create_user() -> dict:
        suffix = _random_suffix()
        return {
            "id": _unique_id(),
            "username": f"user_{suffix}",
            "firstName": "Test",
            "lastName": "User",
            "email": f"user_{suffix}@test.com",
            "password": "senha_segura_123",
            "phone": "11999999999",
            "userStatus": 1,
        }