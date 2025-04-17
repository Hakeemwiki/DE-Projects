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
    