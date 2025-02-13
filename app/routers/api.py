from fastapi import APIRouter
from routers.v1 import root, items, todos, users


router = APIRouter(prefix="/api/v1")

# Register Routers
router.include_router(root.router)
router.include_router(items.router)
router.include_router(todos.router)
router.include_router(users.router)
