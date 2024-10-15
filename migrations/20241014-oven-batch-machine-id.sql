ALTER TABLE oven_batches
ADD COLUMN machine_id INT,
ADD FOREIGN KEY (machine_id) REFERENCES machines(id);