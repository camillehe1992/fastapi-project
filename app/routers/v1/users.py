from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.auth import get_current_user
from db.base import get_db
from schemas.user import UserIn, UserLogin, UserRegister, UserInDBBase, Token, UserBase
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserInDBBase
)
def register(data: UserRegister, session: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        data (UserIn): Details of the user to be registered.
        session (Session): Database session.

    Returns:
        UserInDBBase: Details of the registered user.
    """
    _service = UserService(session)
    return _service.create(data)


@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=Token)
def login(data: UserLogin, session: Session = Depends(get_db)):
    """
    Login user.

    Args:
        data (UserLogin): Login data with username and password.
        session (Session): Database session.

    Returns:
        None
    """
    _service = UserService(session)
    return _service.login(data)


@router.get(
    "/me", status_code=status.HTTP_200_OK, response_model=UserBase, deprecated=True
)
def get_me(user: UserIn = Depends(get_current_user)):
    """
    Retrieve information of the authenticated user.

    Args:
        user (UserIn): Current user's details.

    Returns:
        UserIn: Details of the authenticated user.
    """
    return user


@router.delete("/me", status_code=status.HTTP_200_OK, deprecated=True)
def delete_me(
    user: UserIn = Depends(get_current_user), session: Session = Depends(get_db)
):
    """
    Delete the authenticated user.

    Args:
        user (UserIn): Current user's details.
        session (Session): Database session.

    Returns:
        None
    """
    _service = UserService(session)
    return _service.delete_user(user.id)
