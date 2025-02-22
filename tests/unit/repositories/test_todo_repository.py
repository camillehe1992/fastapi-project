import unittest
from unittest.mock import patch, MagicMock
from uuid import UUID
from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from app.db.models import Todo
from app.schemas.todo import TodoInput
from app.repositories.todo_repository import (
    TodoRepository,
)


class TestTodoRepository(unittest.TestCase):

    def setUp(self):
        # Mock the SQLAlchemy session
        self.mock_session = MagicMock(spec=Session)
        self.todo_repository = TodoRepository(self.mock_session)

        # Common mock data
        self.todo_id = UUID("c9bf9e57-1685-4c89-bafb-ff5af830be8a")
        self.user_id = UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479")
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        # Mock Todo instance
        self.mock_db_item = MagicMock(spec=Todo)
        self.mock_db_item.id = self.todo_id
        self.mock_db_item.title = "Test Todo"
        self.mock_db_item.completed = False
        self.mock_db_item.created_at = self.created_at
        self.mock_db_item.updated_at = self.updated_at
        self.mock_db_item.user_id = self.user_id

    def tearDown(self):
        # Stop all patches
        patch.stopall()

    @patch("app.repositories.todo_repository.Todo")  # Patch the Todo model
    def test_create(self, mock_todo_model):
        # Arrange
        todo_input = TodoInput(title="Test Todo", completed=False, user_id=self.user_id)
        mock_todo_model.return_value = self.mock_db_item
        self.mock_session.add.return_value = None
        self.mock_session.commit.return_value = None
        self.mock_session.refresh.return_value = None

        # Act
        result = self.todo_repository.create(todo_input)

        # Assert
        mock_todo_model.assert_called_once_with(**todo_input.model_dump())
        self.mock_session.add.assert_called_once_with(self.mock_db_item)
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(self.mock_db_item)
        self.assertIsInstance(result, Todo)
        self.assertEqual(result.id, self.mock_db_item.id)
        self.assertEqual(result.title, self.mock_db_item.title)
        self.assertEqual(result.completed, self.mock_db_item.completed)
        self.assertEqual(result.created_at, self.mock_db_item.created_at)
        self.assertEqual(result.updated_at, self.mock_db_item.updated_at)
        self.assertEqual(result.user_id, self.mock_db_item.user_id)

    def test_get_all(self):
        # Arrange
        page = 1
        page_size = 15
        mock_db_items = [
            MagicMock(
                spec=Todo,
                id=self.todo_id,
                title="Todo 1",
                completed=False,
                created_at=self.created_at,
                updated_at=self.updated_at,
                user_id=self.user_id,
            ),
            MagicMock(
                spec=Todo,
                id=UUID("123e4567-e89b-42d3-a456-556642440000"),
                title="Todo 2",
                completed=True,
                created_at=self.created_at,
                updated_at=self.updated_at,
                user_id=self.user_id,
            ),
        ]

        # Mock the counting query
        mock_count_query = MagicMock()
        mock_count_query.count.return_value = 2

        # Mock the fetching query
        mock_fetch_query = MagicMock()
        mock_offset = MagicMock()
        mock_limit = MagicMock()

        # Set up the mock chain for offset, limit, and all
        mock_fetch_query.offset.return_value = mock_offset
        mock_offset.limit.return_value = mock_limit
        mock_limit.all.return_value = mock_db_items

        # Use side_effect to return different mocks for the two calls to query
        self.mock_session.query.side_effect = [mock_count_query, mock_fetch_query]

        # Act
        total_count, result = self.todo_repository.get_all(
            page=page, page_size=page_size
        )

        # Assert
        # Verify the counting query
        self.assertEqual(self.mock_session.query.call_count, 2)
        mock_count_query.count.assert_called_once()

        # Verify the fetching query
        mock_fetch_query.offset.assert_called_once_with((page - 1) * page_size)
        mock_offset.limit.assert_called_once_with(page_size)
        mock_limit.all.assert_called_once()

        self.assertEqual(total_count, 2)
        self.assertIsInstance(result, List)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Todo)
        self.assertEqual(result[0].id, mock_db_items[0].id)
        self.assertEqual(result[0].title, mock_db_items[0].title)
        self.assertEqual(result[0].completed, mock_db_items[0].completed)
        self.assertEqual(result[0].created_at, mock_db_items[0].created_at)
        self.assertEqual(result[0].updated_at, mock_db_items[0].updated_at)
        self.assertEqual(result[0].user_id, mock_db_items[0].user_id)

    def test_get_by_id(self):
        # Arrange
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = (
            self.mock_db_item
        )

        # Act
        result = self.todo_repository.get_by_id(self.todo_id)

        # Assert
        self.mock_session.query.return_value.filter_by.assert_called_once_with(
            id=self.todo_id
        )
        self.assertIsInstance(result, Todo)
        self.assertEqual(result.id, self.mock_db_item.id)
        self.assertEqual(result.title, self.mock_db_item.title)
        self.assertEqual(result.completed, self.mock_db_item.completed)
        self.assertEqual(result.created_at, self.mock_db_item.created_at)
        self.assertEqual(result.updated_at, self.mock_db_item.updated_at)
        self.assertEqual(result.user_id, self.mock_db_item.user_id)

    def test_delete(self):
        # Arrange
        self.mock_session.delete.return_value = None
        self.mock_session.commit.return_value = None

        # Act
        result = self.todo_repository.delete(self.mock_db_item)

        # Assert
        self.mock_session.delete.assert_called_once_with(self.mock_db_item)
        self.mock_session.commit.assert_called_once()
        self.assertTrue(result)

    def test_exists_by_id(self):
        # Arrange
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = (
            self.mock_db_item
        )

        # Act
        result = self.todo_repository.exists_by_id(self.todo_id)

        # Assert
        self.mock_session.query.return_value.filter_by.assert_called_once_with(
            id=self.todo_id
        )
        self.assertTrue(result)

    def test_update(self):
        # Arrange
        updated_input = TodoInput(
            title="New Title", completed=True, user_id=self.user_id
        )
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = (
            self.mock_db_item
        )
        self.mock_session.commit.return_value = None
        self.mock_session.refresh.return_value = None

        # Act
        result = self.todo_repository.update(self.mock_db_item, updated_input)

        # Assert
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(self.mock_db_item)
        self.assertIsInstance(result, Todo)
        self.assertEqual(result.id, self.mock_db_item.id)
        self.assertEqual(result.title, updated_input.title)
        self.assertEqual(result.completed, updated_input.completed)
        self.assertEqual(result.created_at, self.mock_db_item.created_at)
        self.assertEqual(result.updated_at, self.mock_db_item.updated_at)
        self.assertEqual(result.user_id, self.mock_db_item.user_id)
