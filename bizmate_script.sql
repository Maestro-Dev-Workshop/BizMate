CREATE DATABASE bizdb;
USE bizdb;

-- Table: businesses
CREATE TABLE business (
    id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(255),
    name VARCHAR(255),
    business_name VARCHAR(255),
    tg_bot_username VARCHAR(255),
    tg_bot_token VARCHAR(255),
    tg_bot_link VARCHAR(255),
    chat_id VARCHAR(255),
    brief_description TEXT,
    date_joined DATE,
    contact_details VARCHAR(255),
    physical_address VARCHAR(255),
    date_of_birth DATE,
    active BOOLEAN
);

-- Table: products
CREATE TABLE product (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    business_id VARCHAR(255) NOT NULL,
    item_name VARCHAR(255),
    category VARCHAR(255),
    brand VARCHAR(255),
    `active` BOOLEAN,
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
    id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(255),
    name VARCHAR(255),
    age INT,
    gender VARCHAR(1),
    contact_details VARCHAR(255)
);

-- Table: customer_orders
CREATE TABLE customer_order (
    id INTEGER PRIMARY KEY,
    customer_id VARCHAR(255) NOT NULL,
    product_id INTEGER NOT NULL,
    business_id VARCHAR(255) NOT NULL,
    quantity_ordered INTEGER,
    chat_id VARCHAR(255),
    sold_price DECIMAL,
    order_status VARCHAR(255),
    date_ordered TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customer(id),
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (business_id) REFERENCES business(id)
);

CREATE TABLE chat (
	customer_id VARCHAR(255),
    business_id VARCHAR(255),
    chat_id VARCHAR(255),
    PRIMARY KEY(customer_id, business_id, chat_id),
    FOREIGN KEY (customer_id) REFERENCES customer(id),
    FOREIGN KEY (business_id) REFERENCES business(id)
);

-- Table: suppliers
CREATE TABLE supplier (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    business_id INTEGER NOT NULL,
    `active` BOOLEAN,
    name VARCHAR(255),
    contact_details VARCHAR(255),
    FOREIGN KEY (business_id) REFERENCES business(id)
);

-- Table: supply_orders
CREATE TABLE supply_order (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    product_id INTEGER NOT NULL,
    business_id VARCHAR(255) NOT NULL,
    supplier_id INTEGER NOT NULL,
    quantity_ordered INTEGER,
    order_status VARCHAR(255),
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
    `active` BOOLEAN,
    PRIMARY KEY (product_id, supplier_id),
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (supplier_id) REFERENCES supplier(id)
);

-- Table: visits
CREATE TABLE visit (
    customer_id VARCHAR(255) NOT NULL,
    business_id VARCHAR(255) NOT NULL,
    date_of_visit TIMESTAMP,
    visit_summary TEXT,
    orders_made INT,
    PRIMARY KEY (customer_id , business_id , date_of_visit),
    FOREIGN KEY (customer_id)
        REFERENCES customer (id),
    FOREIGN KEY (business_id)
        REFERENCES business (id)
);


CREATE TABLE log_history (
	log_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    business_id VARCHAR(255) NOT NULL,
    login_time TIMESTAMP,
    FOREIGN KEY (business_id) REFERENCES business(id)
);
