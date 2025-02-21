import unittest
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

from app.schemas.response import CommonResponse


# Example data model for testing
class ExampleDataModel(BaseModel):
    id: int
    name: str


class TestCommonResponse(unittest.TestCase):

    def test_common_response_with_data(self):
        # Create an instance of CommonResponse with data
        example_data = ExampleDataModel(id=1, name="Test Name")
        response = CommonResponse[ExampleDataModel](
            message="Success", data=example_data
        )

        # Verify the response attributes
        self.assertEqual(response.message, "Success")
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data.id, 1)
        self.assertEqual(response.data.name, "Test Name")

    def test_common_response_without_data(self):
        # Create an instance of CommonResponse without data
        response = CommonResponse[str](message="No data")

        # Verify the response attributes
        self.assertEqual(response.message, "No data")
        self.assertIsNone(response.data)

    def test_common_response_with_different_data_types(self):
        # Test with integer data
        response_int = CommonResponse[int](message="Integer data", data=42)
        self.assertEqual(response_int.message, "Integer data")
        self.assertEqual(response_int.data, 42)

        # Test with string data
        response_str = CommonResponse[str](message="String data", data="Hello")
        self.assertEqual(response_str.message, "String data")
        self.assertEqual(response_str.data, "Hello")

        # Test with list data
        response_list = CommonResponse[list](message="List data", data=[1, 2, 3])
        self.assertEqual(response_list.message, "List data")
        self.assertEqual(response_list.data, [1, 2, 3])

    def test_common_response_validation(self):
        # Test validation with invalid data type
        with self.assertRaises(ValueError):
            CommonResponse[ExampleDataModel](
                message="Invalid data", data="Not a valid data model"
            )
