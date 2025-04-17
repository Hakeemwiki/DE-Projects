E-Commerce Inventory & Order Management System (SQL Project)
Welcome to my SQL-based E-commerce Inventory and Order Management System — a robust setup built to manage product inventories, handle customer orders, track stock levels, and provide insight into customer behavior. I designed this system to simulate real-world e-commerce operations with automation, business logic, and clean structure.

This system is ideal for learning, simulations, and can even serve as a solid foundation for a production-grade backend.

Technologies Used
MySQL

SQL Procedures & Triggers

Relational Database Design Principles

Project Logic & Design Philosophy
PHASE 1: Database Schema Design
In this phase, I focused on laying a clean, relational foundation with proper normalization and integrity constraints.

1. Products Table
Holds details of all products available in the inventory.
Key columns:

stock_quantity - keeps track of what's available

reorder_level - helps monitor low stock alerts

2. Customers Table
Stores basic customer data, with email being unique to avoid duplication.

3. Orders Table
Each row represents a customer order, with:

total_amount and total_items dynamically updated.

Linked to Customers via a foreign key.

4. Order_Details Table
Captures the individual products associated with an order, their quantities, prices, and applicable discounts.
Composite primary key (order_id, product_id) ensures no duplicate entries per order-product pair.

5. Inventory_Logs Table
Every time stock is updated, this table logs:

The amount changed

Whether it was due to a replenishment or order placement

Sample Data Insertion
I inserted a variety of products across categories (Electronics, Home, Fashion, etc.) and created sample customer records. This helps simulate real order activity and track how the system behaves under different scenarios.

PHASE 2: Business Logic Automation
Here’s where the system goes from static to dynamic. I introduced automation using Triggers and Stored Procedures.

Trigger: trg_log_inventory_change
Whenever a product’s stock is updated, this trigger:

Inserts a log into Inventory_Logs

Automatically categorizes the stock movement as either Order Placement (stock down) or Replenishment (stock up)

This ensures you always have an audit trail of stock movements — no need for manual entries!

Stored Procedure: PlaceMultipleOrder
This procedure lets you place an order for multiple products at once, all through a single call. Here’s the breakdown of how it works:

Takes Inputs:

p_customer_id: Who’s ordering?

p_product_ids: Comma-separated list of product IDs (e.g. '1,3,5')

p_quantities: Corresponding quantities (e.g. '2,1,4')

Processes Each Product:

Calculates applicable discounts (based on quantity thresholds: 3+, 5+, 10+)

Computes discounted_price

Adds entry to Order_Details

Reduces the product's stock_quantity

Updates the Main Order Record:

total_amount and total_items are computed dynamically

Keeps the logic clean, reusable, and rollback-safe with transactions

With just one call, multiple operations are completed atomically. Either everything goes in or nothing at all — thanks to the transaction block.

Business Scenarios Covered
Track product movement (stock in/out)

Handle dynamic order pricing and discounting

Maintain order history

Prevent stock mismatch with constraints and triggers

Possible Extensions
Add user roles (Admin, Customer)

Introduce product restocking functionality

Visualize orders and stock insights with a BI tool (Power BI or Tableau)

Create a web frontend (Streamlit, Flask, etc.)

About Me
I'm Hakeem Wikireh, a Data Scientist and SQL enthusiast with a strong love for building systems that solve real problems. Whether it’s cleaning datasets, designing dashboards, or writing backends like this, I enjoy the journey from raw data to business value.

If you’re reading this and want to collaborate, ask questions, or brainstorm — feel free to reach out.

📁 File Overview

File/Section	Description
CREATE DATABASE	Creates and selects the e-commerce database
CREATE TABLE	Defines the schema for all core entities
INSERT INTO	Seeds sample products, customers, and orders
TRIGGERS	Automates inventory logging
PROCEDURES	Places complex multi-product orders efficiently

Try It Yourself
Here’s a sample procedure call to simulate an order:

sql
Copy
Edit
CALL PlaceMultipleOrder(1, '2,3,4', '1,2,1');
This places an order for:

1x Smartphone

2x Headphones

1x T-Shirt
All under Customer ID 1 (Suave Juggernaut) 

