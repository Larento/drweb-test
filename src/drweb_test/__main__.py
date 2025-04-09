from drweb_test import commands
from drweb_test.database import Database
from drweb_test.repl import get_repl_output

db = Database()

while True:
    try:
        user_input = input("> ")
        if output := get_repl_output(user_input, db):
            print(output)
    except commands.CommandError as e:
        print(e)
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
