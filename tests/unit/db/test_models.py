import unittest
from sqlalchemy import Column, Integer, String
from app.db.models import BaseModel


# Create a concrete model for testing
class ConcreteModel(BaseModel):
    __tablename__ = "concrete_model"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


class TestBaseModel(unittest.TestCase):
    def test_as_dict(self):
        test_model = ConcreteModel(id=1, name="Test Name", age=30)
        expected_dict = {"id": 1, "name": "Test Name", "age": 30}
        self.assertEqual(test_model.as_dict(), expected_dict)

    def test_as_dict_with_empty_model(self):
        empty_model = ConcreteModel()
        expected_dict = {"id": None, "name": None, "age": None}
        self.assertEqual(empty_model.as_dict(), expected_dict)
