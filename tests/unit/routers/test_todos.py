import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.schemas.todo import TodoInput, TodoOutput
from app.schemas.user import UserInDBBase

# Import the router or the function directly
from app.routers.v1 import todos


class TestCreateNewTodo(unittest.TestCase):

    def setUp(self):
        # Common mock objects
        self.mock_session = MagicMock(spec=Session)
        self.mock_current_user = MagicMock(spec=UserInDBBase)
        self.mock_current_user.id = UUID4("f47ac10b-58cc-4372-a567-0e02b2c3d479")

        # Patch get_session and get_current_user
        self.mock_get_session = patch("app.routers.v1.todos.get_session").start()
        self.mock_get_session.return_value = self.mock_session

        self.mock_get_current_user = patch(
            "app.routers.v1.todos.get_current_user"
        ).start()
        self.mock_get_current_user.return_value = self.mock_current_user

        # Create a valid TodoOutput object
        self.mock_todo_output = TodoOutput(
            id=UUID4("c9bf9e57-1685-4c89-bafb-ff5af830be8a"),
            user_id=self.mock_current_user.id,
            title="Test Todo",
            completed=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.mock_another_todo_output = TodoOutput(
            id=UUID4("c9bf9e57-1685-4c89-bafb-ff5af830be8a"),
            user_id=self.mock_current_user.id,
            title="Updated Todo",
            completed=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        self.todo_input = TodoInput(
            title="Test Todo",
            completed=False,
            user_id=self.mock_current_user.id,
        )

        self.todo_id = UUID4("c9bf9e57-1685-4c89-bafb-ff5af830be8a")

        # Patch TodoService
        self.mock_todo_service = patch("app.routers.v1.todos.TodoService").start()
        self.mock_todo_service_instance = self.mock_todo_service.return_value

    def tearDown(self):
        # Stop all patches
        patch.stopall()

    def test_create_new_todo(self):
        # Arrange
        self.mock_todo_service_instance.create.return_value = (
            self.mock_todo_output.model_dump()
        )

        # Act
        response = todos.create_new_todo(
            data=self.todo_input,
            session=self.mock_get_session,
            current_user=self.mock_get_current_user,
        )

        # Assert
        self.mock_todo_service.assert_called_once_with(self.mock_get_session)
        self.mock_todo_service_instance.create.assert_called_once_with(self.todo_input)

        # Validate the response
        self.assertEqual(response.message, "Todo is created successfully.")
        self.assertEqual(response.data.id, self.mock_todo_output.id)
        self.assertEqual(response.data.title, self.mock_todo_output.title)
        self.assertEqual(response.data.completed, self.mock_todo_output.completed)
        self.assertEqual(response.data.user_id, self.mock_todo_output.user_id)

    def test_get_all_todos(self):
        # Arrange
        self.mock_todo_service_instance.get_all.return_value = (
            10,
            [
                self.mock_todo_output.model_dump(),
                self.mock_another_todo_output.model_dump(),
            ],
        )

        page = 1
        page_size = 15

        # Act
        response = todos.get_all_todos(
            session=self.mock_session, page=page, page_size=page_size
        )

        # Assert
        self.mock_todo_service.assert_called_once_with(self.mock_session)
        self.mock_todo_service_instance.get_all.assert_called_once_with(
            page=page, page_size=page_size
        )

        self.assertEqual(response.page, page)
        self.assertEqual(response.page_size, 2)  # Number of todos returned
        self.assertEqual(response.total_count, 10)
        self.assertEqual(len(response.todos), 2)

    def test_get_todo_details(self):
        # Arrange
        self.mock_todo_service_instance.get_by_id.return_value = self.mock_todo_output

        # Act
        response = todos.get_todo_details(_id=self.todo_id, session=self.mock_session)

        # Assert
        self.mock_todo_service.assert_called_once_with(self.mock_session)
        self.mock_todo_service_instance.get_by_id.assert_called_once_with(self.todo_id)

        self.assertEqual(response.id, self.todo_id)
        self.assertEqual(response.title, "Test Todo")
        self.assertEqual(response.completed, False)

    def test_delete_todo(self):
        # Arrange
        self.mock_todo_service_instance.delete.return_value = (
            self.mock_todo_output.model_dump()
        )

        # Act
        response = todos.delete_todo(_id=self.todo_id, session=self.mock_session)

        # Assert
        self.mock_todo_service.assert_called_once_with(self.mock_session)
        self.mock_todo_service_instance.delete.assert_called_once_with(self.todo_id)

        self.assertEqual(response.message, "Todo is deleted successfully.")
        self.assertEqual(response.data.id, self.todo_id)

    def test_update_todo(self):
        # Arrange
        self.mock_todo_service_instance.update.return_value = (
            self.mock_another_todo_output.model_dump()
        )

        # Act
        response = todos.update_todo(
            _id=self.todo_id, data=self.todo_input, session=self.mock_session
        )

        # Assert
        self.mock_todo_service.assert_called_once_with(self.mock_session)
        self.mock_todo_service_instance.update.assert_called_once_with(
            self.todo_id, self.todo_input
        )

        self.assertEqual(response.message, "Todo is updated successfully.")
        self.assertEqual(response.data.id, self.todo_id)
        self.assertEqual(response.data.title, "Updated Todo")
        self.assertEqual(response.data.completed, False)
