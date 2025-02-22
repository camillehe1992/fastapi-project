from typing import Dict, Any
from datetime import timedelta, datetime

from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from utils.datetime_helper import DateTimeHelper
from core.security import get_password_hash, pwd_context, create_access_token
from settings import settings
from repositories.user_repository import UserRepository
from schemas.user import UserRegister, UserLogin, UserInDBBase
from core.password_validator import validate_password
from core.email_validator import validate_email


class UserService:
    """
    Service class for handling user-related operations.
    """

    def __init__(self, session: Session):
        """
        Initialize the service.

        Args:
            session (Session): Database session.
        """
        self.repository = UserRepository(session)

    def create(self, data: UserRegister) -> UserInDBBase:
        """
        Create a new user.

        Args:
            data (UserRegister): User data.

        Returns:
            UserInDBBase: Created user data.
        """
        if self.repository.user_exists_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {data.email} already registered",
            )
        if self.repository.user_exists_by_username(data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username {data.username} already registered",
            )

        validate_password(data.password)
        validate_email(data.email)

        hashed_password = get_password_hash(data.password)
        user = self.repository.create(data, hashed_password)
        return UserInDBBase(**user.as_dict())

    def login(self, data: UserLogin) -> Dict[str, Any]:
        """
        User login.

        Args:
            data (UserLogin): Login data with email and password.

        Returns:
            dict: Token response.
        """
        user = self.repository.get_user_by_email(data.email)
        if not user or not pwd_context.verify(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        datetime_helper = DateTimeHelper()
        expired_at_datetime = datetime_helper.now() + access_token_expires
        expired_at = datetime_helper.format(expired_at_datetime)

        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expired_at": expired_at,
        }

    def is_superuser(self, _id: UUID4) -> bool:
        """
        Check if the user is a superuser.

        Args:
            _id (UUID4): User ID.

        Returns:
            bool: True if the user is a superuser, False otherwise.
        """
        if not self.repository.user_exists_by_id(_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"User {_id} not found"
            )

        user = self.repository.get_user_object_by_id(_id)
        return user.is_superuser

    def delete_user(self, _id: UUID4) -> bool:
        """
        Delete a user.

        Args:
            _id (UUID4): User ID.

        Returns:
            bool: True if the user is successfully deleted, False otherwise.
        """
        if not self.repository.user_exists_by_id(_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"User {_id} not found"
            )

        user = self.repository.get_user_object_by_id(_id)
        self.repository.delete_user(user)
        return True
