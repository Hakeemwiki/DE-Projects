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

