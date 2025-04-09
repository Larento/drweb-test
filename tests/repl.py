import unittest

from drweb_test import commands
from drweb_test.database import Database
from drweb_test.repl import get_repl_output, parse_command_from_user_input


class TestParser(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def test_set(self):
        self.assertEqual(
            parse_command_from_user_input("set a 10"),
            parse_command_from_user_input("SET a 10"),
            parse_command_from_user_input("SET A 10"),
        )

    def test_get(self):
        self.assertEqual(
            parse_command_from_user_input("get a"),
            parse_command_from_user_input("GET a"),
            parse_command_from_user_input("GET A"),
        )

    def test_unset(self):
        self.assertEqual(
            parse_command_from_user_input("unset a"),
            parse_command_from_user_input("UNSET a"),
            parse_command_from_user_input("UNSET A"),
        )

    def test_counts(self):
        self.assertEqual(
            parse_command_from_user_input("counts a"),
            parse_command_from_user_input("COUNTS a"),
            parse_command_from_user_input("COUNTS A"),
        )

    def test_find(self):
        self.assertEqual(
            parse_command_from_user_input("find a"),
            parse_command_from_user_input("FIND a"),
            parse_command_from_user_input("FIND A"),
        )

    def test_end(self):
        with self.assertRaises(SystemExit):
            parse_command_from_user_input("end")

        with self.assertRaises(SystemExit):
            parse_command_from_user_input("END")

    def test_empty_input(self):
        assert parse_command_from_user_input("") is None

    def test_unknown_command(self):
        with self.assertRaises(commands.CommandError):
            parse_command_from_user_input("unknown")


class TestReplOutput(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        self.db.set("a", "10")

    def test_no_output(self):
        assert get_repl_output("", self.db) is None
        assert get_repl_output("unset a", self.db) is None
        assert get_repl_output("set a 10", self.db) is None

    def test_non_null_output(self):
        output = get_repl_output("get a", self.db)
        assert output is not None and output != "NULL"

        output = get_repl_output("counts 10", self.db)
        assert output is not None and output != "NULL"

        output = get_repl_output("find 10", self.db)
        assert output is not None and output != "NULL"

    def test_null_output(self):
        output = get_repl_output("get b", self.db)
        assert output == "NULL"
