-- Add the active_profile_id column to machines
ALTER TABLE machines 
ADD COLUMN active_profile_id INT;

-- Add a foreign key constraint to link to temperature_profiles
ALTER TABLE machines 
ADD CONSTRAINT fk_active_profile
FOREIGN KEY (active_profile_id)
REFERENCES temperature_profiles(id)
ON DELETE SET NULL;