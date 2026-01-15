-- Fix timestamp columns in students table
-- Run this in phpMyAdmin SQL tab

-- 1. Update existing records with NULL/invalid timestamps to current time
UPDATE students 
SET created_at = CURRENT_TIMESTAMP 
WHERE created_at IS NULL OR created_at = '0000-00-00 00:00:00';

UPDATE students 
SET updated_at = CURRENT_TIMESTAMP 
WHERE updated_at IS NULL OR updated_at = '0000-00-00 00:00:00';

-- 2. Modify column definitions to have proper defaults
ALTER TABLE students 
MODIFY COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE students 
MODIFY COLUMN updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- 3. Verify the changes
SELECT id, name, index_number, attendance_status, created_at, updated_at 
FROM students 
ORDER BY id;
