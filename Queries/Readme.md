
# E-Commerce Inventory & Order Management System (SQL Project)

**Problem Statement: Inventory and Order Management System**
You are tasked with designing and implementing a database-driven system to manage the
inventory and orders for an e-commerce company. The system needs to handle product
information, customer data, and order processing efficiently while ensuring that stock levels are
properly updated when orders are placed. Additionally, the company wants to track all inventory
changes and streamline processes related to stock replenishment.
The system should provide insights into customer purchase behaviors, monitor stock levels, and
ensure that products are always available for sale. Your solution should support day-to-day
operations such as placing orders, updating inventory, and summarizing important business
metrics like order summaries and customer spending.

This project can serve as a learning tool, a test simulation, or a strong starting point for a more advanced backend solution.

---

## Technologies Used

- MySQL
- SQL Triggers
- Stored Procedures
- Relational Database Design

---

## Project Logic & Design Overview

### Phase 1: Database Schema Design

The schema is built with normalization and referential integrity in mind. Here’s how the tables are structured:

#### 1. `Products` Table
- Stores product details like name, category, price, stock quantity, and reorder level.
- Useful for tracking inventory status and replenishment needs.

#### 2. `Customers` Table
- Maintains customer data with unique emails to avoid duplication.
- Supports future personalization and tracking of order history.

#### 3. `Orders` Table
- Tracks each order placed, including who placed it and when.
- Has fields for `total_amount` and `total_items`, which are updated automatically through logic.

#### 4. `Order_Details` Table
- Links individual products to their respective orders.
- Handles quantity, price, and discounts.
- Uses a composite primary key (`order_id`, `product_id`) for uniqueness.

#### 5. `Inventory_Logs` Table
- Records every inventory change, whether it’s due to order placement or restocking.
- Helps track stock movement and audit changes over time.

---

## Sample Data

The project includes pre-filled entries for:
- A range of products across categories (Electronics, Fashion, Home)
- Several customers
- Simulated orders and related order details

This setup allows for immediate testing and validation of the system.

---

## Phase 2: Business Logic Automation

To make the system dynamic and reduce manual effort, I implemented a trigger and a stored procedure.

### Trigger: `trg_log_inventory_change`

This trigger automatically fires whenever the `stock_quantity` of a product is updated. It does the following:
- Detects whether the stock is being replenished or reduced
- Logs the change into the `Inventory_Logs` table with a timestamp

This provides a complete, automated trail of all inventory activity.

### Stored Procedure: `PlaceMultipleOrder`

This procedure handles the process of placing an order for multiple products at once. Key steps include:
- Accepts a customer ID, list of product IDs, and their corresponding quantities
- Applies discount logic based on quantity thresholds (3+, 5+, 10+)
- Calculates prices with discounts and inserts entries into `Order_Details`
- Updates stock for each product
- Computes the total amount and total number of items for the order
- Uses transactions to ensure consistency: all operations succeed together or roll back together

---

## Business Scenarios Handled

- Real-time inventory updates
- Automatic inventory logging
- Tiered discount system based on quantity
- Atomic, multi-product order processing
- Order and customer tracking

---

## Possible Enhancements

- Add user roles (e.g., admin, customer)
- Build a frontend using Streamlit or Flask
- Connect with a BI tool like Power BI or Tableau for reporting
- Include email notifications for stock levels or order confirmations

---


If you'd like to collaborate or have feedback, feel free to reach out.

---

## File Overview

| Section           | Description |
|-------------------|-------------|
| Database Setup    | Creates the e-commerce database and selects it |
| Table Creation    | Defines schema for products, orders, customers, etc. |
| Sample Data       | Inserts initial records for testing |
| Trigger           | Logs inventory changes |
| Stored Procedure  | Automates placing orders for multiple products |

---

## Sample Procedure Call

To simulate a multi-product order:

```sql
CALL PlaceMultipleOrder(1, '2,3,4', '1,2,1');
```

This places an order for:
- 1 Smartphone
- 2 Headphones
- 1 T-Shirt  
All ordered by the customer with ID 1.
