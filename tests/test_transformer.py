from unittest import TestCase
from app.transformer import Transformer


class TestTransformer(TestCase):
    def setUp(self) -> None:
        pass
    def test_init_transformer(self):
        try:
            transformer = Transformer()
            error = False
            verbose = ""

        except Exception as e:
            error = True
            verbose = f"error: {e}"

        self.assertFalse(error, verbose)