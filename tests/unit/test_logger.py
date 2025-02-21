import unittest
import logging
from app.settings import settings
from app.logger import setup_logging


class TestSetupLogging(unittest.TestCase):

    def test_setup_logging(self):
        # Call the setup_logging function
        logger = setup_logging()

        # Verify the logger's name
        self.assertEqual(logger.name, settings.NICKNAME)

        # Verify the logger's level
        self.assertEqual(logger.level, logging.DEBUG)

        # Verify the logger has a console handler
        handler = logger.handlers[0]
        self.assertIsInstance(handler, logging.StreamHandler)

        # Verify the handler's level
        self.assertEqual(handler.level, logging.INFO)

        # Verify the handler's formatter
        self.assertIsInstance(handler.formatter, logging.Formatter)
        self.assertEqual(
            handler.formatter._fmt,
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
