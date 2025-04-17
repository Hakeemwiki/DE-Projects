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