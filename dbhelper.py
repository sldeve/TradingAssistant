import sqlite3

class DBHelper:

    def __init(self, dbname="alerts.db"):
        # sets database name and establishes a connection to it
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        # creates a table within our databse 
        create_table = "CREATE TABLE IF NOT EXISTS requests (id, exchange, pair, price, chat_id, trigger)"
        self.conn.execute(create_table)
        self.conn.commit()
    
    def add_alert(self, request_tuple):
        # inserts an item into the table
        insert = "INSERT INTO requests VALUES (?,?,?,?,?,?)"
        self.conn.execute(insert, request_tuple)
        self.conn.commit()
    
    def remove_alert(self, id):
        remove = "DELETE FROM requests WHERE id = (?)"
        self.conn.execute()