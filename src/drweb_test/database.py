import copy
import typing
from collections import OrderedDict

__all__ = ("Database",)


class DataStore(typing.NamedTuple):
    key_value_dict: dict[str, str]
    value_key_dict: dict[str, OrderedDict[str, None]]


class Database:
    """
    Основной класс для хранения значений в по ключу.

    Использует стандартный словарь Python. Поддерживает O(1) поиск ключей по значению, за счет хранения еще одного словаря, у которого пары <значение>-<список ключей>.
    """

    def __init__(self):
        self._store = DataStore(key_value_dict={}, value_key_dict={})
        self._transaction_stack: list[DataStore] = []

    def __getitem__(self, key: str):
        return self._store.key_value_dict[key]

    def get(self, key: str, default: "typing._T" = None):  # type: ignore
        return self._store.key_value_dict.get(key, default)

    def __setitem__(self, key: str, value: str):
        self._store.key_value_dict[key] = value
        try:
            self._store.value_key_dict.setdefault(value, OrderedDict())[key] = None
        except KeyError:
            del self._store.key_value_dict[key]

    def set(self, key: str, value: str):
        self[key] = value

    def __delitem__(self, key: str):
        value = self._store.key_value_dict[key]
        del self._store.key_value_dict[key]
        try:
            del self._store.value_key_dict[value][key]
        except KeyError:
            self._store.key_value_dict[key] = value

    def unset(self, key: str):
        try:
            del self[key]
        except KeyError:
            pass

    def find_keys_with_value(self, value: str) -> list[str]:
        keys_with_value = self._store.value_key_dict.get(value, OrderedDict())
        return list(keys_with_value.keys())

    def begin_transaction(self):
        self._transaction_stack.append(self._store)
        self._store = copy.deepcopy(self._store)

    def rollback_transaction(self):
        try:
            self._store = self._transaction_stack.pop()
        except IndexError:
            pass

    def commit_transaction(self):
        self._transaction_stack.clear()
