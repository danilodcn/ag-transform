from unittest import TestCase

from tcc.core.application.singleton.singleton import SingletonMeta


class SingletonTest(TestCase):
    def test_should_be_the_same_object(self):
        class TestSingleton(metaclass=SingletonMeta):
            ...

        obj1 = TestSingleton()
        obj2 = TestSingleton()

        self.assertIs(obj1, obj2)
        self.assertEqual(id(obj1), id(obj2))
