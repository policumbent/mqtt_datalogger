import sqlite3 as sq
from sqlite3 import Error

class Uploader:
    def __init__(self, db_file):
        self.conn = self.create_connection(db_file)

    def create_connection(self, db_file):
        conn = None #create connection object
        try:
            conn = sq.connect(db_file)
            print(sq.version)
        except Error as e:
            print(e)
        return conn

    def create_table(self, table_sql):
        """
        creates a table with a sqlite3 string in input
        """
        try: 
            c = self.conn.cursor()
            c.execute(table_sql)
        except Error as e:
            print(e)

    def generate_str_table(self, topics, name):
        ''' 
            takes topics from the csvs topics and uses as a primary key the timestamp <<<EDIT WITH THE RIGHT TIMESTAMP OF THE TWO
            generates a string command to create a table via sqlite
        '''
        sql_create_table = f"CREATE TABLE IF NOT EXISTS {name} (\n"
        for topic in topics:
            if topic == 'timestamp': #'timestamp_net'
                sql_create_table += f"    {topic} text NOT NULL PRIMARY KEY,\n"
            else:
                sql_create_table += f"    {topic} REAL NOT NULL,\n"
        sql_create_table = sql_create_table.rstrip(',\n') + "\n);"
        return sql_create_table
    
    
    def insert_table(self, topics, element, name):
        '''
            creation of the sqlite3 command for the insertion of elements
            joins the topics separated by a comma, then creates an equal ammount of question marks
            then inserts in the table via the execute command
        '''
        topics_str = ', '.join(topics)
        values_str = ', '.join(['?' for _ in topics])
        sql_insert = f"INSERT INTO {name}({topics_str}) VALUES({values_str})"
        cur = self.conn.cursor()
        cur.execute(sql_insert, element)
        self.conn.commit()
        return cur.lastrowid