import sqlite3 as db

databases = {}

class base:
    valid_name = None #stores the valid name of the database (with file extension)

    def __init__(self, name):
        if name in databases:
            raise NameError("This database already exists")
        self.valid_name = name + ".db"

        with db.connect(name) as file:
            file.cursor.execute("CREATE TABLE IF NOT EXISTS " + name + " (")

        databases[name] = self
    

    def create(name, param_dict):

        command = "CREATE TABLE IF NOT EXISTS " + name + " ("
        
        with db.connect(name + ".db") as file:
            


