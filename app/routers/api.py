from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from routers.v1 import root, items, todos, users


router = APIRouter(prefix="/api/v1")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Register Routers
router.include_router(root.router)
router.include_router(items.router)
# router.include_router(items.router, dependencies=[Depends(oauth2_scheme)])
router.include_router(todos.router)
router.include_router(users.router)
