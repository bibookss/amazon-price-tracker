import sqlite3

# Query the database to see if the product already exists
conn = sqlite3.connect('products.db')
c = conn.cursor()
c.execute('SELECT * FROM products')

# Print the results
for row in c:
    print(row)

