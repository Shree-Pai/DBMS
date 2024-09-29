from flask import Flask, render_template, request, redirect
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

# Home route to display data and handle form submission
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Handle form submission (POST request)
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        manufacturer = request.form['manufacturer']
        model = request.form['model']
        purchase_date = request.form['purchase_date']
        purchase_price = request.form['purchase_price']
        status = request.form['status']

        # Insert data into the 'equipment' table
        sql = "INSERT INTO equipment (name, type, manufacturer, model, purchase_date, purchase_price, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (name, type, manufacturer, model, purchase_date, purchase_price, status)
        cursor.execute(sql, val)
        conn.commit()

        # After insertion, redirect back to the main page (to avoid re-submission on page refresh)
        return redirect('/')

    # Fetch data from the 'equipment' table (GET request)
    cursor.execute("SELECT * FROM equipment")
    equipment_data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Pass the data to the template
    return render_template('index.html', equipment=equipment_data)

# Route to delete equipment
@app.route('/delete/<int:id>', methods=['POST'])
def delete_equipment(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete the record from the 'equipment' table where the id matches
    sql = "DELETE FROM equipment WHERE id = %s"
    cursor.execute(sql, (id,))
    conn.commit()

    cursor.close()
    conn.close()

    # After deletion, redirect back to the main page
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
