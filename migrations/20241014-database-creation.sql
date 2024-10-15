-- Create TYPE enum for oven_batches and press_batches
CREATE TYPE log_type AS ENUM ('Error', 'Safety', 'Command', 'Phase', 'Confirmation');
CREATE TYPE batch_state_enum AS ENUM ('ACTIVE', 'COMPLETED', 'ERROR');
CREATE TYPE oven_log_description AS ENUM (
    'Error in heating process.',
    'Error in fan operation.',
    'Baking process safety check passed.',
    'Baking process safety check failed.',
    'Safety check overridden.',
    'Oven is idle.',
    'Oven is heating up.',
    'Oven is baking.',
    'Oven is cooling down.',
    'Baking process finished.',
    'Starting oven to bake a batch.',
    'Stopping oven and baking process.'
);
CREATE TYPE press_log_description AS ENUM (
    'Error in press operation.',
    'Error in loading process.',
    'Press process safety check passed.',
    'Press process safety check failed.',
    'Safety check overridden.',
    'Press is idle.',
    'Pulp is being inserted into press.',
    'Press is loading form.',
    'Press is pressing.',
    'Press is extracting finished form.',
    'Press process finished.',
    'Confirmed pulp inserted into press.',
    'Starting press to form a pot.',
    'Stopping press and pressing process.',
    'Opening press.'
);

-- Create 'machines' table
CREATE TABLE machines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Create 'oven_batches' table
CREATE TABLE oven_batches (
    id SERIAL PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    stop_time TIMESTAMP,
    state batch_state_enum NOT NULL
);

-- Create 'humidity_logs' table
CREATE TABLE humidity_logs (
    id SERIAL PRIMARY KEY,
    humidity DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    machine_id INT NOT NULL,
    batch_id INT,
    FOREIGN KEY (machine_id) REFERENCES machines(id),
    FOREIGN KEY (batch_id) REFERENCES oven_batches(id)
);

-- Create 'oven_logs' table
CREATE TABLE oven_logs (
    id SERIAL PRIMARY KEY,
    batch_id INT NOT NULL,
    type log_type NOT NULL,
    description oven_log_description,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (batch_id) REFERENCES oven_batches(id)
);

-- Create 'press_batches' table
CREATE TABLE press_batches (
    id SERIAL PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    stop_time TIMESTAMP,
    state batch_state_enum NOT NULL,
    machine_id INT NOT NULL,
    FOREIGN KEY (machine_id) REFERENCES machines(id)
);

-- Create 'press_logs' table
CREATE TABLE press_logs (
    id SERIAL PRIMARY KEY,
    batch_id INT NOT NULL,
    type log_type NOT NULL,
    description press_log_description,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (batch_id) REFERENCES press_batches(id)
);
