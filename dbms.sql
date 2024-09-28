CREATE DATABASE agricultureequipment;
USE agricultureequipment;

CREATE TABLE equipment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50),
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    purchase_date DATE,
    purchase_price DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'Active'
);

CREATE TABLE maintenance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id INT,
    date DATE,
    description TEXT,
    cost DECIMAL(10,2),
    FOREIGN KEY (equipment_id) REFERENCES equipment(id)
);

CREATE TABLE parts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    quantity INT,
    unit_price DECIMAL(10,2)
);

CREATE TABLE part_usage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    maintenance_id INT,
    part_id INT,
    quantity INT,
    FOREIGN KEY (maintenance_id) REFERENCES maintenance(id),
    FOREIGN KEY (part_id) REFERENCES parts(id)
);

