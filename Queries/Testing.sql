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






