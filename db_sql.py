import mysql.connector

db = mysql.connector.connect(
      host="localhost",
      user="root",
      password="admin",
      database="database"
)

cursor = db.cursor()
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
print(tables)

