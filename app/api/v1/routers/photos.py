from fastapi import APIRouter

router = APIRouter()


@router.get("/photos/")
async def read_photos():
    return [{"photo_id": "TODO"}, {"photo_id": "TODO"}]
