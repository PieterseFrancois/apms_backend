-- 1. Add machine_id column to oven_logs and press_logs (not allowing NULL)
ALTER TABLE oven_logs
ADD COLUMN machine_id INT NOT NULL;

ALTER TABLE press_logs
ADD COLUMN machine_id INT NOT NULL;

-- 2. Add foreign key constraints for machine_id in both logs tables
ALTER TABLE oven_logs
ADD CONSTRAINT fk_oven_logs_machine_id
FOREIGN KEY (machine_id)
REFERENCES machines(id)
ON DELETE RESTRICT;

ALTER TABLE press_logs
ADD CONSTRAINT fk_press_logs_machine_id
FOREIGN KEY (machine_id)
REFERENCES machines(id)
ON DELETE RESTRICT;

-- 3. Ensure batch_id remains optional (if needed)
ALTER TABLE oven_logs
ALTER COLUMN batch_id DROP NOT NULL;

ALTER TABLE press_logs
ALTER COLUMN batch_id DROP NOT NULL;

-- 1. Create the new ENUM type for oven logs
CREATE TYPE oven_log_type_enum AS ENUM (
    'ERROR_HEAT',
    'ERROR_FAN',
    'BAKE_SAFE',
    'BAKE_UNSAFE',
    'OVERRIDE_SAFETY',
    'PHASE_IDLE',
    'PHASE_HEATING',
    'PHASE_BAKING',
    'PHASE_COOLING',
    'PHASE_FINISHED',
    'BAKE_BATCH',
    'STOP_BAKE'
);

-- 2. Alter the oven_logs table to drop the 'description' column
ALTER TABLE oven_logs 
DROP COLUMN description;

-- 3. Alter the 'type' column to use the new ENUM type
ALTER TABLE oven_logs 
ALTER COLUMN type TYPE oven_log_type USING type::text::oven_log_type_enum;

-- 4. Optional: Add constraints or defaults if necessary
ALTER TABLE oven_logs 
ALTER COLUMN type SET NOT NULL;

-- 1. Create the new ENUM type for press logs
CREATE TYPE press_log_type_enum AS ENUM (
    'ERROR_PRESS',
    'ERROR_LOAD',
    'PRESS_SAFE',
    'PRESS_UNSAFE',
    'OVERRIDE_SAFETY',
    'PHASE_IDLE',
    'PHASE_INSERTING',
    'PHASE_LOADING',
    'PHASE_PRESSING',
    'PHASE_EXTRACTING',
    'PHASE_FINISHED',
    'CONFIRM_INSERTION',
    'PRESS_BATCH',
    'STOP_PRESS',
    'OPEN_PRESS'
);

-- 2. Alter the press_logs table to drop the 'description' column
ALTER TABLE press_logs 
DROP COLUMN description;

-- 3. Alter the 'type' column to use the new ENUM type
ALTER TABLE press_logs 
ALTER COLUMN type TYPE press_log_type USING type::text::press_log_type_enum;

-- 4. Optional: Set NOT NULL on the 'type' column if required
ALTER TABLE press_logs 
ALTER COLUMN type SET NOT NULL;
