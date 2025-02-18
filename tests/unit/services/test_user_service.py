from datetime import timedelta
from uuid import uuid4
from unittest.mock import patch, Mock
import pytest
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.services.user_service import UserService
from app.schemas.user import UserRegister, UserLogin, UserInDB
from app.core.security import pwd_context
from app.settings import settings


# Mock data
MOCK_USER_ID = uuid4()
MOCK_USERNAME = "testuser"
MOCK_EMAIL = "testuser@example.com"
MOCK_PASSWORD = "securepassword123"
MOCK_HASHED_PASSWORD = pwd_context.hash(MOCK_PASSWORD)

# Mock UserInDB object
MOCK_USER = UserInDB(
    id=MOCK_USER_ID,
    username=MOCK_USERNAME,
    email=MOCK_EMAIL,
    hashed_password=MOCK_HASHED_PASSWORD,
    is_superuser=False,
)

# Mock UserRegister object
MOCK_USER_REGISTER = UserRegister(
    username=MOCK_USERNAME,
    email=MOCK_EMAIL,
    password=MOCK_PASSWORD,
)

# Mock UserLogin object
MOCK_USER_LOGIN = UserLogin(
    username=MOCK_USERNAME,
    password=MOCK_PASSWORD,
)


# Fixture for UserService
@pytest.fixture
def user_service():
    mock_session = Mock(spec=Session)
    return UserService(mock_session)


# Test create method
@patch("app.services.user_service.UserRepository.create")
@patch("app.services.user_service.validate_email")
@patch("app.services.user_service.validate_password")
@patch("app.services.user_service.UserRepository.user_exists_by_username")
@patch("app.services.user_service.UserRepository.user_exists_by_email")
def test_create_user(
    mock_user_exists_by_email,
    mock_user_exists_by_username,
    mock_validate_password,
    mock_validate_email,
    mock_create,
    user_service,
):
    # Mock repository methods
    mock_user_exists_by_email.return_value = False
    mock_user_exists_by_username.return_value = False
    mock_create.return_value = MOCK_USER

    # Call the method
    result = user_service.create(MOCK_USER_REGISTER)

    # Assertions
    assert result == MOCK_USER
    mock_user_exists_by_email.assert_called_once_with(MOCK_EMAIL)
    mock_user_exists_by_username.assert_called_once_with(MOCK_USERNAME)
    mock_validate_password.assert_called_once_with(MOCK_PASSWORD)
    mock_validate_email.assert_called_once_with(MOCK_EMAIL)
    mock_create.assert_called_once()


# Test create method with existing email
@patch("app.services.user_service.UserRepository.user_exists_by_email")
def test_create_user_existing_email(mock_user_exists_by_email, user_service):
    # Mock repository method to return True (email exists)
    mock_user_exists_by_email.return_value = True

    # Call the method and expect an exception
    with pytest.raises(HTTPException) as exc_info:
        user_service.create(MOCK_USER_REGISTER)

    # Assertions
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == f"Email {MOCK_EMAIL} already registered"


# Test create method with existing username
@patch("app.services.user_service.UserRepository.user_exists_by_username")
@patch("app.services.user_service.UserRepository.user_exists_by_email")
def test_create_user_existing_username(
    mock_user_exists_by_email, mock_user_exists_by_username, user_service
):
    # Mock repository methods
    mock_user_exists_by_email.return_value = False
    mock_user_exists_by_username.return_value = True

    # Call the method and expect an exception
    with pytest.raises(HTTPException) as exc_info:
        user_service.create(MOCK_USER_REGISTER)

    # Assertions
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == f"Username {MOCK_USERNAME} already registered"


# Test login method
@patch("app.services.user_service.create_access_token")
@patch("app.services.user_service.pwd_context.verify")
@patch("app.services.user_service.UserRepository.get_user_by_username")
def test_login_user(
    mock_get_user_by_username, mock_pwd_verify, mock_create_access_token, user_service
):
    # Mock repository method to return a user
    mock_get_user_by_username.return_value = MOCK_USER

    # Mock password verification
    mock_pwd_verify.return_value = True

    # Mock token creation
    mock_create_access_token.return_value = "mock_token"

    # Call the method
    result = user_service.login(MOCK_USER_LOGIN)

    # Assertions
    assert result == {"access_token": "mock_token", "token_type": "bearer"}
    mock_get_user_by_username.assert_called_once_with(MOCK_USERNAME)
    mock_pwd_verify.assert_called_once_with(MOCK_PASSWORD, MOCK_HASHED_PASSWORD)
    mock_create_access_token.assert_called_once_with(
        data={"sub": MOCK_USERNAME},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


# Test login method with incorrect username or password
@patch("app.services.user_service.UserRepository.get_user_by_username")
def test_login_user_incorrect_credentials(mock_get_user_by_username, user_service):
    # Mock repository method to return None (user not found)
    mock_get_user_by_username.return_value = None

    # Call the method and expect an exception
    with pytest.raises(HTTPException) as exc_info:
        user_service.login(MOCK_USER_LOGIN)

    # Assertions
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Incorrect username or password"


# Test is_superuser method
@patch("app.services.user_service.UserRepository.get_user_object_by_id")
@patch("app.services.user_service.UserRepository.user_exists_by_id")
def test_is_superuser(mock_user_exists_by_id, mock_get_user_object_by_id, user_service):
    # Mock repository methods
    mock_user_exists_by_id.return_value = True
    mock_get_user_object_by_id.return_value = MOCK_USER

    # Call the method
    result = user_service.is_superuser(MOCK_USER_ID)

    # Assertions
    assert result is False
    mock_user_exists_by_id.assert_called_once_with(MOCK_USER_ID)
    mock_get_user_object_by_id.assert_called_once_with(MOCK_USER_ID)


# Test is_superuser method with non-existent user
@patch("app.services.user_service.UserRepository.user_exists_by_id")
def test_is_superuser_not_found(mock_user_exists_by_id, user_service):
    # Mock repository method to return False (user not found)
    mock_user_exists_by_id.return_value = False

    # Call the method and expect an exception
    with pytest.raises(HTTPException) as exc_info:
        user_service.is_superuser(MOCK_USER_ID)

    # Assertions
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == f"User {MOCK_USER_ID} not found"


# Test delete_user method
@patch("app.services.user_service.UserRepository.delete_user")
@patch("app.services.user_service.UserRepository.get_user_object_by_id")
@patch("app.services.user_service.UserRepository.user_exists_by_id")
def test_delete_user(
    mock_user_exists_by_id, mock_get_user_object_by_id, mock_delete_user, user_service
):
    # Mock repository methods
    mock_user_exists_by_id.return_value = True
    mock_get_user_object_by_id.return_value = MOCK_USER

    # Call the method
    result = user_service.delete_user(MOCK_USER_ID)

    # Assertions
    assert result is True
    mock_user_exists_by_id.assert_called_once_with(MOCK_USER_ID)
    mock_get_user_object_by_id.assert_called_once_with(MOCK_USER_ID)
    mock_delete_user.assert_called_once_with(MOCK_USER)


# Test delete_user method with non-existent user
@patch("app.services.user_service.UserRepository.user_exists_by_id")
def test_delete_user_not_found(mock_user_exists_by_id, user_service):
    # Mock repository method to return False (user not found)
    mock_user_exists_by_id.return_value = False

    # Call the method and expect an exception
    with pytest.raises(HTTPException) as exc_info:
        user_service.delete_user(MOCK_USER_ID)

    # Assertions
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == f"User {MOCK_USER_ID} not found"
