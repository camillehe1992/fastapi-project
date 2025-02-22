import unittest
from unittest.mock import patch, MagicMock
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import Todo  # Import the actual Todo model
from app.schemas.todo import TodoInput, TodoList, TodoOutput
from app.repositories.todo_repository import (
    TodoRepository,
)  # Replace with the actual module path


class TestTodoRepository(unittest.TestCase):

    def setUp(self):
        # Mock the SQLAlchemy session
        self.mock_session = MagicMock(spec=Session)
        self.todo_repository = TodoRepository(self.mock_session)

    # @patch("app.repositories.todo_repository.Todo")  # Patch the Todo model
    # def test_create(self, mock_todo_model):
    #     # Arrange
    #     todo_input = TodoInput(
    #         title="Test Todo",
    #         completed=False,
    #         user_id=UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479"),
    #     )
    #     mock_db_item = MagicMock(spec=Todo)
    #     mock_db_item.__dict__ = {
    #         "id": UUID("c9bf9e57-1685-4c89-bafb-ff5af830be8a"),
    #         "title": "Test Todo",
    #         "completed": False,
    #         "created_at": datetime.now(),
    #         "updated_at": datetime.now(),
    #         "user_id": UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479"),
    #     }
    #     mock_todo_model.return_value = mock_db_item
    #     self.mock_session.add.return_value = None
    #     self.mock_session.commit.return_value = None
    #     self.mock_session.refresh.return_value = None

    #     # Act
    #     result = self.todo_repository.create(todo_input)

    #     # Assert
    #     mock_todo_model.assert_called_once_with(**todo_input.model_dump())
    #     self.mock_session.add.assert_called_once_with(mock_db_item)
    #     self.mock_session.commit.assert_called_once()
    #     self.mock_session.refresh.assert_called_once_with(mock_db_item)
    #     self.assertIsInstance(result, TodoOutput)
    #     self.assertEqual(result.id, mock_db_item.id)
    #     self.assertEqual(result.title, mock_db_item.title)
    #     self.assertEqual(result.completed, mock_db_item.completed)
    #     self.assertEqual(result.user_id, mock_db_item.user_id)

    # @patch("app.repositories.todo_repository.Todo")  # Patch the Todo model
    # def test_get_all(self, mock_todo_model):
    #     # Arrange
    #     page = 1
    #     page_size = 15
    #     mock_db_items = [
    #         MagicMock(
    #             spec=Todo,
    #             id=UUID("c9bf9e57-1685-4c89-bafb-ff5af830be8a"),
    #             title="Todo 1",
    #             completed=False,
    #             user_id=UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479"),
    #             created_at=datetime.now(),
    #             updated_at=datetime.now(),
    #         ),
    #         MagicMock(
    #             spec=Todo,
    #             id=UUID("123e4567-e89b-42d3-a456-556642440000"),
    #             title="Todo 2",
    #             completed=True,
    #             user_id=UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479"),
    #             created_at=datetime.now(),
    #             updated_at=datetime.now(),
    #         ),
    #     ]
    #     self.mock_session.query.return_value.count.return_value = 2
    #     self.mock_session.query.return_value.offset.return_value.limit.return_value.all.return_value = (
    #         mock_db_items
    #     )

    #     # Act
    #     total_count, result = self.todo_repository.get_all(
    #         page=page, page_size=page_size
    #     )

    #     # Assert
    #     self.mock_session.query.return_value.count.assert_called_once()
    #     self.mock_session.query.return_value.offset.assert_called_once_with(
    #         (page - 1) * page_size
    #     )
    #     # self.mock_session.query.return_value.limit.assert_called_once_with(page_size)
    #     self.assertEqual(total_count, 2)
    #     self.assertIsInstance(result, list)
    #     self.assertEqual(len(result), 2)
    #     self.assertIsInstance(result[0], Todo)
    #     self.assertEqual(result[0].id, mock_db_items[0].id)
    #     self.assertEqual(result[0].title, mock_db_items[0].title)
    #     self.assertEqual(result[0].completed, mock_db_items[0].completed)
    #     self.assertEqual(result[0].user_id, mock_db_items[0].user_id)

    @patch("app.repositories.todo_repository.Todo")  # Patch the Todo model
    def test_get_by_id(self, mock_todo_model):
        # Arrange
        todo_id = UUID("c9bf9e57-1685-4c89-bafb-ff5af830be8a")
        mock_db_item = MagicMock(
            spec=Todo,
            id=todo_id,
            title="Test Todo",
            completed=False,
            user_id=UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479"),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = (
            mock_db_item
        )

        # Act
        result = self.todo_repository.get_by_id(todo_id)

        # Assert
        self.mock_session.query.return_value.filter_by.assert_called_once_with(
            id=todo_id
        )
        self.assertIsInstance(result, Todo)
        self.assertEqual(result.id, mock_db_item.id)
        self.assertEqual(result.title, mock_db_item.title)
        self.assertEqual(result.completed, mock_db_item.completed)
        self.assertEqual(result.user_id, mock_db_item.user_id)

    @patch("app.repositories.todo_repository.Todo")  # Patch the Todo model
    def test_delete(self, mock_todo_model):
        # Arrange
        mock_db_item = MagicMock(spec=Todo)
        self.mock_session.delete.return_value = None
        self.mock_session.commit.return_value = None

        # Act
        result = self.todo_repository.delete(mock_db_item)

        # Assert
        self.mock_session.delete.assert_called_once_with(mock_db_item)
        self.mock_session.commit.assert_called_once()
        self.assertTrue(result)

    @patch("app.repositories.todo_repository.Todo")  # Patch the Todo model
    def test_exists_by_id(self, mock_todo_model):
        # Arrange
        todo_id = UUID("c9bf9e57-1685-4c89-bafb-ff5af830be8a")
        mock_db_item = MagicMock(spec=Todo, id=todo_id)
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = (
            mock_db_item
        )

        # Act
        result = self.todo_repository.exists_by_id(todo_id)

        # Assert
        self.mock_session.query.return_value.filter_by.assert_called_once_with(
            id=todo_id
        )
        self.assertTrue(result)

    @patch("app.repositories.todo_repository.Todo")  # Patch the Todo model
    def test_update(self, mock_todo_model):
        # Arrange
        todo_id = UUID("c9bf9e57-1685-4c89-bafb-ff5af830be8a")
        mock_db_item = MagicMock(
            spec=Todo,
            id=todo_id,
            title="Old Title",
            completed=False,
            user_id=UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479"),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        updated_input = TodoInput(
            title="New Title",
            completed=True,
            user_id=UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479"),
        )
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = (
            mock_db_item
        )
        self.mock_session.commit.return_value = None
        self.mock_session.refresh.return_value = None

        # Act
        result = self.todo_repository.update(mock_db_item, updated_input)

        # Assert
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once()
        self.assertIsInstance(result, Todo)
        self.assertEqual(result.id, mock_db_item.id)
        self.assertEqual(result.title, updated_input.title)
        self.assertEqual(result.completed, updated_input.completed)
        self.assertEqual(result.user_id, mock_db_item.user_id)
