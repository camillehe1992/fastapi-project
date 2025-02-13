from fastapi import APIRouter

router = APIRouter()


@router.get("/albums/")
async def read_albums():
    return [{"album_id": "TODO"}, {"album_id": "TODO"}]
