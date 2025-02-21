import unittest
from sqlalchemy import inspect
from app.db.base import engine
from app.db.models import Base
from app.db.utils import create_tables, drop_tables


class TestDatabaseOperations(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.engine = engine
        self.inspector = inspect(self.engine)

    def test_create_tables(self):
        """Test that tables are created successfully."""
        # Drop all tables first to ensure a clean state
        Base.metadata.drop_all(bind=self.engine)

        # Call the function to create tables
        create_tables()

        # Check if the tables exist
        self.assertTrue(self.inspector.has_table("users"))
        self.assertTrue(self.inspector.has_table("todos"))
        # Uncomment the following lines if you want to test other tables
        # self.assertTrue(self.inspector.has_table('albums'))
        # self.assertTrue(self.inspector.has_table('photos'))
        # self.assertTrue(self.inspector.has_table('posts'))

    def test_drop_tables(self):
        """Test that tables are dropped successfully."""
        # Create tables first to ensure they exist
        create_tables()

        # Call the function to drop tables
        drop_tables()

        # Check if the tables no longer exist
        self.assertFalse(self.inspector.has_table("users"))
        self.assertFalse(self.inspector.has_table("todos"))
        # Uncomment the following lines if you want to test other tables
        # self.assertFalse(self.inspector.has_table('albums'))
        # self.assertFalse(self.inspector.has_table('photos'))
        # self.assertFalse(self.inspector.has_table('posts'))

    def tearDown(self):
        """Clean up the test environment."""
        Base.metadata.drop_all(bind=self.engine)
