import mysql.connector

# Step 1: Establish a connection to the MySQL server and connect to the 'agricultureequipment' database
mydb = mysql.connector.connect(
    host="localhost",
    username="root",  # MySQL username
    password="",      # MySQL password (leave it blank if no password)
    database="agricultureequipment"  # Name of the database created from the SQL dump
)

mycursor = mydb.cursor()

# Step 2: Fetching data from the 'equipment' table
mycursor.execute("SELECT * FROM equipment")
equipment_data = mycursor.fetchall()

print("Equipment Data:")
for row in equipment_data:
    print(row)

# Step 3: Inserting new data into 'equipment' table
sql = "INSERT INTO equipment (name, type, manufacturer, model, purchase_date, purchase_price, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
val = ('Seeder', 'Planting', 'Kubota', 'SX234', '2024-09-15', 18000.00, 'Active')
mycursor.execute(sql, val)
mydb.commit()  # Commit the transaction

print(f"{mycursor.rowcount} record inserted into 'equipment' table")

# Step 4: Fetching data from the 'maintenance' table
mycursor.execute("SELECT * FROM maintenance")
maintenance_data = mycursor.fetchall()

print("Maintenance Data:")
for row in maintenance_data:
    print(row)

# Closing the cursor and connection
mycursor.close()
mydb.close()
