from fastapi import APIRouter

router = APIRouter()


@router.get("/todos/")
async def read_todos():
    return [{"todo_id": "Foo"}, {"todo_id": "Bar"}]
