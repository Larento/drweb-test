from drweb_test.database import Database
from drweb_test.repl import repl_loop


db = Database()

repl_loop(db)
