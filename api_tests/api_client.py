import requests

BASE_URL = "https://petstore.swagger.io/v2"

class APIClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def get(self, path, **kwargs):
        return self.session.get(self._url(path), **kwargs)

    def post(self, path, **kwargs):
        return self.session.post(self._url(path), **kwargs)

    def put(self, path, **kwargs):
        return self.session.put(self._url(path), **kwargs)

    def delete(self, path, **kwargs):
        return self.session.delete(self._url(path), **kwargs)