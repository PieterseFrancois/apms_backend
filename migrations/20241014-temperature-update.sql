ALTER TABLE temperature_logs
ADD COLUMN machine_id INT,
ADD COLUMN batch_id INT,
ADD FOREIGN KEY (machine_id) REFERENCES machines(id),
ADD FOREIGN KEY (batch_id) REFERENCES oven_batches(id);