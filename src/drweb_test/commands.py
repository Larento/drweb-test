import abc
from typing import Generic, TypeVar

from drweb_test.database import Database

__all__ = (
    "NoValue",
    "CommandError",
    "AbstractCommand",
    "SetValueForKeyCommand",
    "GetValueByKeyCommand",
    "UnsetValueForKeyCommand",
    "CountValueReferencesCommand",
    "FindKeysWithValueCommand",
)


class NoValue:
    """
    В базе отсутствует значение для данного ключа.
    """


class CommandError(Exception):
    """
    При выполнении команды произошла ошибка.
    """


CommandResultT = TypeVar("CommandResultT")


class AbstractCommand(abc.ABC, Generic[CommandResultT]):
    def __init__(self, *args: str):
        self.args = args

    @abc.abstractmethod
    def __call__(self, db: Database) -> CommandResultT: ...

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AbstractCommand):
            return NotImplemented
        return self.args == other.args

    def __hash__(self) -> int:
        return hash(self.args)


class SetValueForKeyCommand(AbstractCommand[None]):
    def __call__(self, db: Database):
        try:
            key, value = self.args
        except ValueError:
            raise CommandError("Команда ожидает 2 аргумента.")

        if not value:
            raise CommandError("Значение не может быть пустым.")

        db.set(key, value)


class GetValueByKeyCommand(AbstractCommand[str | NoValue]):
    def __call__(self, db: Database):
        try:
            (key,) = self.args
        except ValueError:
            raise CommandError("Команда ожидает 1 аргумент.")

        return db.get(key, NoValue())


class UnsetValueForKeyCommand(AbstractCommand[None]):
    def __call__(self, db: Database):
        try:
            (key,) = self.args
        except ValueError:
            raise CommandError("Команда ожидает 1 аргумент.")

        db.unset(key)


class CountValueReferencesCommand(AbstractCommand[int]):
    def __call__(self, db: Database):
        try:
            (value,) = self.args
        except ValueError:
            raise CommandError("Команда ожидает 1 аргумент.")

        if not value:
            raise CommandError("Значение не может быть пустым.")

        return len(db.find_keys_with_value(value))


class FindKeysWithValueCommand(AbstractCommand[list[str]]):
    def __call__(self, db: Database):
        try:
            (value,) = self.args
        except ValueError:
            raise CommandError("Команда ожидает 1 аргумент.")

        if not value:
            raise CommandError("Значение не может быть пустым.")

        return db.find_keys_with_value(value)


class BeginTransactionCommand(AbstractCommand[None]):
    def __call__(self, db: Database):
        if len(self.args) > 0:
            raise CommandError("Команда не ожидает аргументов.")

        db.begin_transaction()


class RollbackTransactionCommand(AbstractCommand[None]):
    def __call__(self, db: Database):
        if len(self.args) > 0:
            raise CommandError("Команда не ожидает аргументов.")

        db.rollback_transaction()


class CommitTransactionCommand(AbstractCommand[None]):
    def __call__(self, db: Database):
        if len(self.args) > 0:
            raise CommandError("Команда не ожидает аргументов.")

        db.commit_transaction()
