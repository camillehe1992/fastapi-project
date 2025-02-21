import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session

from app.db.models import Todo
from app.repositories.todo_repository import (
    TodoRepository,
    TodoInput,
    TodoOutput,
)


class TestTodoRepository(unittest.TestCase):

    def setUp(self):
        self.mock_session = MagicMock(spec=Session)
        self.todo_repository = TodoRepository(self.mock_session)

    @patch("app.repositories.todo_repository.TodoOutput")
    @patch("app.repositories.todo_repository.Todo")
    def test_create(self, mock_todo, mock_todo_output):
        # Arrange
        mock_todo_instance = MagicMock(spec=Todo)  # Mocking a Todo instance
        mock_todo.return_value = mock_todo_instance
        mock_todo_output_instance = MagicMock(
            spec=TodoOutput
        )  # Mocking a TodoOutput instance
        mock_todo_output.return_value = mock_todo_output_instance

        todo_input = TodoInput(title="Test Todo", completed=False)

        # Act
        result = self.todo_repository.create(todo_input)

        # Assert
        mock_todo.assert_called_once_with(**todo_input.model_dump())
        self.mock_session.add.assert_called_once_with(mock_todo_instance)
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(mock_todo_instance)
        mock_todo_output.assert_called_once_with(**mock_todo_instance.__dict__)
        self.assertEqual(result, mock_todo_output_instance)

    # def test_get_all(self):
    #     # Arrange
    #     mock_todo_instance = MagicMock(spec=Todo)  # Mocking a Todo instance
    #     mock_todo_instance.__dict__ = {
    #         "id": uuid4(),
    #         "title": "Test Todo",
    #         "completed": False,
    #     }
    #     self.mock_session.query.return_value.count.return_value = 1
    #     self.mock_session.query.return_value.offset.return_value.limit.return_value.all.return_value = [
    #         mock_todo_instance
    #     ]

    #     # Act
    #     total_count, todo_list = self.todo_repository.get_all(page=1, page_size=15)

    #     # Assert
    #     self.mock_session.query.assert_called_with(Todo)
    #     self.mock_session.query.return_value.count.assert_called_once()
    #     self.mock_session.query.return_value.offset.assert_called_once_with(0)
    #     self.mock_session.query.return_value.limit.assert_called_once_with(15)
    #     self.mock_session.query.return_value.offset.return_value.limit.return_value.all.assert_called_once()
    #     self.assertEqual(total_count, 1)
    #     self.assertEqual(len(todo_list), 1)
    #     self.assertIsInstance(todo_list[0], TodoOutput)

    # def test_get_by_id(self):
    #     # Arrange
    #     todo_id = uuid4()
    #     mock_todo_instance = MagicMock(spec=Todo)  # Mocking a Todo instance
    #     self.mock_session.query.return_value.filter_by.return_value.first.return_value = (
    #         mock_todo_instance
    #     )

    #     # Act
    #     result = self.todo_repository.get_by_id(todo_id)

    #     # Assert
    #     self.mock_session.query.assert_called_with(Todo)
    #     self.mock_session.query.return_value.filter_by.assert_called_once_with(
    #         id=todo_id
    #     )
    #     self.mock_session.query.return_value.filter_by.return_value.first.assert_called_once()
    #     self.assertIsInstance(result, TodoOutput)

    # def test_delete(self):
    #     # Arrange
    #     mock_todo_instance = MagicMock(spec=Todo)  # Mocking a Todo instance

    #     # Act
    #     result = self.todo_repository.delete(mock_todo_instance)

    #     # Assert
    #     self.mock_session.delete.assert_called_once_with(mock_todo_instance)
    #     self.mock_session.commit.assert_called_once()
    #     self.assertTrue(result)

    # def test_exists_by_id(self):
    #     # Arrange
    #     todo_id = uuid4()
    #     mock_todo_instance = MagicMock(spec=Todo)  # Mocking a Todo instance
    #     self.mock_session.query.return_value.filter_by.return_value.first.return_value = (
    #         mock_todo_instance
    #     )

    #     # Act
    #     result = self.todo_repository.exists_by_id(todo_id)

    #     # Assert
    #     self.mock_session.query.assert_called_with(Todo)
    #     self.mock_session.query.return_value.filter_by.assert_called_once_with(
    #         id=todo_id
    #     )
    #     self.mock_session.query.return_value.filter_by.return_value.first.assert_called_once()
    #     self.assertTrue(result)

    # def test_update(self):
    #     # Arrange
    #     todo_id = uuid4()
    #     mock_todo_instance = MagicMock(spec=Todo)  # Mocking a Todo instance
    #     mock_todo_instance.id = todo_id
    #     mock_todo_instance.__dict__ = {
    #         "id": todo_id,
    #         "title": "Old Title",
    #         "completed": False,
    #     }
    #     updated_todo_input = TodoInput(title="New Title", completed=True)

    #     self.mock_session.query.return_value.filter_by.return_value.first.return_value = (
    #         mock_todo_instance
    #     )

    #     # Act
    #     result = self.todo_repository.update(mock_todo_instance, updated_todo_input)

    #     # Assert
    #     self.assertEqual(mock_todo_instance.title, updated_todo_input.title)
    #     self.assertEqual(mock_todo_instance.completed, updated_todo_input.completed)
    #     self.mock_session.commit.assert_called_once()
    #     self.mock_session.refresh.assert_called_once_with(mock_todo_instance)
    #     self.mock_session.query.assert_called_with(Todo)
    #     self.mock_session.query.return_value.filter_by.assert_called_once_with(
    #         id=todo_id
    #     )
    #     self.mock_session.query.return_value.filter_by.return_value.first.assert_called_once()
    #     self.assertIsInstance(result, TodoOutput)
