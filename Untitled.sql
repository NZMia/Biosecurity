-- DELETE FROM users as u 
-- WHERE u.id = 5;

-- SELECT employee.*
-- FROM employee
-- JOIN users ON employee.user_id = users.id
-- WHERE users.role_id = 1;
-- SELECT * FROM departments;-- 

SELECT 
    users.email AS user_email,
    roles.role AS user_role,
    departments.department AS department,
    positions.position AS position,
    employee.*
FROM 
    employee
JOIN 
    users ON employee.user_id = users.id
JOIN 
    roles ON users.role_id = roles.id
LEFT JOIN 
    positions ON employee.position_id = positions.id
LEFT JOIN 
    departments ON employee.department_id = departments.id
WHERE 
    users.id = 2
    AND roles.id = 2;

