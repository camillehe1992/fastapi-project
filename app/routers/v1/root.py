from fastapi import APIRouter

from config.settings import settings
from utils.datetime_helper import DateTimeHelper

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/health", status_code=200)
def health():
    return {"status": "ok"}


@router.get("/info", status_code=200)
def info():
    helper = DateTimeHelper()
    current_time = helper.now()
    return {
        "nickname": settings.NICKNAME,
        "version": settings.VERSION,
        "iso_time": helper.iso_format(current_time),
    }
