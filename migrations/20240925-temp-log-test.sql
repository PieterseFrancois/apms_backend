CREATE TABLE temperature_logs (
    id SERIAL PRIMARY KEY,
    temperature FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);