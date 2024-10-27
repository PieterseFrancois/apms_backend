-- Migration script to create temperature_profiles table
CREATE TABLE temperature_profiles (
    id SERIAL PRIMARY KEY,
    machine_id INT NOT NULL,
    max_temp DOUBLE PRECISION NOT NULL,
    safe_temp DOUBLE PRECISION NOT NULL,
    desired_temp DOUBLE PRECISION NOT NULL,
    bake_time_sec INT NOT NULL,
    CONSTRAINT fk_machine
        FOREIGN KEY (machine_id)
        REFERENCES machines(id)
        ON DELETE CASCADE
);

ALTER TABLE temperature_profiles
ADD COLUMN label VARCHAR(255) NOT NULL DEFAULT 'Unnamed Profile';