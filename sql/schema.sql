CREATE TABLE heartbeats (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    heart_rate INTEGER NOT NULL,
    CONSTRAINT valid_heart_rate CHECK (heart_rate >0 AND heart_rate <= 300)
);

-- Create an index on timestamp for efficient time-series queries
CREATE INDEX idx_timestamp ON heartbeats (timestamp);