CREATE TABLE IF NOT EXISTS events (
    event_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    user_name VARCHAR(255),
    user_email VARCHAR(255),
    event_type VARCHAR(60) NOT NULL,
    product_id INT NOT NULL,
    product_name VARCHAR(150),
    product_category VARCHAR(100),
    product_price DECIMAL(10, 2) NOT NULL,
    event_time TIMESTAMP NOT NULL,
    CONSTRAINT valid_event_type CHECK (event_type IN ('view', 'purchase')) -- validate event type
)

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_event_time ON events (event_time);
CREATE INDEX IF NOT EXISTS idx_user_id ON events (user_id);