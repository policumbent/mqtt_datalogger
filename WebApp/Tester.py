from os import name
import time
import sqlite3 as sq
from sqlite3 import Error
import random

def create_connection(db_file):
    conn = None #create connection object
    try:
        conn = sq.connect(db_file)
        print(sq.version)
    except Error as e:
        print(e)
    return conn

def create_table(conn, table_sql):
    try: 
        c = conn.cursor()
        c.execute(table_sql)
    except Error as e:
        print(e)
        
def generate_str_table(topics, name):
    ''' takes topics for the csvs and uses as a primary key the timestamp <<<EDIT WITH THE RIGHT TIMESTAMP OF THE TWO
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

def insert_create(conn, topics, element, name):
    topics_str = ', '.join(topics)
    values_str = ', '.join(['?' for _ in topics])
    sql_insert = f"INSERT INTO {name}({topics_str}) VALUES({values_str})"
    cur = conn.cursor()
    cur.execute(sql_insert, element)
    conn.commit()
    return cur.lastrowid

def update_field(conn, pkey, field_name, value, table_name):
    cur = conn.cursor()
    sql_update_query = f"UPDATE {table_name} SET {field_name} = ? WHERE pkey = ?"
    cur.execute(sql_update_query, (value, pkey))
    conn.commit()
    return cur.latrowid
   
#topics in table
topics_miriam_csv = [
    "latitude",
    "longitude",
    "altitude",
    "distance_gps",
    "speed_gps",
    "timestamp",
    "CO2",
    "temp",
    "TVOC",
    "power",
    "heartrate",
    "rpm_wheel",
    "rpm_pedal",
    "distance_hall",
    "speed_hall",
    "gear",
    "receiver",
    "error",
    "limit_switch"
    ]
#generate list of elements
elements = []
for i in range(0,1000):
    instance = [random.randint(1, 100) + random.randint(1, 100)/10 for _ in range(0,5)]
    instance.append(i) #I use numbers as timestamps
    for _ in range(0,13):
        instance.append(random.randint(1, 100) + random.randint(1, 100)/10)
    elements.append(tuple(instance))
print(elements)

    
db = r".\test.db" #database path
conn = create_connection(db)
miriam_table = generate_str_table(topics_miriam_csv, "Miriam")
        
#inserting elements in db
if conn is not None:
    create_table(conn, miriam_table)
    print("connection successful")
    for e in elements:
        insert_create(conn, topics_miriam_csv, e, 'Miriam')  
        time.sleep(1)
        print(f"inserting element")
else:
    print("no connection established")