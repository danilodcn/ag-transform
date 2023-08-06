from typing import Any
from unittest import TestCase

import pytest

from tcc.core.application.registry.exceptions import (
    DependencyAlreadyExist,
    DependencyNotFound,
)
from tcc.core.infra.registry.application_registry import ApplicationRegistry


class RegistryTest(TestCase):
    def test_should_registry_dependency(self):
        registry = ApplicationRegistry()

        test_object = object()
        registry.provide("test", test_object)

        self.assertEqual(len(registry.dependencies), 1)
        self.assertIn(test_object, registry.dependencies.values())

    def test_inject_method_should_be_return_object(self):
        registry = ApplicationRegistry()

        test_object = object()
        registry.provide("test", test_object)

        received_object = registry.inject("test")

        self.assertIs(received_object, test_object)


class TestRaisesInRegistry(TestCase):
    def setUp(self) -> None:
        self.test_object = object()
        self.registry = ApplicationRegistry()

        self.registry.provide("test", self.test_object)

    def test_should_be_raise_when_registry_with_same_name(self):
        with self.assertRaises(DependencyAlreadyExist) as e:
            self.registry.provide("test", self.test_object)

        self.assertEqual("dependência 'test' já registrada", str(e.exception))

    def test_should_be_raise_when_inject_non_existing_dependency(self):
        with self.assertRaises(DependencyNotFound) as e:
            self.registry.inject("dependency")

        self.assertEqual(
            "dependência 'dependency' não registrada", str(e.exception)
        )


@pytest.mark.parametrize(
    "objects",
    [
        (object(), "objeto"),
        (object(), object()),  # type: ignore
        (
            ApplicationRegistry(),
            pytest.fixture,
            pytest.Config,
            ArithmeticError,
            ...,
            Exception,
            None,
        ),
    ],
    ids=["um objeto e uma string", "dois objetos", "vários objetos"],
)
def test_should_be_registry_and_get(objects: Any):
    registry = ApplicationRegistry()
    for i, obj in enumerate(objects):
        name = "obj %d" % i
        registry.provide(name, obj)

    for i, obj in enumerate(objects):
        name = "obj %d" % i
        received = registry.inject(name)
        assert received is obj
