import unittest
from unittest.mock import patch, MagicMock
from uuid import UUID
from datetime import datetime
from typing import List, Tuple

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.todo import TodoInput, TodoOutput
from app.services.user_service import UserService
from app.repositories.todo_repository import TodoRepository
from app.services.todo_service import TodoService


class TestTodoService(unittest.TestCase):

    def setUp(self):
        # Mock the SQLAlchemy session
        self.mock_session = MagicMock(spec=Session)

        # Mock the TodoRepository and UserService
        self.mock_todo_repository = MagicMock(spec=TodoRepository)
        self.mock_user_service = MagicMock(spec=UserService)

        # Initialize the TodoService with mocked dependencies
        self.todo_service = TodoService(self.mock_session)
        self.todo_service.repository = self.mock_todo_repository
        self.todo_service.user_service = self.mock_user_service

        # Common mock data
        self.todo_id = UUID("c9bf9e57-1685-4c89-bafb-ff5af830be8a")
        self.user_id = UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479")
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        # Mock Todo instance
        self.mock_db_todo = MagicMock()
        self.mock_db_todo.id = self.todo_id
        self.mock_db_todo.title = "Test Todo"
        self.mock_db_todo.completed = False
        self.mock_db_todo.created_at = self.created_at
        self.mock_db_todo.updated_at = self.updated_at
        self.mock_db_todo.user_id = self.user_id
        self.mock_db_todo.as_dict.return_value = {
            "id": self.todo_id,
            "title": "Test Todo",
            "completed": False,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user_id": self.user_id,
        }

    def tearDown(self):
        # Stop all patches
        patch.stopall()

    def test_create(self):
        # Arrange
        todo_input = TodoInput(title="Test Todo", completed=False, user_id=self.user_id)
        self.mock_todo_repository.create.return_value = self.mock_db_todo
        self.mock_user_service.is_superuser.return_value = True

        # Act
        result = self.todo_service.create(todo_input)

        # Assert
        self.mock_todo_repository.create.assert_called_once_with(todo_input)
        self.assertEqual(result.id, self.todo_id)
        self.assertEqual(result.title, "Test Todo")
        self.assertEqual(result.completed, False)
        self.assertEqual(result.user_id, self.user_id)

    # def test_create_forbidden(self):
    #     # Arrange
    #     todo_input = TodoInput(title="Test Todo", completed=False, user_id=self.user_id)
    #     self.mock_user_service.is_superuser.return_value = False

    #     # Act & Assert
    #     with self.assertRaises(HTTPException) as context:
    #         self.todo_service.create(todo_input)
    #     self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(context.exception.detail, "Forbidden")

    def test_get_all(self):
        # Arrange
        page = 1
        page_size = 15
        mock_db_todos = [self.mock_db_todo]
        self.mock_todo_repository.get_all.return_value = (1, mock_db_todos)

        # Act
        total_count, result = self.todo_service.get_all(page=page, page_size=page_size)

        # Assert
        self.mock_todo_repository.get_all.assert_called_once_with(
            page=page, page_size=page_size
        )
        self.assertEqual(total_count, 1)
        self.assertIsInstance(result, List)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, self.todo_id)
        self.assertEqual(result[0].title, "Test Todo")
        self.assertEqual(result[0].completed, False)
        self.assertEqual(result[0].user_id, self.user_id)

    def test_get_by_id(self):
        # Arrange
        self.mock_todo_repository.get_by_id.return_value = self.mock_db_todo

        # Act
        result = self.todo_service.get_by_id(self.todo_id)

        # Assert
        self.mock_todo_repository.get_by_id.assert_called_once_with(self.todo_id)
        self.assertEqual(result.id, self.todo_id)
        self.assertEqual(result.title, "Test Todo")
        self.assertEqual(result.completed, False)
        self.assertEqual(result.user_id, self.user_id)

    def test_delete(self):
        # Arrange
        self.mock_todo_repository.exists_by_id.return_value = True
        self.mock_todo_repository.get_by_id.return_value = self.mock_db_todo

        # Act
        result = self.todo_service.delete(self.todo_id)

        # Assert
        self.mock_todo_repository.exists_by_id.assert_called_once_with(self.todo_id)
        self.mock_todo_repository.get_by_id.assert_called_once_with(self.todo_id)
        self.mock_todo_repository.delete.assert_called_once_with(self.mock_db_todo)
        self.assertEqual(result.id, self.todo_id)
        self.assertEqual(result.title, "Test Todo")
        self.assertEqual(result.completed, False)
        self.assertEqual(result.user_id, self.user_id)

    def test_delete_not_found(self):
        # Arrange
        self.mock_todo_repository.exists_by_id.return_value = False

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            self.todo_service.delete(self.todo_id)
        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            context.exception.detail, f"Todo with ID {self.todo_id} not found"
        )

    def test_update(self):
        # Arrange
        updated_input = TodoInput(
            title="Updated Todo", completed=True, user_id=self.user_id
        )
        self.mock_todo_repository.exists_by_id.return_value = True
        self.mock_todo_repository.get_by_id.return_value = self.mock_db_todo
        self.mock_todo_repository.update.return_value = self.mock_db_todo

        # Act
        result = self.todo_service.update(self.todo_id, updated_input)

        # Assert
        self.mock_todo_repository.exists_by_id.assert_called_once_with(self.todo_id)
        self.mock_todo_repository.get_by_id.assert_called_once_with(self.todo_id)
        self.mock_todo_repository.update.assert_called_once_with(
            self.mock_db_todo, updated_input
        )
        self.assertEqual(result.id, self.todo_id)
        self.assertEqual(result.title, "Test Todo")
        self.assertEqual(result.completed, False)
        self.assertEqual(result.user_id, self.user_id)

    def test_update_not_found(self):
        # Arrange
        updated_input = TodoInput(
            title="Updated Todo", completed=True, user_id=self.user_id
        )
        self.mock_todo_repository.exists_by_id.return_value = False

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            self.todo_service.update(self.todo_id, updated_input)
        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            context.exception.detail, f"Todo with ID {self.todo_id} not found"
        )
