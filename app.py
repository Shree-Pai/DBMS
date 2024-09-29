from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required to use session

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        username="root",
        password="",  # Set your MySQL password
        database="agricultureequipment"
    )

# Route for the home page (Login Page)
@app.route('/')
def index():
    return render_template('login.html')

# Route for the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)  # Hashing the password for security

        # Save user to the database
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        db.commit()
        cursor.close()
        db.close()

        flash('Registration successful! You can now login.', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')

# Route for login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    db.close()

    if user and check_password_hash(user[2], password):  # Assuming password is in 2nd column
        session['user_id'] = user[0]  # Store user ID in session
        session['username'] = user[1]  # Store username in session
        return redirect(url_for('equipment_details'))  # Redirect to equipment details
    else:
        flash('Login failed. Check your username or password.', 'danger')
        return redirect(url_for('index'))

# Route for the equipment details page
@app.route('/equipment_details', methods=['GET', 'POST'])
def equipment_details():
    if 'user_id' not in session:
        return redirect(url_for('index'))  # Redirect to login if not logged in

    db = get_db_connection()
    cursor = db.cursor()

    if request.method == 'POST':
        # Insert new equipment data
        name = request.form['name']
        type_ = request.form['type']
        manufacturer = request.form['manufacturer']
        model = request.form['model']
        purchase_date = request.form['purchase_date']
        purchase_price = request.form['purchase_price']
        status = request.form['status']

        cursor.execute("""
            INSERT INTO equipment (name, type, manufacturer, model, purchase_date, purchase_price, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, type_, manufacturer, model, purchase_date, purchase_price, status))
        db.commit()
        flash('Equipment added successfully!', 'success')

    # Fetch all equipment data
    cursor.execute("SELECT * FROM equipment")
    equipment_data = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('equipment_details.html', equipment=equipment_data, username=session['username'])

# Route for editing equipment
@app.route('/edit/<int:equip_id>', methods=['GET', 'POST'])
def edit_equipment(equip_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))  # Redirect to login if not logged in

    db = get_db_connection()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the equipment data in the database
        name = request.form['name']
        type_ = request.form['type']
        manufacturer = request.form['manufacturer']
        model = request.form['model']
        purchase_date = request.form['purchase_date']
        purchase_price = request.form['purchase_price']
        status = request.form['status']

        cursor.execute("""
            UPDATE equipment
            SET name = %s, type = %s, manufacturer = %s, model = %s, purchase_date = %s, purchase_price = %s, status = %s
            WHERE id = %s
        """, (name, type_, manufacturer, model, purchase_date, purchase_price, status, equip_id))
        db.commit()
        cursor.close()
        db.close()
        flash('Equipment updated successfully!', 'success')
        return redirect(url_for('equipment_details'))

    # Fetch the current equipment details to pre-fill the form
    cursor.execute("SELECT * FROM equipment WHERE id = %s", (equip_id,))
    equipment = cursor.fetchone()
    cursor.close()
    db.close()

    return render_template('edit_equipment.html', equipment=equipment)

# Route for deleting equipment
@app.route('/delete/<int:equip_id>')
def delete_equipment(equip_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))  # Redirect to login if not logged in

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM equipment WHERE id = %s", (equip_id,))
    db.commit()
    cursor.close()
    db.close()

    flash('Equipment deleted successfully!', 'success')
    return redirect(url_for('equipment_details'))

# Route for logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
