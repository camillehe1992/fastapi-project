from fastapi import APIRouter

router = APIRouter()


@router.get("/posts/")
async def read_posts():
    return [{"post_id": "Post1"}, {"post_id": "Post2"}]
