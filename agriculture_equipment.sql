-- Create the database
CREATE DATABASE IF NOT EXISTS agricultureequipment;

-- Use the database
USE agricultureequipment;

-- Create 'equipment' table
CREATE TABLE IF NOT EXISTS equipment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100),
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    purchase_date DATE,
    purchase_price DECIMAL(10, 2),
    status VARCHAR(50)
);

-- Insert sample data into 'equipment'
INSERT INTO equipment (name, type, manufacturer, model, purchase_date, purchase_price, status)
VALUES
    ('Tractor', 'Agricultural', 'John Deere', 'JD5055E', '2021-05-10', 25000.00, 'Active'),
    ('Plow', 'Tilling', 'Case IH', 'CPC101', '2022-01-22', 4000.00, 'Active');

-- Create 'maintenance' table
CREATE TABLE IF NOT EXISTS maintenance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id INT,
    maintenance_date DATE,
    cost DECIMAL(10, 2),
    description TEXT,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id)
);

-- Insert sample data into 'maintenance'
INSERT INTO maintenance (equipment_id, maintenance_date, cost, description)
VALUES
    (1, '2023-07-01', 500.00, 'Engine oil change and filter replacement'),
    (2, '2023-08-15', 150.00, 'Blade sharpening');
