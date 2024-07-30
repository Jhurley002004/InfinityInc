import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv('PSQLHOST')
DB = os.getenv('PSQLDB')
USER = os.getenv('PSQLUSER')
PASSWORD = os.getenv('PSQLPWD')
PORT = os.getenv('PSQLPORT')

# We should be able to pass the database connection
conn = psycopg2.connect(
    host = HOST,
    database = DB,
    user = USER,
    password = PASSWORD,
    port = PORT
)
# Cursor still needs to be created
cur = conn.cursor()

cur.execute(
    'CREATE TABLE IF NOT EXISTS test (id integer NOT NULL, name VARCHAR (50))'
)
cur.execute(
    'INSERT INTO test(id, name) VALUES(%s, %s)', (3, "additional data")
)
cur.execute(
    'INSERT INTO test(id, name) VALUES(%s, %s)', (4, "for demonstration")
)
conn.commit()

cur.execute(
    'SELECT * FROM test'
)
# Fetchone/fetchall doesn't seem to work chained
selected = cur.fetchall()
print(type(selected))
print(selected)

# Cursor and connection must be closed after finished
cur.close()
conn.close()