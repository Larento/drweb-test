from drweb_test import commands
from drweb_test.database import Database

__all__ = (
    "parse_command_from_user_input",
    "get_repl_output",
)


def parse_command_from_user_input(user_input: str):
    command, *args = user_input.split(" ")
    match command:
        # Работа с данными
        case "set" | "SET":
            return commands.SetValueForKeyCommand(*args)
        case "get" | "GET":
            return commands.GetValueByKeyCommand(*args)
        case "unset" | "UNSET":
            return commands.UnsetValueForKeyCommand(*args)

        # Транзакции
        case "begin" | "BEGIN":
            return commands.BeginTransactionCommand(*args)
        case "rollback" | "ROLLBACK":
            return commands.RollbackTransactionCommand(*args)
        case "commit" | "COMMIT":
            return commands.CommitTransactionCommand(*args)

        # Поиск данных
        case "counts" | "COUNTS":
            return commands.CountValueReferencesCommand(*args)
        case "find" | "FIND":
            return commands.FindKeysWithValueCommand(*args)

        # Пустая строка ввода
        case "":
            return None

        # Выход
        case "end" | "END":
            raise SystemExit

        # Неизвестная команда
        case _:
            raise commands.CommandError(f'Неизвестная команда: "{command}"')


def get_repl_output(user_input: str, db: Database) -> str | None:
    command = parse_command_from_user_input(user_input)
    if callable(command):
        match command(db):
            case None:
                pass
            case commands.NoValue():
                return "NULL"
            case list() as result:
                return ", ".join(result)
            case _ as result:
                return str(result)
