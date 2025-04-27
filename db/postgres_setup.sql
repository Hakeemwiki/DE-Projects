CREATE TABLE IF NOT EXISTS events (
    event_id SERIAL PRIMARY KEY,
    user_id INT,
    user_name VARCHAR(255),
    user_email VARCHAR(255),
    event_type VARCHAR(60),
    product_id INT,
    product_name VARCHAR(150),
    product_category VARCHAR(100),
    event_time TIMESTAMP
)