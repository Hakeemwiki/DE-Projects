-- =========================================================
-- REPORTING: Sample Queries that demonstrate how you retrieve order summaries and stock insights.
-- =========================================================

-- View Orders Summary
SELECT * FROM OrderSummary;

-- View Low Stock Products
SELECT * FROM LowStockProducts;

-- Customer Spending & Tier
-- To see customer spending and categorize them into tiers (Gold, Silver, Bronze)
SELECT * FROM CustomerTiers;

-- Place Multiple Products in an Order
-- This procedure will allow you to place an order with multiple products.
-- You just need to provide the customer_id, product_ids (comma-separated), and quantities (comma-separated)
CALL PlaceMultipleOrder(
    1,                           -- Customer ID
    '1,3,5',                     -- Product IDs (comma-separated)
    '2,5,3'                      -- Quantities (comma-separated)
);


-- Replenish Stock
CALL ReplenishStock(
    1,                           -- Product ID
    20                           -- Quantity to add
);


-- View Inventory Logs
-- To view the changes made to inventory (stock levels)
SELECT * FROM Inventory_Logs;

-- Get Products with Specific Stock Level
-- To find products that are close to running out of stock (below reorder level)
SELECT * FROM Products WHERE stock_quantity <= reorder_level;

-- Get Order Details for All Orders by Customer
-- To view all the orders placed by a customer
SELECT o.order_id, o.order_date, o.total_amount, o.total_items
FROM Orders o
WHERE o.customer_id = 1;  -- Replace 1 with the customer ID you want to check

-- Get Total Spending by Customer
-- To find the total amount spent by each customer
SELECT c.name, SUM(o.total_amount) AS total_spent
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id;

-- Get Products Purchased by Customer
-- To find what products a customer has bought
SELECT p.name AS product_name, od.quantity, od.price_at_order, od.discounted_price
FROM Order_Details od
JOIN Products p ON od.product_id = p.product_id
WHERE od.order_id IN (SELECT order_id FROM Orders WHERE customer_id = 1);  -- Replace 1 with the customer ID

-- Get Order Summary
-- To check the overall order summary including total amount and total items
SELECT * FROM OrderSummary;
