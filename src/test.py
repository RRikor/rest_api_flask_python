import sqlite3

# Create sqlite3 database
connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

user = (1, 'jose', 'asdf')
insert_query = "INSERT INTO users VALUES (?,?,?)"
cursor.execute(insert_query, user)

users = [
    (2, 'rolf', 'asdf'),
    (3, 'anne', 'jkl')
]
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM  users"
for row in cursor.execute(select_query):
    print(row)

# Commit is only necessary when adding data
connection.commit()
connection.close()