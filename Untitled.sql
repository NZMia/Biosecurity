-- DELETE FROM users as u 
-- WHERE u.id = 5;

-- SELECT employee.*
-- FROM employee
-- JOIN users ON employee.user_id = users.id
-- WHERE users.role_id = 1;
-- SELECT * FROM departments;-- 

-- SELECT 
--     users.email AS user_email,
--     roles.role AS user_role,
--     departments.department AS department,
--     positions.position AS position,
--     employee.*
-- FROM 
--     employee
-- JOIN 
--     users ON employee.user_id = users.id
-- JOIN 
--     roles ON users.role_id = roles.id
-- LEFT JOIN 
--     positions ON employee.position_id = positions.id
-- LEFT JOIN 
--     departments ON employee.department_id = departments.id
-- WHERE 
--     users.id = 2
--     AND roles.id = 2;
    UPDATE employee
    JOIN users ON employee.user_id = users.id
    JOIN roles ON users.role_id = roles.id
    LEFT JOIN positions ON employee.position_id = positions.id
    LEFT JOIN departments ON employee.department_id = departments.id
    SET 
        employee.last_name = COALESCE('las', employee.last_name),
        employee.work_phone = COALESCE('02334343', employee.work_phone)
    WHERE
        employee.user_id = '15';

    UPDATE users
    SET
        users.role_id = COALESCE('2', users.role_id)
    WHERE
        users.id = '15';
