from unittest import TestCase
from app import app


class FirstTestCase(TestCase):
    def setUp(self) -> None:
        self.app = app

    def test_root_should_return_200(self):
        ...
