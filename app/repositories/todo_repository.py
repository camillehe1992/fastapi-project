from schemas.todo import TodoList

from core.api_client import ApiClient


class ItemRepository:
    def __init__(self, client: ApiClient):
        self.client = client
        pass

    def get_all(self, offset: int = 1, page_limit: int = 15) -> TodoList:
        return self.client.get(endpoint=f"/todos?_page=2&_limit=5")
