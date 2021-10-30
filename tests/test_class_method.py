from unittest import TestCase
from app.utils.classmethod import ClassPropertyDescriptor, classproperty


class MethodForTesting:
    __data = 0

    @classproperty
    def data(cls):
        return cls.__data


class TestPropertyClassBasic(TestCase):
    def test_create_object(self):
        obj = MethodForTesting()
    
    def test_error_while_try_set_the_data(self):
        obj = MethodForTesting()
        with self.assertRaises((AttributeError)) as context:
            obj.data = ...

        self.assertIn("can't set attribute", str(context.exception))