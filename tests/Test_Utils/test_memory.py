from unittest import TestCase
from tcc.utils.memory import Memory


def sandbox(target: callable, *args: list):
    try:
        response = target(*args)
        success = True
        error = ""

    except Exception as err:
        success = False
        response = ""
        error = f"Error = {err}"

    return success, error, response


class TestMemoryBasic(TestCase):
    def test_memory_create(self):
        success, error, _ = sandbox(Memory)
        self.assertTrue(success, error)

    def test_set_data_in_memory(self):
        # data = {"foo": "bar"}
        m = Memory()
        success, error, _ = sandbox(m.set, "foo2", "bar2")
        m.set("foo", "bar")

        self.assertTrue(success, error)

    def test_get_data(self):
        m = Memory()
        m.set("foo", "bar")

        self.assertEqual(m.get("foo"), "bar")

    def test_error_set_data(self):
        m = Memory()
        data = {"foo": "bar"}
        try:
            m.data = data
            error = False
        except ValueError:
            error = True

        self.assertTrue(error)

    def test_drop_memory(self):
        m = Memory()
        m.set("foo", "bar")

        m.drop()
        self.assertEqual(m.data, {})

    def test_set_many(self):
        m = Memory()
        data = {"foo": "bar", "bar": "foo"}
        m.set_many(data)

        self.assertEqual(m.data, data)

    def test_cache_get(self):
        m = Memory()
        data = {"foo": "bar"}
        m.set_many(data)
        initial = m.get("foo")
        bar = "different value"
        m.set("foo", bar)

        self.assertNotEqual(initial, bar)

    def test_clear_cache(self):
        m = Memory()
        data = {"foo": "bar"}
        m.set_many(data)
        m.cache_clear()
        bar = "different value"
        m.set("foo", bar)

        end = m.get("foo")

        self.assertEqual(end, bar)
