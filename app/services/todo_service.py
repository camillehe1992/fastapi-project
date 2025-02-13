from typing import List, Dict, Any

from schemas.todo import TodoList
from core.api_client import ApiClient


class TodoService:
    def __init__(self, client: ApiClient):
        self.client = client
        pass

    def get_all(self, page: int = 1, page_limit: int = 15) -> Dict[str, Any]:
        todos = self.client.get(endpoint=f"/todos?_page={page}&_limit={page_limit}")
        return TodoList(page=page, page_size=page_limit, todos=todos)
