from typing import Any
from unittest import TestCase

import pytest

from tcc.core.application.register.exceptions import (
    DependencyAlreadyExist,
    DependencyNotFound,
)
from tcc.core.infra.register.application_register import ApplicationRegister


class RegisterTest(TestCase):
    def test_should_register_dependency(self):
        register = ApplicationRegister()

        test_object = object()
        register.provide("test", test_object)

        self.assertEqual(len(register.dependencies), 1)
        self.assertIn(test_object, register.dependencies.values())

    def test_inject_method_should_be_return_object(self):
        register = ApplicationRegister()

        test_object = object()
        register.provide("test", test_object)

        received_object = register.inject("test")

        self.assertIs(received_object, test_object)


class TestRaisesInRegister(TestCase):
    def setUp(self) -> None:
        self.test_object = object()
        self.register = ApplicationRegister()

        self.register.provide("test", self.test_object)

    def test_should_be_raise_when_register_with_same_name(self):
        with self.assertRaises(DependencyAlreadyExist) as e:
            self.register.provide("test", self.test_object)

        self.assertEqual("dependência 'test' já registrada", str(e.exception))

    def test_should_be_raise_when_inject_non_existing_dependency(self):
        with self.assertRaises(DependencyNotFound) as e:
            self.register.inject("dependency")

        self.assertEqual(
            "dependência 'dependency' não registrada", str(e.exception)
        )


@pytest.mark.parametrize(
    "objects",
    [
        (object(), "objeto"),
        (object(), object()),  # type: ignore
        (
            ApplicationRegister(),
            pytest.fixture,
            pytest.Config,
            ArithmeticError,
            ...,
            Exception,
            None,
        ),
    ],
    ids=["um objeto e uma string", "dois objetos", "varios objetos"],
)
def test_should_be_register_and_get(objects: Any):
    register = ApplicationRegister()
    for i, obj in enumerate(objects):
        name = "obj %d" % i
        register.provide(name, obj)

    for i, obj in enumerate(objects):
        name = "obj %d" % i
        received = register.inject(name)
        assert received is obj
