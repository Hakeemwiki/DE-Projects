-- *******************************************************
-- ECOMMERCE INVENTORY & ORDER MANAGEMENT SYSTEM
-- FULL SQL SETUP WITH CUSTOMER INSIGHTS AND PROCEDURES
-- *******************************************************

-- ==============================================
-- PHASE 1: Database Design and Schema Implementation
-- ==============================================

-- Create and select database
CREATE DATABASE IF NOT EXISTS ecommerceInventoryDatabase;
USE ecommerceInventoryDatabase;

-- 1. Create Products Table - [Phase 1 - Products]
CREATE TABLE Products(
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2),
    stock_quantity INT NOT NULL CHECK(stock_quantity >= 0),
    reorder_level INT NOT NULL
);

-- 2. Create Customers Table - [Phase 1 - Customers]
CREATE TABLE Customers(
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(60) NOT NULL,
    email VARCHAR(60) UNIQUE,
    phone VARCHAR(20)
);

-- 3. Create Orders Table - [Phase 1 - Orders]
CREATE TABLE Orders(
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0,
    total_items INT DEFAULT 0,
    FOREIGN KEY(customer_id) REFERENCES Customers(customer_id)
);

-- 4. Create Order Details Table - [Phase 1 - Order Details]
CREATE TABLE Order_Details(
    order_id INT,
    product_id INT,
    quantity INT NOT NULL CHECK(quantity > 0),
    price_at_order DECIMAL(10, 2) NOT NULL,
    discount_percent DECIMAL(5, 2) DEFAULT 0,
    discounted_price DECIMAL(10, 2),
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- 5. Create Inventory Logs Table - [Phase 1 & Phase 2 - Inventory Logs]
CREATE TABLE Inventory_Logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    product_name VARCHAR(60),
    change_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    quantity_change INT NOT NULL,
    description VARCHAR(200),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);



-- Adding a sample data to my tables for the purposes of this work and Demonstration
INSERT INTO Products (name, category, price, stock_quantity, reorder_level)
VALUES
    ('Laptop', 'Electronics', 999.99, 50, 10),
    ('Smartphone', 'Electronics', 699.99, 100, 20),
    ('Headphones', 'Electronics', 149.99, 200, 30),
    ('T-Shirt', 'Clothing', 19.99, 300, 50),
    ('Jeans', 'Clothing', 49.99, 150, 25),
    ('Running Shoes', 'Footwear', 89.99, 120, 20),
    ('Coffee Mug', 'Home', 12.99, 250, 40),
    ('Notebook', 'Stationery', 4.99, 500, 100),
    ('Backpack', 'Accessories', 39.99, 80, 15),
    ('Desk Lamp', 'Home', 29.99, 60, 10),
    ('Wireless Mouse', 'Electronics', 24.99, 180, 30),
    ('Water Bottle', 'Accessories', 14.99, 220, 40),
    ('Sunglasses', 'Accessories', 59.99, 90, 15),
    ('Yoga Mat', 'Fitness', 34.99, 70, 10),
    ('Blender', 'Kitchen', 79.99, 40, 5);
    
    
INSERT INTO Customers (name, email, phone)
VALUES
    ('Suave Juggernaut', 'suave.jug@email.com', '233-456-7890'),
    ('Jane Smith', 'jane.smith@email.com', '234-567-8901'),
    ('Alice Johnson', 'alice.j@email.com', '345-678-9012'),
    ('Bob Brown', 'bob.brown@email.com', '456-789-0123'),
    ('Charlie Davis', 'charlie.d@email.com', '567-890-1234'),
    ('Diana Evans', 'diana.e@email.com', '678-901-2345'),
    ('Frank Wilson', 'frank.w@email.com', '789-012-3456'),
    ('Grace Lee', 'grace.lee@email.com', '890-123-4567'),
    ('Henry Taylor', 'henry.t@email.com', '901-234-5678'),
    ('Ivy Clark', 'ivy.c@email.com', '012-345-6789'),
    ('Jack Adams', 'jack.a@email.com', '111-222-3333'),
    ('Karen Hall', 'karen.h@email.com', '222-333-4444'),
    ('Liam White', 'liam.w@email.com', '333-444-5555'),
    ('Mia Green', 'mia.g@email.com', '444-555-6666'),
    ('Noah King', 'noah.k@email.com', '555-666-7777');
    

-- Setting total_amount to an initial amount of 0
INSERT INTO Orders (customer_id, total_amount)
VALUES
    (1, 0), 
    (2, 0), 
    (3, 0), 
    (4, 0), 
    (5, 0); 
    
    
INSERT INTO Order_Details (order_id, product_id, quantity, price_at_order)
VALUES
    -- Order #1 (Suave Juggernaut: Laptop + Headphones)
    (1, 1, 1, (SELECT price FROM Products WHERE product_id = 1)),
    (1, 3, 2, (SELECT price FROM Products WHERE product_id = 3)),
    
    -- Order #2 (Jane Smith: Smartphone + T-Shirt)
    (2, 2, 1, (SELECT price FROM Products WHERE product_id = 2)),
    (2, 4, 3, (SELECT price FROM Products WHERE product_id = 4)),
    
    -- Order #3 (Alice Johnson: Jeans + Running Shoes)
    (3, 5, 2, (SELECT price FROM Products WHERE product_id = 5)),
    (3, 6, 1, (SELECT price FROM Products WHERE product_id = 6)),
    
    -- Order #4 (Bob Brown: Coffee Mug + Notebook)
    (4, 7, 4, (SELECT price FROM Products WHERE product_id = 7)),
    (4, 8, 5, (SELECT price FROM Products WHERE product_id = 8)),
    
    -- Order #5 (Charlie Davis: Backpack + Desk Lamp)
    (5, 9, 1, (SELECT price FROM Products WHERE product_id = 9)),
    (5, 10, 1, (SELECT price FROM Products WHERE product_id = 10)),
    
    -- Additional orders to reach 15 records
    (1, 11, 1, (SELECT price FROM Products WHERE product_id = 11)),
    (2, 12, 2, (SELECT price FROM Products WHERE product_id = 12)),
    (3, 13, 1, (SELECT price FROM Products WHERE product_id = 13)),
    (4, 14, 1, (SELECT price FROM Products WHERE product_id = 14)),
    (5, 15, 1, (SELECT price FROM Products WHERE product_id = 15));
    
 

-- ==============================================
-- PHASE 2: Order Placement and Inventory Management
-- ==============================================

-- TRIGGER 1: Track stock changes - [Phase 2.2 & Phase 4.1 - Inventory Logging]
DELIMITER //
CREATE TRIGGER trg_log_inventory_change
AFTER UPDATE ON Products
FOR EACH ROW
BEGIN
    IF OLD.stock_quantity != NEW.stock_quantity THEN
        INSERT INTO Inventory_Logs(product_id, product_name, quantity_change, description)
        VALUES (
            NEW.product_id,
            NEW.name,
            NEW.stock_quantity - OLD.stock_quantity,
            CASE
                WHEN NEW.stock_quantity > OLD.stock_quantity THEN 'Stock Replenishment'
                ELSE 'Order Placement'
            END
        );
    END IF;
END;
//
DELIMITER ;

-- ==============================================
-- PROCEDURE: Place multiple products in a single order
-- [Phase 2.1 & Phase 4.2 - Order Placement Automation]
-- ==============================================

DELIMITER //
CREATE PROCEDURE PlaceMultipleOrder (
    IN p_customer_id INT,
    IN p_product_ids TEXT,
    IN p_quantities TEXT
)
BEGIN
	-- Creating variables for usage in the stored procedure
    DECLARE v_order_id INT;
    DECLARE v_index INT DEFAULT 1;  -- Counter vairiables for looping through items
    DECLARE v_product_id INT;
    DECLARE v_quantity INT;
    DECLARE v_price DECIMAL(10,2);
    DECLARE v_discount_percent DECIMAL(5,2);
    DECLARE v_discounted_price DECIMAL(10,2);
    DECLARE v_total_amount DECIMAL(10,2) DEFAULT 0;
    DECLARE v_total_items INT DEFAULT 0;
    DECLARE v_count INT; -- Number of products in the comma separated list

	-- Calculating the number of items in the product list by counting the commas and adding 1. i.e 1,2,3
    SET v_count = LENGTH(p_product_ids) - LENGTH(REPLACE(p_product_ids, ',', '')) + 1;


	-- Starting a transaction so that there can be a Rollback when there's an error
    START TRANSACTION;

    -- Create a new order
    INSERT INTO Orders (customer_id) VALUES (p_customer_id);
    SET v_order_id = LAST_INSERT_ID(); -- Get the ID of the order that was just inserted

    -- Loop through products
    WHILE v_index <= v_count DO
		-- Extract the v_index-th product ID from the comma-separated string
        SET v_product_id = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_product_ids, ',', v_index), ',', -1) AS UNSIGNED);
        SET v_quantity = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_quantities, ',', v_index), ',', -1) AS UNSIGNED);

        -- Get product price
        SELECT price INTO v_price FROM Products WHERE product_id = v_product_id;

        -- Calculate discount
        SET v_discount_percent = CASE
            WHEN v_quantity >= 10 THEN 10
            WHEN v_quantity >= 5 THEN 5
            WHEN v_quantity >= 3 THEN 2
            ELSE 0
        END;

        SET v_discounted_price = v_price * (1 - v_discount_percent / 100);

        -- Insert into Order_Details
        INSERT INTO Order_Details (order_id, product_id, quantity, price_at_order, discount_percent, discounted_price)
        VALUES (v_order_id, v_product_id, v_quantity, v_price, v_discount_percent, v_discounted_price);

        -- Update totals
        SET v_total_amount = v_total_amount + (v_discounted_price * v_quantity);
        SET v_total_items = v_total_items + v_quantity;

        -- Update stock
        UPDATE Products
        SET stock_quantity = stock_quantity - v_quantity
        WHERE product_id = v_product_id;

        SET v_index = v_index + 1;
    END WHILE;

    -- Finalize order summary
    UPDATE Orders
    SET total_amount = v_total_amount,
        total_items = v_total_items
    WHERE order_id = v_order_id;

    COMMIT;
END;
//
DELIMITER ;

-- ==============================================
-- PHASE 3: Monitoring and Reporting (Views)
-- ==============================================

-- View 1: Order Summary - [Phase 3.1 - Order Summary Reporting]
CREATE VIEW OrderSummary AS
SELECT 
    c.name AS Customer_name,
    o.order_date,
    o.total_amount,
    o.total_items
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id;

-- View 2: Low Stock Products - [Phase 3.1 - Stock Monitoring]
CREATE VIEW LowStockProducts AS
SELECT
    product_id,
    name,
    stock_quantity,
    reorder_level
FROM Products
WHERE stock_quantity < reorder_level;

-- View 3: Customer Spending & Tier - [Phase 3.2 - Customer Insights]
CREATE VIEW CustomerTiers AS
SELECT
    c.customer_id,
    c.name,
    SUM(o.total_amount) AS total_spent,
    CASE
        WHEN SUM(o.total_amount) >= 1000 THEN 'Gold'
        WHEN SUM(o.total_amount) >= 500 THEN 'Silver'
        ELSE 'Bronze'
    END AS tier
FROM Customers c
LEFT JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id;

-- ==============================================
-- PHASE 4: Stock Replenishment (Manual or Scheduled)
-- ==============================================

-- Manual restock procedure (you can call this when needed) - [Phase 4.1]
DELIMITER //
CREATE PROCEDURE ReplenishStock (
    IN p_product_id INT,
    IN p_quantity INT
)
BEGIN
    UPDATE Products
    SET stock_quantity = stock_quantity + p_quantity
    WHERE product_id = p_product_id;
END;
//
DELIMITER ;

-- ==============================================
-- PERFORMANCE OPTIMIZATION (PHASE 5)
-- ==============================================

-- 1. Index on frequently queried/filter columns

-- Products likely filtered by stock quantity (e.g., for restock alerts)
CREATE INDEX idx_stock_quantity ON Products(stock_quantity);

-- Orders often filtered by customer
CREATE INDEX idx_orders_customer_id ON Orders(customer_id);

-- Order_Details join and filtering by product_id
CREATE INDEX idx_orderdetails_product_id ON Order_Details(product_id);

-- Inventory logs - for retrieving product-specific changes
CREATE INDEX idx_inventorylogs_product_id ON Inventory_Logs(product_id);


-- ==============================================
-- TESTING PHASE – Validate Triggers, Procedures, and Views
-- ==============================================

-- Step 1: Check product stock before placing a new order
SELECT product_id, name, stock_quantity FROM Products WHERE product_id IN (1, 3, 5);

-- Step 2: Place a multi-product order for Customer #1 (Suave Juggernaut)
-- Products: 1 (Laptop) x2, 3 (Headphones) x5, 5 (Jeans) x3
-- You can use your own values to confirm
CALL PlaceMultipleOrder(
    1,
    '1,3,5',
    '2,5,3'
);

-- Step 3: Check the newly created order and its details
SELECT * FROM Orders WHERE customer_id = 1 ORDER BY order_id DESC LIMIT 1;

-- Step 4: Check the order details for that order
SELECT * FROM Order_Details
WHERE order_id = (SELECT MAX(order_id) FROM Orders WHERE customer_id = 1); -- This subquery gives us the latest ID using the max

-- Step 5: Confirm that stock quantities were reduced
SELECT product_id, name, stock_quantity FROM Products WHERE product_id IN (1, 3, 5);

-- Step 6: Check inventory logs for changes (trigger test)
SELECT * FROM Inventory_Logs
WHERE product_id IN (1, 3, 5)
ORDER BY change_date DESC;

-- Step 7: Check if the OrderSummary view reflects the new order
SELECT * FROM OrderSummary WHERE Customer_name = 'Suave Juggernaut';

-- Step 8: Check if the CustomerTiers view updates Suave's tier
SELECT * FROM CustomerTiers WHERE name = 'Suave Juggernaut';

-- Step 9: Check LowStockProducts view (if any item falls below reorder level)
SELECT * FROM LowStockProducts;

-- Step 10: Replenish stock for Product ID 1 (Laptop) by 10 units and check again
CALL ReplenishStock(1, 10);
SELECT * FROM Products WHERE product_id = 1;
SELECT * FROM Inventory_Logs WHERE product_id = 1 ORDER BY change_date DESC;




