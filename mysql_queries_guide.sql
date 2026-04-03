-- ==========================================
-- SPAS TiDB / MySQL Database Commands Cheat Sheet
-- ==========================================
-- You can copy and paste these commands into TiDB Cloud's "SQL Editor"
-- or any MySQL Desktop App (like Workbench or DBeaver).

-- ------------------------------------------
-- 1. VIEWING DATA (SELECT)
-- ------------------------------------------

-- View all registered students
SELECT * FROM users;

-- View all registered faculty members
SELECT * FROM faculty;

-- View all exam results from all students
SELECT * FROM results;

-- View all results for a specific student (replace 12345 with the roll number)
SELECT * FROM results WHERE roll_no = '12345';

-- View all subjects
SELECT * FROM subjects;

-- View all practicals
SELECT * FROM practicals;

-- View all exam questions
SELECT * FROM questions;

-- View all attendance sessions created by faculty
SELECT * FROM attendance_sessions;

-- View all attendance records (who was present)
SELECT * FROM attendance_records;


-- ------------------------------------------
-- 2. SEARCHING & FILTERING
-- ------------------------------------------

-- Find a specific student by their Roll Number
SELECT * FROM users WHERE roll_no = '12345';

-- Find all students in a specific branch (e.g., Computer Science)
SELECT * FROM users WHERE branch = 'Computer Science';

-- Find all students in a specific year (e.g., 2nd)
SELECT * FROM users WHERE year = '2nd';

-- See the highest scoring students in a specific practical
SELECT * FROM results WHERE practical_name = 'Practical No: 1' ORDER BY correct DESC;


-- ------------------------------------------
-- 3. UPDATING DATA (UPDATE)
-- ------------------------------------------

-- Change a student's full name
UPDATE users SET full_name = 'New Name' WHERE roll_no = '12345';

-- Change a student's branch
UPDATE users SET branch = 'Information Technology' WHERE roll_no = '12345';


-- ------------------------------------------
-- 4. DELETING DATA (DELETE)
-- ------------------------------------------

-- WARNING: Deleting data cannot be undone easily!

-- Delete a specific student entirely
DELETE FROM users WHERE roll_no = '12345';

-- Delete all results for a specific student
DELETE FROM results WHERE roll_no = '12345';

-- Delete a specific faculty member
DELETE FROM faculty WHERE faculty_id = 'FAC001';


-- ------------------------------------------
-- 5. COUNTING DATA (AGGREGATION)
-- ------------------------------------------

-- Count exactly how many students are registered total
SELECT COUNT(*) FROM users;

-- Count how many exam results have been submitted total
SELECT COUNT(*) FROM results;

-- ------------------------------------------
-- 6. DANGER ZONE (WIPE EVERYTHING)
-- ------------------------------------------
-- ONLY RUN THESE IF YOU WANT TO DELETE ABSOLUTELY EVERYONE'S DATA!

-- DELETE FROM results;
-- DELETE FROM attendance_records;
-- DELETE FROM users;
-- DELETE FROM faculty;
