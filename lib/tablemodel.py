import os
import sqlite3

class DatabaseModel:

      def __init__(self, database_file):
         self.database_file = database_file
         if not os.path.exists(self.database_file):
               raise FileNotFoundError(f"Could not find database file: {database_file}")

      # Using the built-in sqlite3 system table, return a list of all tables in the database
      def get_table_list(self):
            cursor = sqlite3.connect(self.database_file).cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [table[0] for table in cursor.fetchall()]
            return tables

      # Given a table name, return the rows and column names
      def get_table_content(self, table_name):
            cursor = sqlite3.connect(self.database_file).cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
            table_headers = [column_name[0] for column_name in cursor.description]
            table_content = cursor.fetchall()

            # Note that this method returns 2 variables!
            return table_content, table_headers
      def validate_login(self, username, password):
         con = sqlite3.connect(self.database_file)
         cur = con.cursor()
         query = f"SELECT * FROM Users WHERE username = '{username}' AND password = '{password}'"
         cur.execute(query)
         account = cur.fetchone()
         print("ACCOUNT IS " + str(account))
         return account