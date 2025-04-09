import unittest

from drweb_test.database import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def test_set(self):
        self.db.set("a", "10")
        self.db.set("b", "20")
        assert self.db.get("a") == "10"
        assert self.db.get("b") == "20"

    def test_unset(self):
        self.db.set("a", "10")
        assert self.db.get("a") == "10"
        self.db.unset("a")
        assert self.db.get("a") is None

    def test_overwrite(self):
        self.db.set("a", "10")
        self.db.set("a", "20")
        assert self.db.get("a") == "20"

    def test_unset_empty(self):
        self.db.unset("a")
        self.db.unset("a")

    def test_find_keys_with_value_in_insertion_order(self):
        self.db.set("a", "10")
        self.db.set("c", "10")
        self.db.set("b", "10")
        self.db.set("z", "10")
        assert self.db.find_keys_with_value("10") == ["a", "c", "b", "z"]

        self.db.unset("a")
        assert self.db.find_keys_with_value("10") == ["c", "b", "z"]


if __name__ == "__main__":
    unittest.main()
