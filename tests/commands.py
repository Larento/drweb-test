import unittest

from drweb_test import commands
from drweb_test.database import Database


class TestCommands(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def test_set_value_for_key_command(self):
        command = commands.SetValueForKeyCommand("a", "10")
        assert command(self.db) is None
        assert self.db.get("a") == "10"

    def test_get_value_by_key_command(self):
        self.db.set("a", "10")
        command = commands.GetValueByKeyCommand("a")
        assert command(self.db) == "10"
        assert self.db.get("a") == "10"

        command = commands.GetValueByKeyCommand("b")
        assert isinstance(command(self.db), commands.NoValue)

    def test_unset_value_for_key_command(self):
        self.db.set("a", "10")
        command = commands.UnsetValueForKeyCommand("a")
        assert command(self.db) is None
        assert self.db.get("a") is None

    def test_count_value_references_command(self):
        self.db.set("a", "10")
        self.db.set("b", "10")
        self.db.set("c", "10")
        command = commands.CountValueReferencesCommand("10")
        assert command(self.db) == 3

    def test_find_keys_with_value_command(self):
        self.db.set("d", "10")
        self.db.set("e", "10")
        self.db.set("f", "10")
        command = commands.FindKeysWithValueCommand("10")
        assert command(self.db) == ["d", "e", "f"]

    def test_not_enough_arguments(self):
        with self.assertRaises(commands.CommandError):
            commands.SetValueForKeyCommand()(self.db)

        with self.assertRaises(commands.CommandError):
            commands.GetValueByKeyCommand()(self.db)

        with self.assertRaises(commands.CommandError):
            commands.UnsetValueForKeyCommand()(self.db)

        with self.assertRaises(commands.CommandError):
            commands.CountValueReferencesCommand()(self.db)

        with self.assertRaises(commands.CommandError):
            commands.FindKeysWithValueCommand()(self.db)

    def test_too_many_arguments(self):
        with self.assertRaises(commands.CommandError):
            commands.SetValueForKeyCommand("a", "10", "20")(self.db)

        with self.assertRaises(commands.CommandError):
            commands.GetValueByKeyCommand("a", "10")(self.db)

        with self.assertRaises(commands.CommandError):
            commands.UnsetValueForKeyCommand("a", "10")(self.db)

        with self.assertRaises(commands.CommandError):
            commands.CountValueReferencesCommand("a", "10")(self.db)

        with self.assertRaises(commands.CommandError):
            commands.FindKeysWithValueCommand("a", "10")(self.db)

        with self.assertRaises(commands.CommandError):
            commands.BeginTransactionCommand("a")(self.db)

        with self.assertRaises(commands.CommandError):
            commands.RollbackTransactionCommand("a")(self.db)

        with self.assertRaises(commands.CommandError):
            commands.CommitTransactionCommand("a")(self.db)

    def test_empty_value_argument(self):
        with self.assertRaises(commands.CommandError):
            commands.SetValueForKeyCommand("a", "")(self.db)

        with self.assertRaises(commands.CommandError):
            commands.CountValueReferencesCommand("a", "")(self.db)

        with self.assertRaises(commands.CommandError):
            commands.FindKeysWithValueCommand("a", "")(self.db)


if __name__ == "__main__":
    unittest.main()
