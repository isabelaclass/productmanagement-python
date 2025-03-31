CREATE DATABASE products;
USE products;

CREATE TABLE products (
	id INT AUTO_INCREMENT PRIMARY KEY, 
    name VARCHAR(255) NOT NULL,
    vend VARCHAR(255) NOT NULL,
    vend_address VARCHAR(255),
    quantity INT NOT NULL,
    address VARCHAR(255),
    price_unit DECIMAL(10,2) NOT NULL
);

INSERT INTO products (name, vend, vend_address, quantity, 
address, price_unit) VALUES ('Steel Hammer', 'ABC Tools', '123 Tools Street', 50, 'Stock A1', 29.99),
('Screwdriver', 'XPTO Utilities', '456 Screw Avenue', 100, 'Stock B2', 9.50),
('Electric Saw', 'Turbo Machines', '789 Machines Road', 20, 'Stock C3', 199.99),
('Drill Driver', 'Electro Tools', '321 Fasteners Alley', 30, 'Stock D4', 149.90);

SELECT * FROM products

