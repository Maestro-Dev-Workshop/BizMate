-- Insert Businesses
INSERT INTO business (
  id, username, name, business_name, tg_bot_username, tg_bot_token, tg_bot_link, chat_id,
  brief_description, date_joined, contact_details, physical_address, date_of_birth, active
) VALUES
('1362251018', 'bizuser1', 'Alice Green', 'GreenGrocers', NULL, NULL, NULL, NULL,
 'Fresh produce and organic items', '2024-01-10', '08012345678', '12 Market Rd, Lagos', '1988-03-12', TRUE),
('6217992152', 'bizuser2', 'Bob Techie', 'TechWorld', NULL, NULL, NULL, NULL,
 'Electronics and gadgets retailer', '2024-02-15', '08123456789', '88 Tech Blvd, Abuja', '1992-06-22', TRUE);


-- Insert Products
INSERT INTO product (
  business_id, item_name, category, brand, active, minimum_threshold, quantity_in_stock,
  selling_price, minimum_selling_price, expiry_date, metadata
) VALUES
('1362251018', 'Bananas', 'Fruits', 'NatureFresh', TRUE, 15, 80, 500.00, 450.00, '2025-07', '{"unit":"bunch"}'),
('1362251018', 'Brown Eggs (12 Pack)', 'Dairy', 'FarmBest', TRUE, 20, 60, 1200.00, 1100.00, '2025-06', '{"pack_size":"12"}'),
('1362251018', 'Organic Tomatoes', 'Vegetables', 'FreshFarm', TRUE, 10, 50, 800.00, 700.00, '2025-08', '{"unit":"kg"}'),
('1362251018', 'Fresh Milk (1L)', 'Dairy', 'LushDairy', TRUE, 10, 40, 900.00, 850.00, '2025-08', '{"type":"whole milk"}'),
('6217992152', 'Wireless Headphones', 'Accessories', 'AudioPro', TRUE, 10, 25, 25000.00, 24000.00, 'N/A', '{"color":"blue"}'),
('6217992152', 'Smartwatch Pro', 'Wearables', 'TechBrand', TRUE, 5, 15, 60000.00, 58000.00, 'N/A', '{"connectivity":"Bluetooth"}'),
('6217992152', 'USB-C Charging Cable', 'Accessories', 'QuickCharge', TRUE, 20, 100, 2000.00, 1800.00, 'N/A', '{"length":"1m"}'),
('6217992152', 'Smartphone X1', 'Phones', 'TechBrand', TRUE, 5, 30, 250000.00, 240000.00, 'N/A', '{"color":"black"}');


-- Insert Customers
INSERT INTO customer (id, username, name, age, gender, contact_details) VALUES
('cust001', 'cust1', 'Jane Doe', 29, 'F', '09011223344'),
('cust002', 'cust2', 'John Smith', 35, 'M', '08112223344'),
('cust003', 'cust3', 'John Doe', 19, 'M', '08145789967'),
('cust004', 'cust4', 'Grace Lee', 27, 'F', '07099887766');


-- Insert Customer Orders
INSERT INTO customer_order (
  id, customer_id, product_id, business_id, quantity_ordered, chat_id,
  sold_price, order_status, date_ordered
) VALUES
(1, 'cust001', 1, '1362251018', 2, NULL, 500.00, 'Completed', DATE_SUB(NOW(), INTERVAL 14 DAY)),
(2, 'cust001', 2, '1362251018', 1, NULL, 1150.00, 'Completed', DATE_SUB(NOW(), INTERVAL 12 DAY)),
(3, 'cust001', 3, '1362251018', 3, NULL, 800.00, 'Completed', DATE_SUB(NOW(), INTERVAL 9 DAY)),
(4, 'cust001', 4, '1362251018', 2, NULL, 880.00, 'Pending', DATE_SUB(NOW(), INTERVAL 6 DAY)),
(5, 'cust001', 3, '1362251018', 1, NULL, 750.00, 'Completed', DATE_SUB(NOW(), INTERVAL 3 DAY)),
(6, 'cust001', 6, '6217992152', 1, NULL, 59000.00, 'Completed', DATE_SUB(NOW(), INTERVAL 2 DAY)),
(7, 'cust001', 5, '6217992152', 2, NULL, 24000.00, 'Completed', NOW()),
(8, 'cust001', 1, '1362251018', 3, NULL, 450.00, 'Completed', NOW());


-- Insert Suppliers
INSERT INTO supplier (business_id, active, name, contact_details) VALUES
('1362251018', TRUE, 'AgroSuppliers Ltd.', '08034567890'),
('1362251018', TRUE, 'GreenGrow Distributors', 'greengrow@example.com'),
('6217992152', TRUE, 'TechGlobal Ltd.', '08187654321'),
('6217992152', TRUE, 'TechGear Supplies', 'support@techgear.com');


-- Insert Supply Orders
INSERT INTO supply_order (
  product_id, business_id, supplier_id, quantity_ordered, order_status, date_ordered
) VALUES
(1, '1362251018', 1, 10, 'Fulfilled', NOW()),
(2, '6217992152', 2, 50, 'Pending', NOW());


-- Insert Supplier Inventory
INSERT INTO supplier_inventory (product_id, supplier_id, cost_price, available, active) VALUES
(1, 2, 500.00, TRUE, TRUE),
(2, 1, 1000.00, TRUE, TRUE),
(3, 2, 500.00, TRUE, TRUE),
(4, 1, 300.00, TRUE, TRUE),
(5, 2, 20000.00, TRUE, TRUE),
(6, 2, 50000.00, TRUE, TRUE),
(7, 1, 1500.00, TRUE, TRUE),
(8, 1, 200000.00, TRUE, TRUE);


-- Insert Visits
INSERT INTO visit (customer_id, business_id, date_of_visit, visit_summary, orders_made) VALUES
('cust001', '1362251018', DATE_SUB(NOW(), INTERVAL 14 DAY), 'Bought fruits and eggs.', 2),
('cust001', '1362251018', DATE_SUB(NOW(), INTERVAL 9 DAY), 'Picked up tomatoes and milk.', 2),
('cust001', '6217992152', DATE_SUB(NOW(), INTERVAL 3 DAY), 'Browsed tech gadgets and ordered a smartwatch.', 1),
('cust001', '6217992152', DATE_SUB(NOW(), INTERVAL 1 DAY), 'Came back for headphones.', 1);


-- Insert Login History
INSERT INTO log_history (business_id, login_time) VALUES
('1362251018', NOW()),
('6217992152', NOW());
