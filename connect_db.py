import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("/Users/rucharaval/Documents/FinalProject.sqlite")

# Create a cursor object
cursor = conn.cursor()

# Example: Querying the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

# Close the connection
conn.close()
