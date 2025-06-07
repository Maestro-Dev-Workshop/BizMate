CREATE DATABASE bizdb;
USE bizdb;

-- Table: businesses
CREATE TABLE business (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    business_name VARCHAR(255),
    brief_description TEXT,
    date_joined DATE,
    contact_details VARCHAR(255),
    physical_address VARCHAR(255),
    date_of_birth DATE,
    active BOOLEAN,
    password VARCHAR(15),
    basic_info BOOLEAN,
    product_info BOOLEAN,
    supplier_info BOOLEAN
);

-- Table: products
CREATE TABLE product (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    business_id INTEGER NOT NULL,
    item_name VARCHAR(255),
    category VARCHAR(255),
    brand VARCHAR(255),
    minimum_threshold INTEGER,
    quantity_in_stock INTEGER,
    selling_price DECIMAL,
    minimum_selling_price DECIMAL,
    expiry_date VARCHAR(10),
    metadata TEXT,
    FOREIGN KEY (business_id) REFERENCES business(id)
);

-- Table: customers
CREATE TABLE customer (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    name VARCHAR(255),
    age INT,
    gender VARCHAR(1),
    contact_details VARCHAR(255)
);

-- Table: customer_orders
CREATE TABLE customer_order (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    business_id INTEGER NOT NULL,
    quantity_ordered INTEGER,
    discount_factor DECIMAL,
    date_ordered TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customer(id),
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (business_id) REFERENCES business(id)
);

 -- Table: customer_preferences
 CREATE TABLE customer_preference (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    preference VARCHAR(255),
    FOREIGN KEY(customer_id) REFERENCES customer(id)
 );

-- Table: suppliers
CREATE TABLE supplier (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    business_id INTEGER NOT NULL,
    name VARCHAR(255),
    contact_details VARCHAR(255),
    FOREIGN KEY (business_id) REFERENCES business(id)
);

-- Table: supply_orders
CREATE TABLE supply_order (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    product_id INTEGER NOT NULL,
    business_id INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    quantity_ordered INTEGER,
    fufilled BOOLEAN,
    date_ordered TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (business_id) REFERENCES business(id),
    FOREIGN KEY (supplier_id) REFERENCES supplier(id)
);

-- Table: supplier_inventory
CREATE TABLE supplier_inventory (
    product_id INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    cost_price DECIMAL,
    available BOOLEAN,
    PRIMARY KEY (product_id, supplier_id),
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (supplier_id) REFERENCES supplier(id)
);

-- Table: visits
CREATE TABLE visit (
    customer_id INTEGER NOT NULL,
    business_id INTEGER NOT NULL,
    date_of_visit TIMESTAMP,
    purchase_made BOOLEAN,
    PRIMARY KEY (customer_id , business_id , date_of_visit),
    FOREIGN KEY (customer_id)
        REFERENCES customer (id),
    FOREIGN KEY (business_id)
        REFERENCES business (id)
);

CREATE TABLE log_history (
	log_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    business_id INTEGER NOT NULL,
    login_time TIMESTAMP,
    FOREIGN KEY (business_id) REFERENCES business(id)
);

CREATE TABLE non_active (
	business_id INTEGER NOT NULL,
	active BOOLEAN,
	why_leave TEXT,
    PRIMARY KEY (business_id),
    FOREIGN KEY (business_id) REFERENCES business (id)
);
