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


