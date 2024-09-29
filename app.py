from flask import Flask, render_template, url_for
import mysql.connector

app = Flask(__name__)

# MySQL database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        username="root",
        password="",
        database="agricultureequipment"
    )

# Home route
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch data from 'equipment' table
    cursor.execute("SELECT * FROM equipment")
    equipment_data = cursor.fetchall()

    # Fetch data from 'maintenance' table
    cursor.execute("SELECT * FROM maintenance")
    maintenance_data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Pass the data to the template
    return render_template('index.html', equipment=equipment_data, maintenance=maintenance_data)

if __name__ == "__main__":
    app.run(debug=True)
