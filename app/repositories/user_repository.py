from typing import Type

from pydantic import UUID4
from sqlalchemy.orm import Session

from db.models import User
from schemas.user import UserIn, UserInDBBase, UserInDB, UserRegister


class UserRepository:
    """
    Repository class for handling users.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.

        Args:
            session (Session): The database session.
        """
        self.session = session

    def create(self, data: UserRegister, hashed_password: str) -> User:
        """
        Create a new user.

        Args:
            data (UserIn): The user data.
            hashed_password (str): The hashed password.

        Returns:
            UserInDBBase: The created user.
        """
        db_user = User(
            **data.model_dump(exclude={"password"}), hashed_password=hashed_password
        )
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def user_exists_by_email(self, email: str) -> bool:
        """
        Check if a user exists by email.

        Args:
            email (str): The email to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        return (
            self.session.query(User)
            .filter(User.email == email, User.is_active == True)
            .first()
            is not None
        )

    def user_exists_by_username(self, username: str) -> bool:
        """
        Check if a user exists by username.

        Args:
            username (str): The username to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        return (
            self.session.query(User)
            .filter(User.username == username, User.is_active == True)
            .first()
            is not None
        )

    def get_user_by_email(self, email: str):
        """
        Get a user by email.

        Args:
            email (str): The email of the user.

        Returns:
            User: The user.
        """
        return (
            self.session.query(User)
            .filter(User.email == email, User.is_active == True)
            .first()
        )

    def get_user_by_username(self, username: str) -> Type[User]:
        """
        Get a user by username.

        Args:
            username (str): The username of the user.

        Returns:
            User: The user.
        """
        return (
            self.session.query(User)
            .filter(User.username == username, User.is_active == True)
            .first()
        )

    def get_user_object_by_id(self, _id: UUID4) -> Type[User]:
        """
        Get a user object by ID.

        Args:
            _id (UUID4): The ID of the user.

        Returns:
            Type[User]: The user instance.
        """
        return (
            self.session.query(User)
            .filter(User.id == _id, User.is_active == True)
            .first()
        )

    def user_exists_by_id(self, _id: UUID4) -> bool:
        """
        Check if a user exists by ID.

        Args:
            _id (UUID4): The ID of the user.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        return (
            self.session.query(User)
            .filter(User.id == _id, User.is_active == True)
            .first()
            is not None
        )

    def inactive_user(self, user: Type[User]) -> bool:
        """
        De-register a user.

        Args:
            user (Type[User]): The user instance.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        user.is_active = False
        self.session.commit()
        self.session.refresh(user)
        return True

    def delete_user(self, user: Type[User]) -> bool:
        """
        Delete a user.

        Args:
            user (Type[User]): The user instance.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        self.session.delete(user)
        self.session.commit()
        return True
